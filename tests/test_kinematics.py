import numpy as np
from robot_lab import kinematics as K


def test_diff_drive_straight_and_spin():
    s = K.diff_drive_state(6.5, 12.0, 100, 100)
    assert s["omega"] == 0 and np.isinf(s["radius"]) and s["v"] > 0
    s = K.diff_drive_state(6.5, 12.0, -100, 100)
    assert abs(s["v"]) < 1e-9 and s["omega"] > 0 and abs(s["radius"]) < 1e-9


def test_diff_drive_circle_closes():
    s = K.diff_drive_state(6.5, 12.0, 100, 150)
    T = 2 * np.pi / s["omega"]
    tr = K.simulate_diff_drive(s["v_l"], s["v_r"], 12.0, T, n=1000)
    assert abs(tr["x"][-1]) < 1e-6 and abs(tr["y"][-1]) < 1e-6
    assert abs(np.max(tr["y"]) - 2 * s["radius"]) < 0.05


def test_fk_ik_roundtrip():
    L = [10, 9, 7]
    for q in ([60, -40, 20], [90, -90, 0], [30, 50, -30]):
        pts = K.planar_fk(L, q)
        phi = K.end_orientation_deg(q)
        for up in (True, False):
            sol = K.ik_planar_3r(pts[-1], phi, L, elbow_up=up)
            assert sol is not None
            assert np.allclose(K.planar_fk(L, sol)[-1], pts[-1], atol=1e-6)


def test_ik_unreachable():
    assert K.ik_planar_3r([100, 100], 0, [10, 9, 7]) is None


def test_jacobian_numeric():
    L, q = [10, 9, 7], np.array([50.0, -30.0, 15.0])
    J = K.jacobian(L, q)
    eps = 1e-6
    for i in range(3):
        dq = q.copy(); dq[i] += eps
        num = (K.planar_fk(L, dq)[-1] - K.planar_fk(L, q)[-1]) / np.deg2rad(eps)
        assert np.allclose(J[:, i], num, atol=1e-3)


def test_singularity_manipulability():
    L = [10, 9, 7]
    assert K.manipulability(L, [45, 0, 0]) < 1e-6        # tam uzanmış kol = tekillik
    assert K.manipulability(L, [45, -80, 40]) > 1.0


def test_workspace_bounds():
    L = [10, 9, 7]
    pts = K.workspace(L, [(0, 180), (-150, 150), (-120, 120)], 2000)
    assert pts.shape == (2000, 2) and np.hypot(pts[:, 0], pts[:, 1]).max() <= sum(L) + 1e-9


def test_gaits():
    m = {g: K.gait_metrics(v["phase"], v["beta"]) for g, v in K.GAITS.items()}
    assert m["Tripod"]["min_support"] == 3 and m["Tripod"]["max_support"] == 3
    assert m["Ripple"]["min_support"] >= 3
    assert m["Wave"]["min_support"] == 5
    for g, v in K.GAITS.items():
        seg = K.gait_segments(v["phase"], v["beta"])
        assert all(abs(sum(l for _, l in s) - v["beta"]) < 1e-9 for s in seg)


def test_foot_trajectory_and_speed():
    tr = K.foot_trajectory(4.0, 2.0, 0.5)
    assert abs(tr["x"].max() - 2.0) < 0.05 and abs(tr["z"].max() - 2.0) < 0.05
    assert K.body_speed(4.0, 1.5) == 6.0


def test_line_follower_default_tracks():
    r = K.simulate_line_follower()
    assert r["rms_cte"] < 2.0 and r["lost_ratio"] < 0.05
    bad = K.simulate_line_follower(kp=0.0)       # kontrolsüz: çizgiden çıkmalı
    assert bad["rms_cte"] > r["rms_cte"]
