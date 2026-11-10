"""Her robot sayfasındaki 'Nasıl yapılır?' rehberinin Streamlit arayüzü."""
from __future__ import annotations

import importlib
import inspect
import re
from html import escape

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from . import diagrams
from . import physics as X
from . import plots as P
from .data import ROBOTS
from .guides import GUIDES
from .ui import holo_build, load_holo, show_df, show_fig


def build_steps(g: dict, final: bool = False) -> list:
    """Her adım için hologramda görünecek (show) ve vurgulanacak (focus) parça gruplarını üretir."""
    shown: list = []
    out = []
    for s in g["adimlar"]:
        shown += [k for k in s["yeni"] if k not in shown]
        out.append({"t": s["baslik"], "show": list(shown), "focus": list(s["yeni"] or s["vurgu"])})
    if final:
        out.append({"t": "Tamamlandı: tüm parçalar monte edildi", "show": list(shown), "focus": []})
    return out


def part_names(key: str) -> dict:
    """Hologramdaki parça grubu anahtarı -> okunabilir ad (INFO tablosundan)."""
    txt = load_holo(key)
    return {k: n.split(" (")[0] for k, n in re.findall(r"""(\w+)"?:\s*\{\s*"?n"?\s*:\s*["']([^"']+)["']""", txt)}


def source_of(fn_path: str) -> str:
    mod, name = fn_path.split(".")
    return inspect.getsource(getattr(importlib.import_module(f"robot_lab.{mod}"), name))


def _chips(items) -> None:
    st.markdown("".join(f'<span class="chip">{escape(str(i))}</span>' for i in items), unsafe_allow_html=True)


def _checklist(prefix: str, items: list, caption: str) -> None:
    done = 0
    for i, text in enumerate(items):
        if st.checkbox(text, key=f"{prefix}_{i}"):
            done += 1
    st.progress(done / max(len(items), 1))
    st.caption(f"{caption}: {done} / {len(items)}")


def _go(key: str, delta: int, n: int) -> None:
    st.session_state[key] = min(max(st.session_state.get(key, 1) + delta, 1), n)


def _overview_tab(key: str, g: dict) -> None:
    st.markdown(f"**Hedef:** {g['hedef']}")
    st.markdown("**Gerekli beceriler**")
    _chips(g["beceri"])
    st.markdown("**Bu projede öğrenecekleriniz**")
    for o in g["ogrenme"]:
        st.markdown(f"- {o}")
    st.markdown("**Gerekli araçlar**")
    _chips(g["araclar"])
    st.markdown("**Malzeme listesi (BOM)**")
    df = pd.DataFrame(g["malzeme"], columns=["Parça", "Adet", "Not"])
    df["Adet"] = df["Adet"].astype(str)
    show_df(df)
    with st.expander("✔️ Malzeme kontrol listesi (hazır olanları işaretleyin)"):
        _checklist(f"{key}_bom", [f"{a} × {p}" for p, a, _ in g["malzeme"]], "Hazır malzeme")
    st.caption("Parça modelleri tipik örneklerdir; kendi kitinizin kılavuzu ve veri sayfaları önceliklidir.")


def _steps_tab(key: str, g: dict, height: int) -> None:
    n = len(g["adimlar"])
    skey = f"{key}_step"
    if skey not in st.session_state:
        st.session_state[skey] = 1
    all_steps = build_steps(g, final=False)
    c1, c2, c3 = st.columns([1, 1, 3])
    c1.button("◀ Önceki", key=f"{key}_prev", on_click=_go, args=(skey, -1, n))
    c2.button("Sonraki ▶", key=f"{key}_next", on_click=_go, args=(skey, 1, n))
    c3.toggle("🎬 Montaj animasyonunu otomatik oynat", key=f"{key}_auto")
    auto = st.session_state.get(f"{key}_auto", False)
    step = st.select_slider("Adım", options=list(range(1, n + 1)), key=skey,
                            format_func=lambda i: f"{i}. {g['adimlar'][i - 1]['baslik']}")
    ex = st.slider("Patlatılmış görünüm", 0.0, 1.0, 0.0, 0.05, key=f"{key}_explode",
                   help="Parçaları katman katman ayırır; her parçanın yerini daha net gösterir.")
    left, right = st.columns([3, 2], gap="medium")
    h = min(height, 700)
    name = ROBOTS[key]["ad"].split(" (")[0].upper()
    with left:
        if auto:
            holo_build(key, build_steps(g, final=True), idx=0, autoplay=True, explode=ex, height=h, title=f"MONTAJ · {name}")
        else:
            holo_build(key, all_steps, idx=step - 1, autoplay=False, explode=ex, height=h, title=f"MONTAJ · {name}")
    with right:
        st.progress(step / n)
        if auto:
            st.markdown("**Montaj sırası** (animasyon otomatik döner; tek bir adımı incelemek için animasyonu kapatın)")
            for i, s in enumerate(g["adimlar"], 1):
                st.markdown(f"{i}. {s['baslik']}  \n<small>⏱️ {s['sure']}</small>", unsafe_allow_html=True)
            return
        s = g["adimlar"][step - 1]
        st.markdown(f"### Adım {step} / {n}: {s['baslik']}")
        st.caption(f"⏱️ Tahmini süre: {s['sure']}")
        for line in s["yap"]:
            st.markdown(f"- {line}")
        if s["ipucu"]:
            st.info("💡 " + s["ipucu"])
        if s["uyari"]:
            st.warning("⚠️ " + s["uyari"])
        st.success("✅ Kontrol: " + s["kontrol"])
        if s["yeni"]:
            pn = part_names(key)
            st.caption("Bu adımda hologramda belirenler: " + ", ".join(pn.get(k, k) for k in s["yeni"]))


def _wiring_tab(key: str, g: dict) -> None:
    kb = g["kablolama"]
    w, h = kb["boyut"]
    st.markdown("Blueprint kablolama şeması: kalın çizgi güç hattı, ince çizgi sinyal, kesikli çizgi veri hattı, noktalı çizgi motor / servo çıkışıdır.")
    components.html(diagrams.wiring_html(ROBOTS[key]["ad"], kb["nodes"], kb["edges"], w, h), height=h + 16, scrolling=False)
    st.markdown("**Bağlantı tablosu**")
    show_df(pd.DataFrame(kb["pinler"], columns=["Kaynak", "Hedef", "Bağlantı / pin", "Not"]))
    st.caption("Pin numaraları örnektir; kartınıza ve sürücünüze göre değişebilir. Bağlantıyı yapmadan önce veri sayfasını kontrol edin.")


def _rover_tool() -> None:
    st.markdown("#### 🧮 Direksiyon geometrisi hesaplayıcısı")
    a, b = st.columns(2)
    with a:
        straight = st.checkbox("Düz gidiş (R = ∞)", value=False, key="rv_straight")
        radius = st.slider("Dönüş yarıçapı R (cm) — + sol, − sağ, 0 yerinde dönüş", -300, 300, 80, 5, key="rv_R")
    with b:
        track = st.slider("İz genişliği (cm)", 10.0, 80.0, 28.0, 1.0, key="rv_T")
        dfv = st.slider("Ön köşe tekerlek mesafesi (cm)", 5.0, 50.0, 17.0, 1.0, key="rv_DF")
        drv = st.slider("Arka köşe tekerlek mesafesi (cm)", 5.0, 50.0, 16.0, 1.0, key="rv_DR")
    r = float("inf") if straight else float(radius)
    res = X.rover_steering(r, dfv, drv, track)
    show_df(pd.DataFrame({"Tekerlek": res["names"], "Direksiyon açısı (°)": np.round(res["angle_deg"], 1),
                          "Göreli hız": np.round(res["speed"], 2)}))
    if any(abs(x) > 45 for x in res["angle_deg"]):
        st.warning("Bazı açılar ±45°'yi aşıyor: servo sınırlarını ve mekanik dönüş aralığını kontrol edin.")
    show_fig(P.fig_rover_steering(res["angle_deg"], track, dfv, drv, r))


def _code_tab(key: str, g: dict) -> None:
    for i, item in enumerate(g["kod"]):
        code = source_of(item["fn"]) if "fn" in item else item["kod"]
        st.markdown(f"**{item['baslik']}** — {item['aciklama']}")
        st.code(code, language=item["dil"])
        st.download_button(f"⬇️ {item['dosya']} indir", data=code, file_name=item["dosya"], mime="text/plain", key=f"{key}_dl_{i}")
    st.caption("Örnek kodlardır: pin numaralarını, kalibrasyon değerlerini ve güvenlik sınırlarını kendi donanımınıza göre ayarlayın.")
    if key == "rover":
        _rover_tool()


def _test_tab(key: str, g: dict) -> None:
    st.markdown("**Kabul kontrol listesi**")
    _checklist(f"{key}_test", g["test"], "Geçen test")


def _help_tab(key: str, g: dict) -> None:
    st.markdown("**Sorun giderme**")
    show_df(pd.DataFrame(g["sorun"], columns=["Belirti", "Olası neden", "Çözüm"]))
    st.markdown("**Güvenlik**")
    for t in g["guvenlik"]:
        st.error("⚠️ " + t)
    st.markdown("**Geliştirme fikirleri**")
    for t in g["gelistir"]:
        st.markdown(f"- {t}")


def render_guide(key: str, height: int) -> None:
    g = GUIDES[key]
    st.divider()
    st.header("🛠️ Nasıl yapılır? Adım adım yapım rehberi")
    m = st.columns(4)
    m[0].metric("Zorluk", g["zorluk"])
    m[1].metric("Tahmini süre", g["sure"])
    m[2].metric("Bütçe sınıfı", g["butce"])
    m[3].metric("Montaj adımı", str(len(g["adimlar"])))
    tabs = st.tabs(["📋 Genel ve malzeme", "🧩 Adım adım montaj", "🔌 Kablolama", "💻 Yazılım", "✅ Test", "🛟 Sorun giderme ve güvenlik"])
    with tabs[0]:
        _overview_tab(key, g)
    with tabs[1]:
        _steps_tab(key, g, height)
    with tabs[2]:
        _wiring_tab(key, g)
    with tabs[3]:
        _code_tab(key, g)
    with tabs[4]:
        _test_tab(key, g)
    with tabs[5]:
        _help_tab(key, g)
