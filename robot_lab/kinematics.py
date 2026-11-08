"""Üç robot için bilimsel hesaplamalar (saf NumPy, arayüzden bağımsız).

1) Tekerlekli robot : diferansiyel sürüş kinematiği ve P/PD çizgi izleme simülasyonu
2) Robot kol        : düzlemsel 3R ileri/ters kinematik, Jacobian, manipülabilite, çalışma uzayı
3) Altı bacaklı     : yürüyüş (gait) çizelgesi, kararlılık, ayak yörüngesi, hız
"""
from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------
# 1) Diferansiyel sürüşlü tekerlekli robot
# --------------------------------------------------------------------------

def rpm_to_rad_s(rpm: float) -> float:
    return rpm * 2.0 * np.pi / 60.0


def diff_drive_state(wheel_diameter_cm: float, track_cm: float, rpm_l: float, rpm_r: float) -> dict:
    """Tekerlek devirlerinden doğrusal hız, açısal hız ve dönüş yarıçapı.

    v = (vR + vL) / 2,  w = (vR - vL) / L,  R = (L/2) (vR + vL) / (vR - vL)
    """
    r = wheel_diameter_cm / 2.0
    v_l = r * rpm_to_rad_s(rpm_l)
    v_r = r * rpm_to_rad_s(rpm_r)
    v = (v_r + v_l) / 2.0
    omega = (v_r - v_l) / track_cm
    radius = np.inf if abs(v_r - v_l) < 1e-9 else (track_cm / 2.0) * (v_r + v_l) / (v_r - v_l)
    return {"v_l": v_l, "v_r": v_r, "v": v, "omega": omega, "radius": radius}


def simulate_diff_drive(v_l: float, v_r: float, track_cm: float, duration_s: float, n: int = 400) -> dict:
    """Sabit tekerlek hızları için tam (analitik) yörünge. Başlangıç: (0,0), yön +x."""
    t = np.linspace(0.0, duration_s, n)
    v = (v_r + v_l) / 2.0
    omega = (v_r - v_l) / track_cm
    if abs(omega) < 1e-9:
        x, y, th = v * t, np.zeros_like(t), np.zeros_like(t)
    else:
        th = omega * t
        x = (v / omega) * np.sin(th)
        y = (v / omega) * (1.0 - np.cos(th))
    return {"t": t, "x": x, "y": y, "theta": th}


def line_y(x, amp: float, wavelength: float):
    return amp * np.sin(2.0 * np.pi * np.asarray(x) / wavelength)


def line_slope(x, amp: float, wavelength: float):
    return amp * (2.0 * np.pi / wavelength) * np.cos(2.0 * np.pi * np.asarray(x) / wavelength)


def simulate_line_follower(
    kp: float = 3.0,
    kd: float = 0.0,
    v0: float = 15.0,
    track_cm: float = 12.0,
    lookahead_cm: float = 6.0,
    amp: float = 5.0,
    wavelength: float = 80.0,
    duration_s: float = 20.0,
    dt: float = 0.01,
    vmax: float = 30.0,
    n_sensors: int = 5,
    sensor_spacing: float = 1.6,
    line_width: float = 1.9,
) -> dict:
    """Sinüs şeklindeki çizgiyi izleyen robotun PD kontrol simülasyonu.

    Hata = çizgiyi gören sensörlerin yanal konumlarının ağırlıklı ortalaması (cm).
    u = Kp*e + Kd*de/dt ;  vL = v0 - u ,  vR = v0 + u   (e > 0 : çizgi solda)
    """
    n = int(duration_s / dt)
    s_pos = (np.arange(n_sensors) - (n_sensors - 1) / 2.0) * sensor_spacing
    x = y = th = 0.0
    y = float(line_y(0.0, amp, wavelength))  # çizgi üzerinde başla
    prev_err = 0.0
    last_err = 0.0
    ts, xs, ys, ths, ctes, errs, lost = [], [], [], [], [], [], []
    for i in range(n):
        sx = x + lookahead_cm * np.cos(th) - s_pos * np.sin(th)
        sy = y + lookahead_cm * np.sin(th) + s_pos * np.cos(th)
        dist = np.abs(sy - line_y(sx, amp, wavelength)) / np.sqrt(1.0 + line_slope(sx, amp, wavelength) ** 2)
        seen = dist < line_width / 2.0
        if seen.any():
            err = float((s_pos * seen).sum() / seen.sum())
            lost.append(0)
        else:
            err = last_err
            lost.append(1)
        last_err = err
        u = kp * err + kd * (err - prev_err) / dt
        prev_err = err
        v_l = float(np.clip(v0 - u, -vmax, vmax))
        v_r = float(np.clip(v0 + u, -vmax, vmax))
        v = (v_l + v_r) / 2.0
        w = (v_r - v_l) / track_cm
        th += w * dt
        x += v * np.cos(th) * dt
        y += v * np.sin(th) * dt
        cte = (y - float(line_y(x, amp, wavelength))) / np.sqrt(1.0 + float(line_slope(x, amp, wavelength)) ** 2)
        ts.append(i * dt); xs.append(x); ys.append(y); ths.append(th); ctes.append(cte); errs.append(err)
    cte_arr = np.array(ctes)
    return {
        "t": np.array(ts), "x": np.array(xs), "y": np.array(ys), "theta": np.array(ths),
        "cte": cte_arr, "sensor_err": np.array(errs), "lost": np.array(lost),
        "rms_cte": float(np.sqrt(np.mean(cte_arr ** 2))),
        "max_cte": float(np.max(np.abs(cte_arr))),
        "lost_ratio": float(np.mean(lost)),
        "distance": float(np.sum(np.hypot(np.diff(xs), np.diff(ys)))),
    }


# --------------------------------------------------------------------------
# 2) Düzlemsel 3R robot kol (x: ileri erişim, z: yükseklik)
# --------------------------------------------------------------------------

def planar_fk(lengths, q_deg) -> np.ndarray:
    """Eklem noktaları (n+1, 2). q1 yataydan (x ekseni) ölçülür, diğerleri göreli."""
    q = np.deg2rad(np.asarray(q_deg, dtype=float))
    a = np.cumsum(q)
    pts = [np.zeros(2)]
    for l, ang in zip(lengths, a):
        pts.append(pts[-1] + l * np.array([np.cos(ang), np.sin(ang)]))
    return np.array(pts)


def end_orientation_deg(q_deg) -> float:
    return float(np.sum(q_deg))


def jacobian(lengths, q_deg) -> np.ndarray:
    """2xN pozisyon Jacobian'ı."""
    a = np.cumsum(np.deg2rad(np.asarray(q_deg, dtype=float)))
    n = len(lengths)
    J = np.zeros((2, n))
    for i in range(n):
        J[0, i] = -sum(lengths[j] * np.sin(a[j]) for j in range(i, n))
        J[1, i] = sum(lengths[j] * np.cos(a[j]) for j in range(i, n))
    return J


def manipulability(lengths, q_deg) -> float:
    """Yoshikawa manipülabilite ölçüsü w = sqrt(det(J J^T)). 0'a yakın = tekillik."""
    J = jacobian(lengths, q_deg)
    return float(np.sqrt(max(np.linalg.det(J @ J.T), 0.0)))


def ik_planar_3r(target_xz, phi_deg: float, lengths, elbow_up: bool = True):
    """Uç nokta (x,z) ve uç yönelimi phi için analitik ters kinematik.

    Dönüş: [q1,q2,q3] (derece) ya da ulaşılamıyorsa None.
    """
    l1, l2, l3 = lengths
    phi = np.deg2rad(phi_deg)
    wx = target_xz[0] - l3 * np.cos(phi)
    wz = target_xz[1] - l3 * np.sin(phi)
    r2 = wx * wx + wz * wz
    c2 = (r2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    if abs(c2) > 1.0:
        return None
    q2 = -np.arccos(c2) if elbow_up else np.arccos(c2)
    q1 = np.arctan2(wz, wx) - np.arctan2(l2 * np.sin(q2), l1 + l2 * np.cos(q2))
    q3 = phi - q1 - q2
    return list(np.rad2deg([q1, q2, q3]))


def workspace(lengths, ranges_deg, n: int = 4000, seed: int = 0) -> np.ndarray:
    """Eklem sınırları içinde rastgele örnekleme ile erişilebilir uç noktalar (n,2)."""
    rng = np.random.default_rng(seed)
    q = np.column_stack([rng.uniform(lo, hi, n) for lo, hi in ranges_deg])
    a = np.cumsum(np.deg2rad(q), axis=1)
    ls = np.asarray(lengths)
    return np.column_stack([(ls * np.cos(a)).sum(axis=1), (ls * np.sin(a)).sum(axis=1)])


# --------------------------------------------------------------------------
# 3) Altı bacaklı robot yürüyüşü
# --------------------------------------------------------------------------

LEGS = ["R1 (ön sağ)", "R2 (orta sağ)", "R3 (arka sağ)", "L1 (ön sol)", "L2 (orta sol)", "L3 (arka sol)"]

GAITS = {
    "Tripod": {"beta": 0.5, "phase": [0, .5, 0, .5, 0, .5],
               "info": "Üç bacak havada, üç bacak yerde. En hızlı statik kararlı yürüyüş."},
    "Ripple": {"beta": 2 / 3, "phase": [2 / 3, 1 / 3, 0, 1 / 6, 5 / 6, .5],
               "info": "Dalga benzeri geçişler; her an en az 4 bacak yerde. Daha kararlı, daha yavaş."},
    "Wave": {"beta": 5 / 6, "phase": [2 / 6, 1 / 6, 0, 5 / 6, 4 / 6, 3 / 6],
             "info": "Bacaklar sırayla kalkar; her an 5 bacak yerde. En kararlı, en yavaş."},
}


def stance_mask(phase: float, beta: float, tau):
    """tau in [0,1): bacak yerde (destek fazı) ise True."""
    return ((np.asarray(tau) - phase) % 1.0) < beta


def gait_segments(phases, beta: float):
    """Her bacak için [0,1] döngüsünde destek fazı aralıkları: [(başlangıç, uzunluk), ...]."""
    out = []
    for p in phases:
        s = p % 1.0
        e = s + beta
        out.append([(s, beta)] if e <= 1.0 + 1e-12 else [(s, 1.0 - s), (0.0, e - 1.0)])
    return out


def support_count(phases, beta: float, n: int = 720) -> np.ndarray:
    tau = (np.arange(n) + 0.5) / n
    return np.sum([stance_mask(p, beta, tau) for p in phases], axis=0)


def gait_metrics(phases, beta: float) -> dict:
    cnt = support_count(phases, beta)
    return {"min_support": int(cnt.min()), "max_support": int(cnt.max()), "mean_support": float(cnt.mean()),
            "statically_stable": bool(cnt.min() >= 3)}


def foot_trajectory(stride_cm: float, lift_cm: float, beta: float, n: int = 400) -> dict:
    """Gövdeye göre ayak yörüngesi: destekte doğrusal geri, salınımda yarım sinüs ile kalkış."""
    tau = np.linspace(0.0, 1.0, n, endpoint=False)
    x = np.zeros(n)
    z = np.zeros(n)
    st = tau < beta
    x[st] = stride_cm / 2.0 - stride_cm * (tau[st] / beta)
    s = (tau[~st] - beta) / (1.0 - beta)
    x[~st] = -stride_cm / 2.0 + stride_cm * (0.5 - 0.5 * np.cos(np.pi * s))
    z[~st] = lift_cm * np.sin(np.pi * s)
    return {"tau": tau, "x": x, "z": z}


def body_speed(stride_cm: float, freq_hz: float) -> float:
    """Gövde hızı = adım uzunluğu x döngü frekansı (cm/s)."""
    return stride_cm * freq_hz
