"""Streamlit arayüz yardımcıları: tema CSS'i, hologram gömme, sürüm uyumlu çizim fonksiyonları."""
from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from .data import HOLO_FILES

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "holograms"

CSS = """
<style>
.stApp{background:
 linear-gradient(rgba(0,229,255,.035) 1px,transparent 1px) 0 0/32px 32px,
 linear-gradient(90deg,rgba(0,229,255,.035) 1px,transparent 1px) 0 0/32px 32px,
 radial-gradient(ellipse at 50% 0%,#06303f 0%,#02101a 55%,#010a10 100%);}
h1,h2,h3{letter-spacing:.04em}
.lab-head{border:1px solid rgba(0,229,255,.45);border-radius:10px;padding:14px 18px;margin-bottom:10px;
 background:linear-gradient(90deg,rgba(0,229,255,.10),rgba(0,229,255,.02));box-shadow:0 0 22px rgba(0,229,255,.12)}
.lab-head .club{font-size:.8rem;letter-spacing:.35em;color:#6ff;text-shadow:0 0 8px #0ff}
.lab-head .title{font-size:1.7rem;font-weight:700;color:#fff;margin:2px 0}
.lab-head .sub{font-size:.85rem;color:#9fd8e8}
[data-testid="stMetric"]{background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.3);border-radius:8px;padding:8px 12px}
[data-testid="stMetricValue"]{color:#6ff}
.stTabs [data-baseweb="tab"]{letter-spacing:.04em}
.formula{border-left:3px solid #00e5ff;padding:2px 12px;color:#bfeaf5;background:rgba(0,229,255,.05)}
.foot{text-align:center;letter-spacing:.3em;color:#bff;text-shadow:0 0 6px #0ff,0 0 14px #0ee;margin-top:28px;padding:14px 0;
 border-top:1px solid rgba(0,229,255,.25)}
iframe{border:1px solid rgba(126,190,255,.55);border-radius:10px;background:#0b3a8f}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def header() -> None:
    st.markdown(
        '<div class="lab-head"><div class="club">MERAL ROBOTİK KULÜBÜ</div>'
        '<div class="title">3D Robot Hologram Laboratuvarı</div>'
        '<div class="sub">Robot araba · Robot kol · Hexapod · Quadcopter · Paletli tank · Mars rover — mavi blueprint hologramlar, parça tanıtımı ve bilimsel analiz</div></div>',
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown('<div class="foot">MERAL Robotik Kulübü</div>', unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_holo(key: str) -> str:
    return (ASSETS / HOLO_FILES[key]).read_text(encoding="utf-8")


def holo(key: str, height: int) -> None:
    components.html(load_holo(key), height=height, scrolling=False)


def show_fig(fig) -> None:
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:  # eski Streamlit sürümleri
        st.plotly_chart(fig, use_container_width=True)


def show_df(df) -> None:
    try:
        st.dataframe(df, hide_index=True, width="stretch")
    except TypeError:
        st.dataframe(df, hide_index=True, use_container_width=True)
