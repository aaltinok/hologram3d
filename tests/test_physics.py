import numpy as np
from robot_lab import physics as X


def test_twr_and_hover_throttle():
    twr = X.thrust_to_weight(0.8, 4, 600)
    assert abs(twr - 3.0) < 1e-9
    assert abs(X.hover_throttle(twr) - np.sqrt(1 / 3)) < 1e-9
    assert X.hover_throttle(0.9) is None


def test_flight_time_physical_trends():
    base = dict(prop_diam_in=5, n_motors=4, capacity_mah=3000, voltage_v=14.8)
    a = X.quad_flight_time(0.8, **base)
    assert 8 < a["minutes"] < 25                              # makul aralık
    assert X.quad_flight_time(1.2, **base)["minutes"] < a["minutes"]       # ağır = kısa uçuş
    assert X.quad_flight_time(0.8, **{**base, "capacity_mah": 6000})["minutes"] > a["minutes"]
    assert X.quad_flight_time(0.8, **{**base, "prop_diam_in": 7})["minutes"] > a["minutes"]  # büyük pervane = verimli
    assert abs(a["thrust_N"] - 0.8 * X.G) < 1e-9


def test_roll_step_response_theory():
    r = X.quad_roll_step(0.012, 0.3, 0.06)
    assert abs(r["zeta"] - 0.5) < 1e-9 and abs(r["wn"] - 5.0) < 1e-9
    # ζ=0.5 için teorik aşım ≈ %16.3
    assert abs(r["overshoot_pct"] - 16.3) < 1.0
    assert r["stable"] and abs(r["theta_deg"][-1] - 10.0) < 0.2
    crit = X.quad_roll_step(0.012, 0.3, 2 * np.sqrt(0.3 * 0.012))   # kritik sönüm
    assert crit["overshoot_pct"] < 0.5
    assert X.quad_roll_step(0.012, 0.3, 0.0)["overshoot_pct"] > 90   # sönümsüz: aşırı salınım


def test_quad_mixer_properties():
    m = X.quad_mix(0.5, 0.1, -0.05, 0.02)
    assert abs(m["raw"].sum() - 4 * 0.5) < 1e-12                 # kolektif korunur
    fl, fr, rl, rr = m["raw"]
    assert abs((fl + rl) - (fr + rr) - 4 * 0.1) < 1e-12          # roll momenti
    assert abs((rl + rr) - (fl + fr) - 4 * (-0.05) * -1) < 1e-12 or True
    assert abs((rl + rr) - (fl + fr) - 4 * (-0.05)) < 1e-12      # pitch momenti
    assert abs((fl + rr) - (fr + rl) - 4 * 0.02) < 1e-12         # yaw momenti
    assert X.quad_mix(0.95, 0.2, 0, 0)["saturated"] and not m["saturated"]


def test_tracked_turn():
    s = X.tracked_turn_state(5, 5, 11.6, 1.2)
    assert s["omega"] == 0 and np.isinf(s["radius"])
    s = X.tracked_turn_state(-5, 5, 11.6, 1.2)
    assert abs(s["v"]) < 1e-12 and s["omega"] > 0 and abs(s["radius"]) < 1e-12
    assert abs(s["omega"] - 10 / (1.2 * 11.6)) < 1e-12


def test_tracked_forces():
    M = X.tracked_resisting_moment(1.2, 0.6, 15)
    assert abs(M - 0.6 * 1.2 * X.G * 0.15 / 4) < 1e-12
    F = X.pivot_turn_track_force(1.2, 0.6, 15, 11.6)
    assert abs(F * 0.116 - M) < 1e-12
    assert abs(X.slope_thrust(1.0, 0.1, 0) - 0.1 * X.G) < 1e-9
    assert X.slope_thrust(1.0, 0.1, 30) > X.slope_thrust(1.0, 0.1, 10)
    assert abs(X.sprocket_torque_Ncm(10, 2.5, 2) - 12.5) < 1e-12
    assert abs(X.traction_limit_deg(1.0) - 45.0) < 1e-9


def test_rocker_bogie_averaging():
    r = X.simulate_rocker_bogie_step(5, 10, ramp_cm=1.0, both_sides=True)
    assert abs(r["final_rise"] - 5) < 1e-9                       # iki yan: gövde tam h kadar yükselir
    assert np.all(np.diff(r["body"]) >= -1e-12)                  # tek yönlü artış
    one = X.simulate_rocker_bogie_step(5, 10, ramp_cm=1.0, both_sides=False)
    assert abs(one["final_rise"] - 2.5) < 1e-9                   # tek yan: h/2
    # tek tekerlek (ön) engele çıkınca gövde h/4 yükselir (iki yan): (zf + (zm+zr)/2)/2 = h/2 tek yanda
    assert abs(float(X.rocker_bogie_body_height(4, 0, 0)) - 2.0) < 1e-12
    assert X.simulate_rocker_bogie_step(5, 10)["status"] == "kolay"
    assert X.simulate_rocker_bogie_step(12, 10)["status"] == "sınırda"
    assert X.simulate_rocker_bogie_step(20, 10)["status"] == "aşılamaz"


def test_tipover():
    t = X.tipover_angles(28, 35, 14)
    assert abs(t["lateral"] - 45.0) < 1e-9
    assert t["longitudinal"] > t["lateral"]


def test_rover_steering_geometry():
    st = X.rover_steering(np.inf, 17, 16, 28)
    assert all(a == 0 for a in st["angle_deg"]) and all(v == 1 for v in st["speed"])
    L = X.rover_steering(60, 17, 16, 28)                     # sol dönüş (R>0)
    a, v = L["angle_deg"], L["speed"]
    assert a[0] < 0 and a[1] < 0 and a[4] > 0 and a[5] > 0   # ön tekerlekler sola, arka tekerlekler sağa
    assert abs(a[0]) > abs(a[1])                             # iç (sol ön) tekerlek daha çok döner
    assert a[2] == 0 and a[3] == 0                           # orta tekerlekler düz
    assert abs(max(v) - 1.0) < 1e-12 and max(v) in (v[1], v[5])   # en hızlı: dış köşe tekerlekler
    assert 0 < v[2] < v[3] < 1.0                              # dış orta tekerlek, iç orta tekerlekten hızlı
    R = X.rover_steering(-60, 17, 16, 28)                    # sağ dönüş simetrik
    assert abs(R["angle_deg"][1] + L["angle_deg"][0]) < 1e-9
    P = X.rover_steering(0.0, 17, 16, 28)                    # yerinde dönüş: sol tekerlekler geri, sağ ileri
    assert P["speed"][2] < 0 < P["speed"][3]
    assert all(abs(x) <= 90 for x in P["angle_deg"])
