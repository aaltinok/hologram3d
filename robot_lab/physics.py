"""Quadcopter, paletli tank ve Mars rover (rocker-bogie) için bilimsel hesaplamalar (saf NumPy).

Tüm formüller eğitim amaçlı basitleştirilmiş modellerdir; gerçek robotta sürtünme, aerodinamik ve
aktüatör dinamikleri farklı olabilir.
"""
from __future__ import annotations

import numpy as np

G = 9.81  # m/s^2

# --------------------------------------------------------------------------
# 1) Quadcopter
# --------------------------------------------------------------------------

def thrust_to_weight(mass_kg: float, n_motors: int, max_thrust_g_per_motor: float) -> float:
    """İtki/ağırlık oranı (TWR)."""
    return n_motors * (max_thrust_g_per_motor / 1000.0) * G / (mass_kg * G)


def hover_throttle(twr: float) -> float | None:
    """Asılı kalma gaz oranı. İtki ≈ gaz² varsayımıyla  gaz = sqrt(1/TWR). TWR<1 ise uçamaz (None)."""
    return None if twr < 1.0 else float(np.sqrt(1.0 / twr))


def quad_flight_time(mass_kg: float, prop_diam_in: float, n_motors: int, capacity_mah: float, voltage_v: float,
                     fm: float = 0.6, eta: float = 0.75, usable: float = 0.8, rho: float = 1.225,
                     extra_power_w: float = 0.0) -> dict:
    """Momentum teorisiyle asılı kalma gücü ve uçuş süresi.

    P_ideal = T^1.5 / sqrt(2 ρ A),  P_elektrik = P_ideal / (FM · η) + P_ekstra
    FM: figure of merit (pervane verimi), η: motor + ESC verimi, usable: bataryanın kullanılabilir oranı.
    """
    thrust = mass_kg * G
    area = n_motors * np.pi * (prop_diam_in * 0.0254 / 2.0) ** 2
    p_ideal = thrust ** 1.5 / np.sqrt(2.0 * rho * area)
    p_el = p_ideal / (fm * eta) + extra_power_w
    energy_wh = capacity_mah / 1000.0 * voltage_v * usable
    return {"thrust_N": thrust, "disk_area_m2": float(area), "p_ideal_W": float(p_ideal), "p_electric_W": float(p_el),
            "energy_Wh": energy_wh, "minutes": float(energy_wh / p_el * 60.0),
            "disk_loading": float(thrust / area)}


def flight_time_vs_mass(masses_kg, **kw) -> np.ndarray:
    return np.array([quad_flight_time(m, **kw)["minutes"] for m in masses_kg])


def quad_roll_step(inertia: float = 0.012, kp: float = 0.3, kd: float = 0.06, step_deg: float = 10.0,
                   duration_s: float = 2.0, dt: float = 0.001, tau_max: float | None = None) -> dict:
    """Tek eksen (roll) dönme dinamiği için PD basamak yanıtı:  I·θ'' = τ,  τ = Kp(θref − θ) − Kd·θ'."""
    n = int(duration_s / dt)
    ref = np.deg2rad(step_deg)
    th = om = 0.0
    t = np.arange(n) * dt
    out = np.zeros(n)
    tau_log = np.zeros(n)
    for i in range(n):
        tau = kp * (ref - th) - kd * om
        if tau_max is not None:
            tau = float(np.clip(tau, -tau_max, tau_max))
        om += tau / inertia * dt
        th += om * dt
        out[i] = th
        tau_log[i] = tau
    deg = np.rad2deg(out)
    overshoot = max(0.0, (deg.max() - step_deg) / step_deg * 100.0)
    err = np.abs(deg - step_deg) > 0.02 * step_deg
    settle = float(t[np.where(err)[0][-1]] + dt) if err.any() else 0.0
    i10 = np.argmax(deg >= 0.1 * step_deg) if (deg >= 0.1 * step_deg).any() else None
    i90 = np.argmax(deg >= 0.9 * step_deg) if (deg >= 0.9 * step_deg).any() else None
    rise = float(t[i90] - t[i10]) if (i10 is not None and i90 is not None) else float("nan")
    zeta = kd / (2.0 * np.sqrt(kp * inertia)) if kp > 0 else float("inf")
    return {"t": t, "theta_deg": deg, "tau": tau_log, "ref_deg": step_deg, "overshoot_pct": float(overshoot),
            "settling_s": settle, "rise_s": rise, "zeta": float(zeta),
            "wn": float(np.sqrt(kp / inertia)) if kp > 0 else 0.0,
            "stable": bool(abs(deg[-1] - step_deg) < 0.05 * step_deg + 1e-9 and np.isfinite(deg).all())}


MOTOR_NAMES = ["Ön sol (FL)", "Ön sağ (FR)", "Arka sol (RL)", "Arka sağ (RR)"]


def quad_mix(throttle: float, roll: float, pitch: float, yaw: float) -> dict:
    """X şasi karıştırıcı (mixer). Girişler -1..1 / gaz 0..1.

    roll>0 : sağ taraf aşağı (sol motorlar artar)   pitch>0 : burun aşağı (arka motorlar artar)
    yaw>0  : saat yönünün tersi (FL ve RR motorları artar; bunlar saat yönünde dönen pervanelerdir)
    """
    raw = np.array([
        throttle + roll - pitch + yaw,   # FL
        throttle - roll - pitch - yaw,   # FR
        throttle + roll + pitch - yaw,   # RL
        throttle - roll + pitch + yaw,   # RR
    ])
    clipped = np.clip(raw, 0.0, 1.0)
    return {"names": MOTOR_NAMES, "raw": raw, "cmd": clipped, "saturated": bool(np.any(raw != clipped))}


# --------------------------------------------------------------------------
# 2) Paletli (skid-steer) robot
# --------------------------------------------------------------------------

def tracked_turn_state(v_l: float, v_r: float, track_width_cm: float, slip_factor: float = 1.2) -> dict:
    """Paletli robotun doğrusal / açısal hızı. Etkin iz genişliği = χ · B  (χ ≥ 1: kayma faktörü)."""
    b_eff = slip_factor * track_width_cm
    v = (v_l + v_r) / 2.0
    omega = (v_r - v_l) / b_eff
    radius = np.inf if abs(v_r - v_l) < 1e-9 else (b_eff / 2.0) * (v_r + v_l) / (v_r - v_l)
    return {"v": v, "omega": omega, "radius": radius, "b_eff": b_eff}


def tracked_resisting_moment(mass_kg: float, mu_lateral: float, track_length_cm: float) -> float:
    """Yerinde dönüşte zeminin direnç momenti (N·m):  M = μ · m · g · L / 4  (düzgün basınç dağılımı)."""
    return mu_lateral * mass_kg * G * (track_length_cm / 100.0) / 4.0


def pivot_turn_track_force(mass_kg: float, mu_lateral: float, track_length_cm: float, track_width_cm: float) -> float:
    """Yerinde dönüşte her paletin ürettiği (zıt yönlü) kuvvet (N):  F = M / B."""
    return tracked_resisting_moment(mass_kg, mu_lateral, track_length_cm) / (track_width_cm / 100.0)


def slope_thrust(mass_kg: float, mu_rolling: float, slope_deg: float) -> float:
    """Eğimde toplam itki ihtiyacı (N):  F = m g (μr cos α + sin α)."""
    a = np.deg2rad(slope_deg)
    return mass_kg * G * (mu_rolling * np.cos(a) + np.sin(a))


def sprocket_torque_Ncm(force_total_N: float, sprocket_radius_cm: float, n_tracks: int = 2) -> float:
    """Palet başına gereken tahrik dişlisi torku (N·cm)."""
    return force_total_N / n_tracks * sprocket_radius_cm


def traction_limit_deg(mu: float) -> float:
    """Kaymadan çıkılabilecek en dik eğim (yeterli tork varsayımıyla):  α = atan(μ)."""
    return float(np.rad2deg(np.arctan(mu)))


# --------------------------------------------------------------------------
# 3) Mars rover tipi 6 tekerlekli robot (rocker-bogie)
# --------------------------------------------------------------------------

def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def rocker_bogie_body_height(z_front, z_mid, z_rear):
    """Bir yandaki rocker pivot yüksekliği (eşit kol uzunluğu varsayımıyla ortalama kuralı).

    bogie pivotu = (orta + arka)/2 ;  rocker pivotu = (ön + bogie pivotu)/2
    """
    bogie = (np.asarray(z_mid) + np.asarray(z_rear)) / 2.0
    return (np.asarray(z_front) + bogie) / 2.0


def simulate_rocker_bogie_step(step_cm: float, wheel_d_cm: float, ramp_cm: float = 1.0, both_sides: bool = True,
                               n: int = 600) -> dict:
    """Basamak engelinin aşılması. Tekerlek konumları (tekerlek çapı D cinsinden, hologram oranları):
    ön +2.24 D, orta −0.26 D, arka −2.10 D. Tekerlek yüksekliği = zemin yüksekliği (nokta temas yaklaşımı)."""
    D = wheel_d_cm
    xf, xm, xr = 2.24 * D, -0.26 * D, -2.10 * D
    s = np.linspace(-xf - 2 * D, -xr + 2 * D, n)           # gövde merkezinin konumu; engel x=0'da
    ramp = max(ramp_cm, 1e-3)
    ter = lambda x: step_cm * smoothstep(np.asarray(x) / ramp)
    zf, zm, zr = ter(s + xf), ter(s + xm), ter(s + xr)
    left = rocker_bogie_body_height(zf, zm, zr)
    right = left if both_sides else np.zeros_like(left)
    body = (left + right) / 2.0
    ratio = step_cm / D
    status = "kolay" if ratio <= 1.0 else ("sınırda" if ratio <= 1.5 else "aşılamaz")
    return {"s": s, "z_front": zf, "z_mid": zm, "z_rear": zr, "pivot_left": left, "pivot_right": right,
            "body": body, "ratio": ratio, "status": status, "final_rise": float(body[-1])}


def tipover_angles(track_cm: float, wheelbase_cm: float, cg_height_cm: float) -> dict:
    """Statik devrilme eşikleri (derece): yanal = atan((iz/2)/h), boyuna = atan((dingil mesafesi/2)/h)."""
    return {"lateral": float(np.rad2deg(np.arctan((track_cm / 2.0) / cg_height_cm))),
            "longitudinal": float(np.rad2deg(np.arctan((wheelbase_cm / 2.0) / cg_height_cm)))}
