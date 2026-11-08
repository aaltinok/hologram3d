"""MERAL Robotik Kulübü - 3D Robot Hologram Laboratuvarı (Streamlit)

Çalıştırma:  streamlit run app.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from robot_lab import __version__
from robot_lab import kinematics as K
from robot_lab import physics as X
from robot_lab import plots as P
from robot_lab.data import (COMPARE_ROWS, RADAR_AXES, RADAR_SCORES, ROBOTS, parts_df)
from robot_lab.ui import footer, header, holo, inject_css, show_df, show_fig

st.set_page_config(page_title="MERAL · 3D Robot Hologram Laboratuvarı", page_icon="🤖", layout="wide",
                   initial_sidebar_state="expanded")
inject_css()
header()

# ----------------------------------------------------------------------------- Kenar çubuğu
with st.sidebar:
    st.markdown("### ⚙️ Görünüm")
    HEIGHT = st.slider("Hologram yüksekliği (px)", 520, 1000, 760, 20)
    st.markdown("### 🕹️ Hologram kontrolleri")
    st.markdown(
        "- **Sürükle:** robotu istediğin açıdan çevir\n"
        "- **Parça düğmeleri:** parçayı vurgula ve tanıtımını oku\n"
        "- **TÜMÜ:** serbest 360° görünüme dön\n"
        "- **TEL KAFES:** dolu / tel kafes görünüm\n"
        "- **DÖNÜŞ / HAREKET / YÜRÜ:** animasyonları durdur-başlat"
    )
    st.info("Hologramlar three.js'i internetten (CDN) yükler; ilk açılışta bağlantı gerekir.", icon="🌐")
    st.caption(f"Sürüm {__version__} · MERAL Robotik Kulübü")

NAV = ["🔭 Genel Bakış", "🚗 Robot Araba", "🦾 Robot Kol", "🕷️ Altı Bacaklı", "🚁 Quadcopter", "🚜 Paletli Tank",
       "🪐 Mars Rover", "📊 Karşılaştırma", "ℹ️ Hakkında"]
# Yalnızca seçili bölüm çizilir: gizli sekmelerde gereksiz WebGL hologramları çalışmaz.
view = st.radio("Bölüm", NAV, horizontal=True, label_visibility="collapsed")
sim_line = st.cache_data(show_spinner=False)(K.simulate_line_follower)
sim_roll = st.cache_data(show_spinner=False)(X.quad_roll_step)


def robot_panel(key: str) -> None:
    """Sol: hologram, sağ: açıklama + metrikler + parça tablosu."""
    r = ROBOTS[key]
    c1, c2 = st.columns([3, 2], gap="medium")
    with c1:
        holo(key, HEIGHT)
    with c2:
        st.subheader(f"{r['emoji']} {r['ad']}")
        st.write(r["ozet"])
        for col, (lab, val) in zip(st.columns(len(r["metrikler"])), r["metrikler"]):
            col.metric(lab, val)
        st.markdown("**Parça kataloğu**")
        show_df(parts_df(key))


# ----------------------------------------------------------------------------- 1) Genel bakış
if view == NAV[0]:
    st.markdown("Robotları tek ekranda inceleyin. Her hologram bağımsızdır; parçalara dokunarak tanıtımlarını okuyabilirsiniz.")
    more = st.checkbox("Yeni robotları da göster (Quadcopter, Paletli Tank, Mars Rover)", value=True)
    rows = [["araba", "kol", "hexapod"], ["quad", "tank", "rover"]]
    for row in rows[: 2 if more else 1]:
        for col, key in zip(st.columns(3, gap="small"), row):
            with col:
                r = ROBOTS[key]
                st.markdown(f"#### {r['emoji']} {r['ad']}")
                holo(key, HEIGHT)
                st.caption(r["ozet"])

# ----------------------------------------------------------------------------- 2) Robot araba
if view == NAV[1]:
    robot_panel("araba")
    st.divider()
    st.header("🔬 Bilimsel analiz")
    t1, t2 = st.tabs(["Diferansiyel sürüş kinematiği", "Çizgi izleme (PD kontrol) simülasyonu"])

    with t1:
        st.markdown('<div class="formula">v = (v<sub>R</sub> + v<sub>L</sub>)/2 &nbsp;·&nbsp; ω = (v<sub>R</sub> − v<sub>L</sub>)/L '
                    '&nbsp;·&nbsp; R = (L/2)(v<sub>R</sub> + v<sub>L</sub>)/(v<sub>R</sub> − v<sub>L</sub>)</div>', unsafe_allow_html=True)
        a, b = st.columns(2)
        with a:
            dia = st.slider("Tekerlek çapı (cm)", 3.0, 12.0, 6.5, 0.1, key="dd_dia")
            track = st.slider("Tekerlek aralığı L (cm) — tahmini", 6.0, 25.0, 12.0, 0.5, key="dd_track")
            dur = st.slider("Süre (s)", 1, 30, 10, key="dd_dur")
        with b:
            rl = st.slider("Sol tekerlek (devir/dk)", -250, 250, 120, 5, key="dd_rl")
            rr = st.slider("Sağ tekerlek (devir/dk)", -250, 250, 150, 5, key="dd_rr")
        s = K.diff_drive_state(dia, track, rl, rr)
        tr = K.simulate_diff_drive(s["v_l"], s["v_r"], track, dur)
        m = st.columns(4)
        m[0].metric("Doğrusal hız v", f"{s['v']:.1f} cm/s")
        m[1].metric("Açısal hız ω", f"{np.degrees(s['omega']):.1f} °/s")
        m[2].metric("Dönüş yarıçapı R", "∞ (düz)" if np.isinf(s["radius"]) else f"{abs(s['radius']):.1f} cm")
        m[3].metric("Alınan yol", f"{abs(s['v']) * dur:.0f} cm")
        if abs(s["v"]) < 1e-9 and abs(s["omega"]) > 0:
            st.info("Tekerlekler zıt yönde ve eşit hızda: robot olduğu yerde dönüyor (pivot dönüşü).")
        show_fig(P.fig_diff_drive(tr))

    with t2:
        st.markdown("Robot, **sinüs biçimli bir çizgiyi** 5 kanallı IR dizisiyle izler. Hata, çizgiyi gören sensörlerin "
                    "yanal konumlarının ağırlıklı ortalamasıdır; **u = Kp·e + Kd·de/dt**, **v<sub>L</sub> = v₀ − u**, "
                    "**v<sub>R</sub> = v₀ + u**.", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            kp = st.slider("Kp", 0.0, 10.0, 3.0, 0.1, key="lf_kp")
            kd = st.slider("Kd", 0.0, 1.0, 0.0, 0.01, key="lf_kd")
            v0 = st.slider("Temel hız v₀ (cm/s)", 5.0, 30.0, 15.0, 0.5, key="lf_v0")
        with b:
            look = st.slider("Sensör öne uzaklığı (cm)", 2.0, 12.0, 6.0, 0.5, key="lf_look")
            lft = st.slider("Tekerlek aralığı L (cm)", 6.0, 25.0, 12.0, 0.5, key="lf_L")
            dur2 = st.slider("Süre (s)", 10, 40, 20, key="lf_dur")
        with c:
            amp = st.slider("Çizgi genliği (cm)", 1.0, 10.0, 5.0, 0.5, key="lf_amp")
            wl = st.slider("Çizgi dalga boyu (cm)", 40.0, 160.0, 80.0, 5.0, key="lf_wl")
        res = sim_line(kp=kp, kd=kd, v0=v0, track_cm=lft, lookahead_cm=look, amp=amp, wavelength=wl, duration_s=float(dur2))
        m = st.columns(4)
        m[0].metric("RMS yanal hata", f"{res['rms_cte']:.2f} cm")
        m[1].metric("Maks. yanal hata", f"{res['max_cte']:.2f} cm")
        m[2].metric("Çizgi kaybı", f"%{100 * res['lost_ratio']:.1f}")
        m[3].metric("Alınan yol", f"{res['distance']:.0f} cm")
        if res["lost_ratio"] > 0.2:
            st.warning("Robot çizgiyi sık kaybediyor: hızı düşürmeyi, Kp'yi ayarlamayı veya Kd eklemeyi deneyin.")
        show_fig(P.fig_line_follow(res, amp, wl))
        show_fig(P.fig_cte(res))
        st.caption("Varsayımlar: sensör aralığı 1,6 cm, çizgi genişliği 1,9 cm, tekerlek hız sınırı ±30 cm/s. "
                   "Gerçek robotta sensör yerleşimi ve motor dinamikleri farklı olabilir.")

# ----------------------------------------------------------------------------- 3) Robot kol
if view == NAV[2]:
    robot_panel("kol")
    st.divider()
    st.header("🔬 Bilimsel analiz")
    st.markdown("Kolun düzlemdeki (yan görünüş) **3R modeli**: q₁ yataydan ölçülür, q₂ ve q₃ göreli açılardır. "
                "Uç nokta: **p = Σ lᵢ·[cos θᵢ, sin θᵢ]**, θᵢ = q₁ + … + qᵢ. Manipülabilite: **w = √det(J·Jᵀ)**.")
    t1, t2 = st.tabs(["İleri kinematik + çalışma uzayı", "Ters kinematik"])
    with t1:
        a, b = st.columns(2)
        with a:
            l1 = st.slider("Üst kol l₁ (cm) — tahmini", 5.0, 20.0, 10.0, 0.5, key="fk_l1")
            l2 = st.slider("Ön kol l₂ (cm) — tahmini", 5.0, 20.0, 9.0, 0.5, key="fk_l2")
            l3 = st.slider("Bilek + tutucu l₃ (cm) — tahmini", 3.0, 15.0, 7.0, 0.5, key="fk_l3")
        with b:
            q1 = st.slider("q₁ omuz (°)", 0, 180, 70, key="fk_q1")
            q2 = st.slider("q₂ dirsek (°)", -150, 150, -50, key="fk_q2")
            q3 = st.slider("q₃ bilek (°)", -120, 120, 20, key="fk_q3")
        L, q = [l1, l2, l3], [q1, q2, q3]
        pts = K.planar_fk(L, q)
        w = K.manipulability(L, q)
        m = st.columns(4)
        m[0].metric("Uç nokta x", f"{pts[-1, 0]:.1f} cm")
        m[1].metric("Uç nokta z", f"{pts[-1, 1]:.1f} cm")
        m[2].metric("Uç yönelimi φ", f"{K.end_orientation_deg(q):.0f}°")
        m[3].metric("Manipülabilite w", f"{w:.1f}")
        if w < 0.05 * (l1 * l2):
            st.warning("Tekilliğe çok yakın: kol bu konfigürasyonda bazı yönlerde hareket üretemez.")
        ws = K.workspace(L, [(0, 180), (-150, 150), (-120, 120)], 4000)
        show_fig(P.fig_arm(pts, ws, title="Kol konfigürasyonu ve erişilebilir çalışma uzayı"))
        st.caption("Çalışma uzayı, eklem sınırları içinde 4000 rastgele konfigürasyondan hesaplanır "
                   "(q₁: 0–180°, q₂: ±150°, q₃: ±120°; varsayım).")
    with t2:
        a, b = st.columns(2)
        with a:
            tx = st.slider("Hedef x (cm)", 0.0, 30.0, 14.0, 0.5, key="ik_x")
            tz = st.slider("Hedef z (cm)", -5.0, 30.0, 12.0, 0.5, key="ik_z")
        with b:
            phi = st.slider("İstenen uç yönelimi φ (°)", -90, 90, 0, key="ik_phi")
            elbow = st.radio("Dirsek konumu", ["Yukarı", "Aşağı"], horizontal=True, key="ik_elbow")
        Li = [l1, l2, l3]
        sol = K.ik_planar_3r([tx, tz], phi, Li, elbow_up=(elbow == "Yukarı"))
        if sol is None:
            st.error("Hedef noktaya bu yönelimle ulaşılamıyor (kolun erişimi dışında).")
        else:
            m = st.columns(3)
            for col, (nm, v) in zip(m, zip(["q₁ omuz", "q₂ dirsek", "q₃ bilek"], sol)):
                col.metric(nm, f"{v:.1f}°")
            ok = all(lo <= v <= hi for v, (lo, hi) in zip(sol, [(0, 180), (-150, 150), (-120, 120)]))
            if not ok:
                st.warning("Çözüm matematiksel olarak var, fakat varsayılan eklem sınırlarının dışında kalıyor.")
            show_fig(P.fig_arm(K.planar_fk(Li, sol), None, target=[tx, tz], title="Ters kinematik çözümü"))
        st.caption("Kol uzunlukları, 'İleri kinematik' sekmesindeki kaydırıcılardan alınır.")

# ----------------------------------------------------------------------------- 4) Altı bacaklı
if view == NAV[3]:
    robot_panel("hexapod")
    st.divider()
    st.header("🔬 Bilimsel analiz: yürüyüş (gait) analizi")
    st.markdown("Her bacak bir döngüde **destek (yerde)** ve **salınım (havada)** fazından geçer. "
                "β (duty factor) destek fazının oranıdır. Gövde hızı: **v = adım uzunluğu × döngü frekansı**.")
    a, b = st.columns(2)
    with a:
        gname = st.selectbox("Yürüyüş tipi", list(K.GAITS) + ["Özel β (tripod fazları)"], key="g_name")
        if gname in K.GAITS:
            g = K.GAITS[gname]
            beta, phases = g["beta"], g["phase"]
            st.caption(g["info"])
        else:
            beta = st.slider("β (duty factor)", 0.5, 0.95, 0.6, 0.01, key="g_beta")
            phases = K.GAITS["Tripod"]["phase"]
            st.caption("Tripod fazları sabit; β > 0,5 olduğunda bacak grupları çakışır ve destek sayısı artar.")
    with b:
        stride = st.slider("Adım uzunluğu (cm)", 1.0, 10.0, 4.0, 0.5, key="g_stride")
        freq = st.slider("Döngü frekansı (Hz)", 0.2, 3.0, 1.2, 0.1, key="g_freq")
        lift = st.slider("Ayak kaldırma yüksekliği (cm)", 0.5, 4.0, 2.0, 0.5, key="g_lift")
    gm = K.gait_metrics(phases, beta)
    m = st.columns(4)
    m[0].metric("Duty factor β", f"{beta:.2f}")
    m[1].metric("Yerdeki bacak (min / ort.)", f"{gm['min_support']} / {gm['mean_support']:.1f}")
    m[2].metric("Statik kararlılık", "Evet ✅" if gm["statically_stable"] else "Hayır ⚠️")
    m[3].metric("Gövde hızı", f"{K.body_speed(stride, freq):.1f} cm/s")
    show_fig(P.fig_gait(phases, beta, gname.split(" ")[0]))
    c1, c2 = st.columns(2)
    with c1:
        show_fig(P.fig_support(phases, beta))
    with c2:
        show_fig(P.fig_foot(K.foot_trajectory(stride, lift, beta)))
    st.caption("Bacak sırası: R1/R2/R3 sağ ön/orta/arka, L1/L2/L3 sol ön/orta/arka. "
               "Tripod yürüyüşte her an tam 3 bacak yerdedir; bu, statik kararlılığın alt sınırıdır.")

# ----------------------------------------------------------------------------- 5) Quadcopter
if view == NAV[4]:
    robot_panel("quad")
    st.divider()
    st.header("🔬 Bilimsel analiz")
    t1, t2, t3 = st.tabs(["İtki ve uçuş süresi", "Yatış (roll) PD kontrolü", "Motor karıştırıcı (mixer)"])

    with t1:
        st.markdown('<div class="formula">TWR = n·T<sub>max</sub> / (m·g) &nbsp;·&nbsp; gaz<sub>asılı</sub> ≈ √(1/TWR) &nbsp;·&nbsp; '
                    'P<sub>ideal</sub> = T<sup>3/2</sup> / √(2ρA) &nbsp;·&nbsp; P<sub>elk</sub> = P<sub>ideal</sub> / (FM·η)</div>',
                    unsafe_allow_html=True)
        a1, b1 = st.columns(2)
        with a1:
            mass = st.slider("Toplam kütle (kg)", 0.2, 3.0, 0.8, 0.05, key="q_mass")
            prop = st.slider("Pervane çapı (inç)", 3.0, 10.0, 5.0, 0.5, key="q_prop")
            tmax = st.slider("Motor başına maks. itki (g)", 200, 2000, 600, 50, key="q_tmax")
        with b1:
            cap = st.slider("Batarya kapasitesi (mAh)", 500, 8000, 3000, 100, key="q_cap")
            volt = st.slider("Batarya gerilimi (V)", 7.4, 25.2, 14.8, 0.1, key="q_volt")
            extra = st.slider("Ekstra güç: kamera, elektronik (W)", 0.0, 30.0, 5.0, 0.5, key="q_extra")
        twr = X.thrust_to_weight(mass, 4, tmax)
        thr = X.hover_throttle(twr)
        ft = X.quad_flight_time(mass, prop, 4, cap, volt, extra_power_w=extra)
        m = st.columns(4)
        m[0].metric("İtki/ağırlık (TWR)", f"{twr:.2f}")
        m[1].metric("Asılı kalma gazı", "—" if thr is None else f"%{100 * thr:.0f}")
        m[2].metric("Elektrik gücü", f"{ft['p_electric_W']:.0f} W")
        m[3].metric("Asılı kalma süresi", f"{ft['minutes']:.1f} dk")
        if thr is None:
            st.error("TWR < 1: itki ağırlığı karşılamıyor, araç havalanamaz.")
        elif twr < 2:
            st.warning("TWR < 2: manevra ve rüzgâr için itki payı az.")
        masses = np.linspace(0.2, 3.0, 40)
        mins = X.flight_time_vs_mass(masses, prop_diam_in=prop, n_motors=4, capacity_mah=cap, voltage_v=volt,
                                     extra_power_w=extra)
        show_fig(P.fig_flight_vs_mass(masses, mins, mass, ft["minutes"]))
        st.caption("Varsayımlar: FM = 0,60, motor + ESC verimi = %75, bataryanın %80'i kullanılır, havanın yoğunluğu 1,225 kg/m³. "
                   "Sonuç asılı kalma içindir; ileri uçuş ve rüzgâr süreyi değiştirir.")

    with t2:
        st.markdown('<div class="formula">I·θ″ = τ &nbsp;·&nbsp; τ = K<sub>p</sub>(θ<sub>ref</sub> − θ) − K<sub>d</sub>·θ′ '
                    '&nbsp;·&nbsp; ω<sub>n</sub> = √(K<sub>p</sub>/I) &nbsp;·&nbsp; ζ = K<sub>d</sub>/(2√(K<sub>p</sub>I))</div>',
                    unsafe_allow_html=True)
        a2, b2 = st.columns(2)
        with a2:
            inert = st.slider("Eylemsizlik momenti I (kg·m²)", 0.002, 0.05, 0.012, 0.001, key="r_I", format="%.3f")
            kpr = st.slider("Kp (N·m/rad)", 0.05, 2.0, 0.3, 0.05, key="r_kp")
            kdr = st.slider("Kd (N·m·s/rad)", 0.0, 0.5, 0.06, 0.01, key="r_kd")
        with b2:
            stp = st.slider("Basamak girişi (°)", 5, 30, 10, key="r_step")
            sat = st.checkbox("Tork sınırı uygula", value=False, key="r_sat")
            tmx = st.slider("Maks. tork (N·m)", 0.05, 2.0, 0.5, 0.05, key="r_tmax", disabled=not sat)
        res = sim_roll(inertia=inert, kp=kpr, kd=kdr, step_deg=float(stp), tau_max=(tmx if sat else None))
        m = st.columns(5)
        m[0].metric("Aşım", f"%{res['overshoot_pct']:.1f}")
        m[1].metric("Oturma süresi (%2)", f"{res['settling_s']:.2f} s")
        m[2].metric("Yükselme süresi", "—" if np.isnan(res["rise_s"]) else f"{res['rise_s']:.2f} s")
        m[3].metric("Sönüm oranı ζ", f"{res['zeta']:.2f}")
        m[4].metric("Doğal frekans ωn", f"{res['wn']:.1f} rad/s")
        if res["zeta"] < 0.3:
            st.warning("Sönüm çok düşük: yatış salınım yapar. Kd'yi artırın.")
        elif res["zeta"] > 1.2:
            st.info("Aşırı sönümlü: aşım yok ama yanıt yavaş. Kd'yi azaltmayı veya Kp'yi artırmayı deneyin.")
        show_fig(P.fig_step_response(res))
        st.caption("Tek eksenli, doğrusal bir modeldir; gerçek uçuş kartı üç eksende, filtreli ve gecikmeli çalışır.")

    with t3:
        st.markdown("X şasili quadcopter'da dört motorun komutu, gaz ve üç eksen girişinden karıştırılır. "
                    "**roll > 0:** sağ taraf aşağı (sol motorlar artar) · **pitch > 0:** burun aşağı (arka motorlar artar) · "
                    "**yaw > 0:** saat yönünün tersi (FL ve RR artar).")
        a3, b3 = st.columns(2)
        with a3:
            thrt = st.slider("Gaz", 0.0, 1.0, 0.5, 0.01, key="m_thr")
            rol = st.slider("Roll", -1.0, 1.0, 0.15, 0.01, key="m_roll")
        with b3:
            pit = st.slider("Pitch", -1.0, 1.0, -0.10, 0.01, key="m_pit")
            yaw = st.slider("Yaw", -1.0, 1.0, 0.05, 0.01, key="m_yaw")
        mix = X.quad_mix(thrt, rol, pit, yaw)
        show_df(pd.DataFrame({"Motor": mix["names"], "Ham değer": np.round(mix["raw"], 3), "Komut (0–1)": np.round(mix["cmd"], 3)}))
        if mix["saturated"]:
            st.warning("Bir veya daha fazla motor sınıra (0 ya da 1) dayandı: kontrol yetkisi kaybolur. Gazı ortaya çekin veya girişleri azaltın.")

# ----------------------------------------------------------------------------- 6) Paletli tank
if view == NAV[5]:
    robot_panel("tank")
    st.divider()
    st.header("🔬 Bilimsel analiz")
    t1, t2 = st.tabs(["Paletli sürüş kinematiği", "Kuvvet ve tork analizi"])
    with t1:
        st.markdown('<div class="formula">v = (v<sub>R</sub> + v<sub>L</sub>)/2 &nbsp;·&nbsp; ω = (v<sub>R</sub> − v<sub>L</sub>)/(χ·B) '
                    '&nbsp;·&nbsp; χ ≥ 1: kayma faktörü (paletler dönerken yanlara kayar)</div>', unsafe_allow_html=True)
        a1, b1 = st.columns(2)
        with a1:
            bw = st.slider("Palet merkezleri arası B (cm) — tahmini", 6.0, 30.0, 11.6, 0.2, key="t_B")
            chi = st.slider("Kayma faktörü χ", 1.0, 2.0, 1.2, 0.05, key="t_chi")
            dur = st.slider("Süre (s)", 1, 30, 10, key="t_dur")
        with b1:
            vl = st.slider("Sol palet hızı (cm/s)", -20.0, 20.0, 4.0, 0.5, key="t_vl")
            vr = st.slider("Sağ palet hızı (cm/s)", -20.0, 20.0, 8.0, 0.5, key="t_vr")
        ts = X.tracked_turn_state(vl, vr, bw, chi)
        traj = K.simulate_diff_drive(vl, vr, ts["b_eff"], dur)
        m = st.columns(4)
        m[0].metric("Doğrusal hız v", f"{ts['v']:.1f} cm/s")
        m[1].metric("Açısal hız ω", f"{np.degrees(ts['omega']):.1f} °/s")
        m[2].metric("Dönüş yarıçapı R", "∞ (düz)" if np.isinf(ts["radius"]) else f"{abs(ts['radius']):.1f} cm")
        m[3].metric("Etkin iz genişliği", f"{ts['b_eff']:.1f} cm")
        if abs(ts["v"]) < 1e-9 and abs(ts["omega"]) > 0:
            st.info("Paletler zıt yönde ve eşit hızda: robot yerinde dönüyor (pivot dönüşü).")
        show_fig(P.fig_diff_drive(traj))
    with t2:
        st.markdown('<div class="formula">M<sub>direnç</sub> = μ<sub>y</sub>·m·g·L/4 &nbsp;·&nbsp; F<sub>pivot</sub> = M/B &nbsp;·&nbsp; '
                    'F<sub>eğim</sub> = m·g(μ<sub>r</sub>cos α + sin α) &nbsp;·&nbsp; T = F·r<sub>dişli</sub></div>', unsafe_allow_html=True)
        a2, b2, c2 = st.columns(3)
        with a2:
            mt = st.slider("Kütle (kg)", 0.3, 10.0, 1.2, 0.1, key="f_m")
            lt = st.slider("Palet temas uzunluğu L (cm)", 8.0, 40.0, 15.0, 0.5, key="f_L")
            rs_ = st.slider("Tahrik dişlisi yarıçapı (cm)", 1.0, 6.0, 2.5, 0.1, key="f_rs")
        with b2:
            mu_l = st.slider("Yanal sürtünme μy (dönüş)", 0.2, 1.2, 0.6, 0.05, key="f_mul")
            mu_r = st.slider("Yuvarlanma direnci μr", 0.02, 0.4, 0.10, 0.01, key="f_mur")
            mu_t = st.slider("Çekiş katsayısı μ", 0.2, 1.5, 0.9, 0.05, key="f_mut")
        with c2:
            slope = st.slider("Eğim (°)", 0, 45, 20, key="f_slope")
            avail = st.slider("Palet başına kullanılabilir tork (N·cm)", 5.0, 200.0, 25.0, 1.0, key="f_av")
        f_flat = X.slope_thrust(mt, mu_r, 0.0)
        f_slope = X.slope_thrust(mt, mu_r, slope)
        f_piv = X.pivot_turn_track_force(mt, mu_l, lt, bw)
        req = [X.sprocket_torque_Ncm(f_flat, rs_, 2), X.sprocket_torque_Ncm(f_slope, rs_, 2), f_piv * rs_]
        labels = ["Düz zemin", f"{slope}° eğim", "Yerinde dönüş"]
        m = st.columns(4)
        m[0].metric("Düz zemin torku", f"{req[0]:.1f} N·cm")
        m[1].metric(f"{slope}° eğimde tork", f"{req[1]:.1f} N·cm")
        m[2].metric("Yerinde dönüş torku", f"{req[2]:.1f} N·cm")
        m[3].metric("Çekiş sınırı", f"{X.traction_limit_deg(mu_t):.0f}°")
        worst = max(req)
        if worst > avail:
            st.warning(f"Gereken en yüksek tork ({worst:.1f} N·cm) kullanılabilir torku ({avail:.0f} N·cm) aşıyor: "
                       "daha güçlü motor, daha yüksek redüksiyon veya daha küçük dişli yarıçapı gerekir.")
        else:
            st.success(f"Tork payı: {avail / worst:.1f}× (en zorlu durum: {labels[int(np.argmax(req))]}).")
        if slope > X.traction_limit_deg(mu_t):
            st.warning("Eğim, çekiş sınırını aşıyor: palet yeterli torkla bile kayar.")
        show_fig(P.fig_torque(labels, req, avail))
        st.caption("B değeri, kinematik sekmesindeki kaydırıcıdan alınır. Modeller sade ve eğitim amaçlıdır: "
                   "motor verimi, dişli kayıpları ve zemin deformasyonu hesaba katılmaz.")

# ----------------------------------------------------------------------------- 7) Mars rover
if view == NAV[6]:
    robot_panel("rover")
    st.divider()
    st.header("🔬 Bilimsel analiz")
    t1, t2 = st.tabs(["Engel aşma (rocker-bogie)", "Devrilme ve kayma kararlılığı"])
    with t1:
        st.markdown("Rocker-bogie'de **bogie pivotu = (orta + arka)/2**, **rocker pivotu = (ön + bogie pivotu)/2** ve gövde, "
                    "iki yandaki rocker pivotlarının ortalamasıdır. Bu yüzden bir tekerlek engele çıkınca gövde engelin yalnızca "
                    "bir kısmı kadar yükselir; sallanma azalır.")
        a1, b1 = st.columns(2)
        with a1:
            wd = st.slider("Tekerlek çapı D (cm)", 4.0, 60.0, 10.0, 1.0, key="v_D")
            sh = st.slider("Engel yüksekliği h (cm)", 0.5, 40.0, 8.0, 0.5, key="v_h")
        with b1:
            rp = st.slider("Engel eğim uzunluğu (cm)", 0.5, 10.0, 1.0, 0.5, key="v_ramp")
            side = st.radio("Engel", ["İki yanda", "Tek yanda"], horizontal=True, key="v_side")
        rb = X.simulate_rocker_bogie_step(sh, wd, rp, both_sides=(side == "İki yanda"))
        m = st.columns(4)
        m[0].metric("Engel / çap (h/D)", f"{rb['ratio']:.2f}")
        m[1].metric("Değerlendirme", rb["status"])
        m[2].metric("Gövde yükselmesi", f"{rb['final_rise']:.1f} cm")
        m[3].metric("Tekerlek başına kazanç", f"%{100 * rb['final_rise'] / sh:.0f}")
        if rb["status"] == "aşılamaz":
            st.error("h/D > 1,5: tipik rocker-bogie tasarımları bu engeli aşamaz.")
        elif rb["status"] == "sınırda":
            st.warning("1,0 < h/D ≤ 1,5: engel aşma sınırında; tutunma ve tork kritik olur.")
        show_fig(P.fig_obstacle(rb))
        st.caption("Varsayımlar: eşit kol uzunlukları, nokta temas, tekerlek konumları çapın katları olarak ön +2,24 D, orta −0,26 D, "
                   "arka −2,10 D. 'Kolay/sınırda/aşılamaz' eşikleri (1,0 D ve 1,5 D) kaba, tipik bir değerlendirmedir.")
    with t2:
        st.markdown("Katı gövde yamaçta **yanal devrilme** için tan α = (iz/2)/h, **boyuna devrilme** için tan α = (dingil mesafesi/2)/h "
                    "ve **kayma** için tan α = μ koşullarına bakılır; hangisi küçükse önce o gerçekleşir.")
        a2, b2 = st.columns(2)
        with a2:
            tr_ = st.slider("İz genişliği (cm)", 10.0, 80.0, 28.0, 1.0, key="s_track")
            wb_ = st.slider("Dingil mesafesi (cm)", 10.0, 100.0, 35.0, 1.0, key="s_wb")
            hcg = st.slider("Ağırlık merkezi yüksekliği (cm)", 5.0, 60.0, 14.0, 1.0, key="s_cg")
        with b2:
            mu_s = st.slider("Zemin sürtünme katsayısı μ", 0.1, 1.5, 0.6, 0.05, key="s_mu")
            slp = st.slider("Yamaç eğimi (°)", 0, 60, 20, key="s_slope")
        ang = X.tipover_angles(tr_, wb_, hcg)
        slip = X.traction_limit_deg(mu_s)
        m = st.columns(3)
        m[0].metric("Yanal devrilme eşiği", f"{ang['lateral']:.0f}°")
        m[1].metric("Boyuna devrilme eşiği", f"{ang['longitudinal']:.0f}°")
        m[2].metric("Kayma eşiği", f"{slip:.0f}°")
        first = min([("yanal devrilme", ang["lateral"]), ("kayma", slip)], key=lambda x: x[1])
        if slp >= first[1]:
            st.error(f"{slp}° yamaçta {first[0]} gerçekleşir (eşik {first[1]:.0f}°).")
        elif slp >= 0.7 * first[1]:
            st.warning(f"Güvenlik payı az: yamaç, {first[0]} eşiğinin %{100 * slp / first[1]:.0f}'ine ulaştı.")
        else:
            st.success(f"Yamaç güvenli bölgede. Yan yamaçta ilk sınır: {first[0]} ({first[1]:.0f}°).")
        show_fig(P.fig_tipover(ang, slip, slp))
        st.caption("Statik hesaptır; süspansiyon hareketi, dinamik yükler ve zemin deformasyonu hesaba katılmaz. "
                   "Gerçek kullanımda en az %30 güvenlik payı bırakın.")

# ----------------------------------------------------------------------------- 8) Karşılaştırma
if view == NAV[7]:
    st.subheader("Teknik karşılaştırma")
    show_df(pd.DataFrame(COMPARE_ROWS))
    c1, c2 = st.columns(2)
    with c1:
        show_fig(P.fig_radar(RADAR_AXES, RADAR_SCORES))
    with c2:
        show_fig(P.fig_actuators(COMPARE_ROWS))
    st.caption("Radar grafiği **öznel ve eğitim amaçlı** bir değerlendirmedir, ölçüm sonucu değildir. "
               "Tablo, robot fotoğraflarından görülebilen bilgilere dayanır; kesin model/ölçü bilgisi için kit belgelerine bakın.")

# ----------------------------------------------------------------------------- 9) Hakkında
if view == NAV[8]:
    st.subheader("Proje hakkında")
    st.markdown(
        """
**MERAL Robotik Kulübü · 3D Robot Hologram Laboratuvarı**, altı robotu (çizgi izleyen araba, 6 eksenli kol, altı bacaklı robot,
quadcopter, paletli tank, Mars rover tipi robot) mavi blueprint temalı etkileşimli 3D hologramlarla tanıtır ve her robot için
temel robotik hesaplamaları gösterir.

**Nasıl kullanılır?**
1. Üstteki sekmelerden robotu seçin; *Genel Bakış* üçünü birlikte gösterir.
2. Hologramı sürükleyerek çevirin, parça düğmeleriyle parçaları tanıyın.
3. Sekmenin altındaki *Bilimsel analiz* bölümünde kaydırıcılarla parametreleri değiştirin.

**Dosya yapısı:** `app.py` (arayüz) · `robot_lab/kinematics.py` ve `robot_lab/physics.py` (hesaplamalar) · `robot_lab/plots.py` (grafikler) ·
`robot_lab/data.py` (parça verileri) · `assets/holograms/*.html` (three.js hologramları) · `tests/` (birim testleri).

**Önemli notlar**
- 3D modeller robot fotoğraflarına bakılarak **yaklaşık** olarak çizilmiştir; ölçüler birebir değildir.
- Parça açıklamalarındaki değerler bu tür kitlerde **tipik** olanlardır; kendi robotunuzun modeline göre farklı olabilir.
- Hologramlar three.js kütüphanesini CDN'den yükler, bu yüzden internet bağlantısı gerekir.
        """
    )
    st.caption(f"Sürüm {__version__}")

footer()
