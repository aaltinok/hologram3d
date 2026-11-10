"""Plotly grafikleri (karanlık, bilimsel tema)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from . import kinematics as K

CYAN, AMB, GRN, RED, VIO = "#8fd0ff", "#ffd166", "#7cf5c1", "#ff8aa0", "#b7a6ff"


def _style(fig: go.Figure, title: str | None = None, h: int = 420, equal: bool = False) -> go.Figure:
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,45,110,.55)",
        font=dict(family="monospace", color="#cdf"), height=h,
        title=dict(text=title, font=dict(size=14)) if title else None,
        margin=dict(l=10, r=10, t=44 if title else 12, b=10),
        legend=dict(orientation="h", y=-0.18),
    )
    fig.update_xaxes(gridcolor="#2a5aa8", zerolinecolor="#4a7fcf")
    fig.update_yaxes(gridcolor="#2a5aa8", zerolinecolor="#4a7fcf")
    if equal:
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


# ---- Robot araba ----------------------------------------------------------
def fig_diff_drive(tr: dict) -> go.Figure:
    f = go.Figure()
    f.add_trace(go.Scatter(x=tr["x"], y=tr["y"], mode="lines", name="Yörünge", line=dict(color=CYAN, width=3)))
    f.add_trace(go.Scatter(x=[tr["x"][0]], y=[tr["y"][0]], mode="markers", name="Başlangıç",
                           marker=dict(color=GRN, size=11)))
    th = tr["theta"][-1]
    f.add_trace(go.Scatter(x=[tr["x"][-1]], y=[tr["y"][-1]], mode="markers", name="Bitiş",
                           marker=dict(color=AMB, size=13, symbol="arrow", angle=90 - np.degrees(th))))
    f.update_xaxes(title="x (cm)"); f.update_yaxes(title="y (cm)")
    return _style(f, "Sabit tekerlek hızlarında yörünge", 420, equal=True)


def fig_line_follow(res: dict, amp: float, wavelength: float) -> go.Figure:
    xs = np.linspace(min(0.0, res["x"].min()), max(res["x"].max(), 1.0), 600)
    f = go.Figure()
    f.add_trace(go.Scatter(x=xs, y=K.line_y(xs, amp, wavelength), name="Çizgi",
                           line=dict(color="#e8f9ff", width=9), opacity=0.35))
    f.add_trace(go.Scatter(x=res["x"], y=res["y"], name="Robot", line=dict(color=CYAN, width=2.5)))
    f.update_xaxes(title="x (cm)"); f.update_yaxes(title="y (cm)")
    return _style(f, "Çizgi ve robot yörüngesi", 360, equal=True)


def fig_cte(res: dict) -> go.Figure:
    f = go.Figure(go.Scatter(x=res["t"], y=res["cte"], line=dict(color=AMB, width=2), name="Yanal hata"))
    f.add_hline(y=0, line_color="#4a7fcf")
    f.update_xaxes(title="Zaman (s)"); f.update_yaxes(title="Yanal hata (cm)")
    return _style(f, "Çizgiden yanal sapma", 300)


# ---- Robot kol --------------------------------------------------------------
def fig_arm(pts: np.ndarray, ws: np.ndarray | None = None, target=None, title: str = "Düzlemsel 3R kol") -> go.Figure:
    f = go.Figure()
    if ws is not None:
        f.add_trace(go.Scattergl(x=ws[:, 0], y=ws[:, 1], mode="markers", name="Çalışma uzayı",
                                 marker=dict(color=CYAN, size=3, opacity=0.18)))
    f.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="lines+markers", name="Kol",
                           line=dict(color=AMB, width=6), marker=dict(size=10, color="#fff")))
    f.add_trace(go.Scatter(x=[pts[-1, 0]], y=[pts[-1, 1]], mode="markers", name="Uç nokta",
                           marker=dict(color=RED, size=14, symbol="x")))
    if target is not None:
        f.add_trace(go.Scatter(x=[target[0]], y=[target[1]], mode="markers", name="Hedef",
                               marker=dict(color=GRN, size=14, symbol="circle-open", line=dict(width=3))))
    f.update_xaxes(title="x: ileri erişim (cm)"); f.update_yaxes(title="z: yükseklik (cm)")
    return _style(f, title, 480, equal=True)


# ---- Altı bacaklı -------------------------------------------------------------
def fig_gait(phases, beta: float, name: str) -> go.Figure:
    f = go.Figure()
    seg = K.gait_segments(phases, beta)
    first_sw = first_st = True
    for i, leg in enumerate(K.LEGS):
        for c in (0, 1):  # iki döngü göster
            f.add_trace(go.Bar(y=[leg], x=[1.0], base=[c], orientation="h", marker_color=AMB, opacity=0.28,
                               name="Salınım (havada)", showlegend=first_sw, hoverinfo="skip"))
            first_sw = False
            for s, l in seg[i]:
                f.add_trace(go.Bar(y=[leg], x=[l], base=[c + s], orientation="h", marker_color=CYAN, opacity=0.9,
                                   name="Destek (yerde)", showlegend=first_st))
                first_st = False
    f.update_layout(barmode="overlay", bargap=0.25)
    f.update_yaxes(autorange="reversed")
    f.update_xaxes(title="Döngü fazı (2 döngü)", range=[0, 2], dtick=0.25)
    return _style(f, f"{name} yürüyüşü: ayak temas çizelgesi", 360)


def fig_support(phases, beta: float) -> go.Figure:
    n = 720
    tau = (np.arange(n) + 0.5) / n
    cnt = K.support_count(phases, beta, n)
    f = go.Figure(go.Scatter(x=tau, y=cnt, mode="lines", line=dict(color=GRN, width=3, shape="hv"), name="Yerdeki bacak"))
    f.add_hline(y=3, line_dash="dash", line_color=RED, annotation_text="statik kararlılık için ≥ 3")
    f.update_yaxes(title="Yerdeki bacak sayısı", range=[0, 6.5], dtick=1)
    f.update_xaxes(title="Döngü fazı τ")
    return _style(f, "Destek bacağı sayısı", 300)


def fig_foot(tr: dict) -> go.Figure:
    f = go.Figure(go.Scatter(x=tr["x"], y=tr["z"], mode="lines", line=dict(color=CYAN, width=3), name="Ayak yörüngesi"))
    f.update_xaxes(title="x: gövdeye göre ileri (cm)"); f.update_yaxes(title="z: yükseklik (cm)")
    return _style(f, "Bir döngüde ayak ucu yörüngesi", 300, equal=True)


# ---- Karşılaştırma -----------------------------------------------------------------
def fig_radar(axes, scores: dict) -> go.Figure:
    cols = [CYAN, AMB, GRN, RED, VIO, "#ff9a3a"]
    f = go.Figure()
    for (name, vals), c in zip(scores.items(), cols):
        f.add_trace(go.Scatterpolar(r=list(vals) + [vals[0]], theta=list(axes) + [axes[0]], fill="toself",
                                    name=name, line=dict(color=c), opacity=0.55))
    f.update_layout(polar=dict(bgcolor="rgba(10,45,110,.55)", radialaxis=dict(range=[0, 10], gridcolor="#2a5aa8"),
                               angularaxis=dict(gridcolor="#2a5aa8")))
    return _style(f, "Nitel karşılaştırma (öznel, 1–10)", 460)


def fig_actuators(rows) -> go.Figure:
    f = go.Figure(go.Bar(x=[r["Robot"] for r in rows], y=[r["Aktüatör sayısı"] for r in rows],
                         marker_color=[CYAN, AMB, GRN, RED, VIO, "#ff9a3a"][:len(rows)], text=[r["Aktüatör sayısı"] for r in rows], textposition="outside"))
    f.update_yaxes(title="Aktüatör sayısı")
    return _style(f, "Aktüatör sayısı", 360)


# ---- Quadcopter ----------------------------------------------------------------
def fig_step_response(res: dict) -> go.Figure:
    f = go.Figure()
    f.add_trace(go.Scatter(x=res["t"], y=[res["ref_deg"]] * len(res["t"]), name="Hedef",
                           line=dict(color=GRN, dash="dash", width=2)))
    f.add_trace(go.Scatter(x=res["t"], y=res["theta_deg"], name="Roll açısı", line=dict(color=CYAN, width=3)))
    f.update_xaxes(title="Zaman (s)"); f.update_yaxes(title="Roll açısı (°)")
    return _style(f, "Roll basamak yanıtı (PD kontrol)", 380)


def fig_flight_vs_mass(masses, minutes, m0: float, t0: float) -> go.Figure:
    f = go.Figure()
    f.add_trace(go.Scatter(x=masses, y=minutes, name="Uçuş süresi", line=dict(color=CYAN, width=3)))
    f.add_trace(go.Scatter(x=[m0], y=[t0], name="Seçili", mode="markers", marker=dict(color=AMB, size=13)))
    f.update_xaxes(title="Toplam kütle (kg)"); f.update_yaxes(title="Asılı kalma süresi (dk)", rangemode="tozero")
    return _style(f, "Kütle arttıkça uçuş süresi", 360)


# ---- Paletli tank --------------------------------------------------------------
def fig_torque(labels, required, available: float) -> go.Figure:
    f = go.Figure(go.Bar(x=list(labels), y=list(required), marker_color=[CYAN, AMB, GRN][:len(labels)],
                         text=[f"{v:.1f}" for v in required], textposition="outside"))
    f.add_hline(y=available, line_dash="dash", line_color=RED, annotation_text="kullanılabilir tork")
    f.update_yaxes(title="Palet başına tork (N·cm)", rangemode="tozero")
    return _style(f, "Gereken ve kullanılabilir tahrik torku", 380)


# ---- Mars rover ----------------------------------------------------------------
def fig_obstacle(res: dict) -> go.Figure:
    f = go.Figure()
    for key, name, c in [("z_front", "Ön tekerlek", CYAN), ("z_mid", "Orta tekerlek", GRN), ("z_rear", "Arka tekerlek", VIO)]:
        f.add_trace(go.Scatter(x=res["s"], y=res[key], name=name, line=dict(color=c, width=2, dash="dot")))
    f.add_trace(go.Scatter(x=res["s"], y=res["body"], name="Gövde", line=dict(color=AMB, width=4)))
    f.update_xaxes(title="Gövde konumu (cm); engel x = 0"); f.update_yaxes(title="Yükseklik (cm)")
    return _style(f, "Basamak engelinde tekerlek ve gövde yüksekliği", 400)


def fig_tipover(angles: dict, slip_deg: float, slope_deg: float) -> go.Figure:
    names = ["Yanal devrilme", "Boyuna devrilme", "Kayma (çekiş)"]
    vals = [angles["lateral"], angles["longitudinal"], slip_deg]
    f = go.Figure(go.Bar(x=names, y=vals, marker_color=[CYAN, AMB, GRN], text=[f"{v:.0f}°" for v in vals],
                         textposition="outside"))
    f.add_hline(y=slope_deg, line_dash="dash", line_color=RED, annotation_text="yamaç eğimi")
    f.update_yaxes(title="Eşik açı (°)", rangemode="tozero")
    return _style(f, "Statik eşik açılar", 380)


# ---- Rover direksiyon şeması -------------------------------------------------------
def fig_rover_steering(angles, track: float, df: float, dr: float, radius: float) -> go.Figure:
    pos = [(-track / 2, df), (track / 2, df), (-track / 2, 0), (track / 2, 0), (-track / 2, -dr), (track / 2, -dr)]
    f = go.Figure()
    f.add_trace(go.Scatter(x=[-track / 2, track / 2, track / 2, -track / 2, -track / 2],
                           y=[df, df, -dr, -dr, df], mode="lines", name="Gövde çerçevesi", line=dict(color="#e8f3ff", width=2, dash="dot")))
    for i, ((x, y), a) in enumerate(zip(pos, angles)):
        s, c = np.sin(np.radians(a)), np.cos(np.radians(a))
        L = 0.17 * max(track, df + dr)
        f.add_trace(go.Scatter(x=[x - s * L, x + s * L], y=[y - c * L, y + c * L], mode="lines", showlegend=False,
                               line=dict(color=AMB if a != 0 else CYAN, width=9)))
    if np.isfinite(radius):
        f.add_trace(go.Scatter(x=[-radius], y=[0], mode="markers", name="Dönüş merkezi (ICC)",
                               marker=dict(color=RED, size=13, symbol="x")))
    f.update_xaxes(title="x (cm)"); f.update_yaxes(title="y (cm)")
    return _style(f, "Tekerlek yönleri (üstten görünüş)", 420, equal=True)
