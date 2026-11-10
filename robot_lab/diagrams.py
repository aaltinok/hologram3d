"""Blueprint stilinde kablolama şeması (SVG) üretici. Bağımsız çalışır, dış kütüphane gerektirmez."""
from __future__ import annotations

from html import escape

STYLES = {  # stil -> (çizgi kalınlığı, dash, renk, açıklama)
    "guc": (3.2, "", "#ffffff", "Güç hattı (+ / −)"),
    "sinyal": (1.8, "", "#bfe0ff", "Sinyal / PWM"),
    "i2c": (1.8, "9 5", "#bfe0ff", "I²C / UART veri hattı"),
    "faz": (2.4, "2 4", "#ffffff", "Motor / servo çıkışı"),
    "kablosuz": (1.8, "2 7", "#9ccfff", "Kablosuz"),
}
CHAR_W = 7.4   # 13 px monospace için yaklaşık karakter genişliği


def _bounds(n):
    return n["x"], n["y"], n["x"] + n["w"], n["y"] + n["h"]


def route(a: dict, b: dict, off: float = 0.0, mid: float = 0.0):
    """İki düğüm arasında dik açılı (ortogonal) bağlantı yolu."""
    ax0, ay0, ax1, ay1 = _bounds(a)
    bx0, by0, bx1, by1 = _bounds(b)
    acx, acy, bcx, bcy = (ax0 + ax1) / 2, (ay0 + ay1) / 2, (bx0 + bx1) / 2, (by0 + by1) / 2
    if ax1 <= bx0 or bx1 <= ax0:                         # yatay boşluk var
        x1, x2 = (ax1, bx0) if ax1 <= bx0 else (ax0, bx1)
        xm = (x1 + x2) / 2 + mid
        return [(x1, acy + off), (xm, acy + off), (xm, bcy + off), (x2, bcy + off)]
    y1, y2 = (ay1, by0) if ay1 <= by0 else (ay0, by1)    # dikey bağlantı
    ym = (y1 + y2) / 2 + mid
    return [(acx + off, y1), (acx + off, ym), (bcx + off, ym), (bcx + off, y2)]


def layout_issues(nodes: dict, edges: list, width: int, height: int) -> list[str]:
    """Düğüm taşması / çakışması / metin sığmaması / bilinmeyen düğüm kontrolü."""
    out = []
    ids = list(nodes)
    for i in ids:
        n = nodes[i]
        x0, y0, x1, y1 = _bounds(n)
        if x0 < 0 or y0 < 0 or x1 > width or y1 > height:
            out.append(f"{i}: çerçeve dışında")
        longest = max(len(t) for t in n["lines"])
        if longest * CHAR_W > n["w"] - 14:
            out.append(f"{i}: metin sığmıyor ({longest} karakter, w={n['w']})")
        if len(n["lines"]) * 17 + 14 > n["h"]:
            out.append(f"{i}: yükseklik yetersiz")
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            A, B = _bounds(nodes[ids[a]]), _bounds(nodes[ids[b]])
            if A[0] < B[2] and B[0] < A[2] and A[1] < B[3] and B[1] < A[3]:
                out.append(f"{ids[a]} ile {ids[b]} çakışıyor")
    for e in edges:
        for k in ("a", "b"):
            if e[k] not in nodes:
                out.append(f"bilinmeyen düğüm: {e[k]}")
    return out


def wiring_svg(title: str, nodes: dict, edges: list, width: int = 980, height: int = 400) -> str:
    used = []
    parts = []
    # kenarlar önce (düğümlerin altında kalsın)
    for e in edges:
        a, b = nodes[e["a"]], nodes[e["b"]]
        pts = route(a, b, e.get("off", 0.0), e.get("mid", 0.0))
        w, dash, color, _ = STYLES[e.get("stil", "sinyal")]
        if e.get("stil", "sinyal") not in used:
            used.append(e.get("stil", "sinyal"))
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
                     f'{"stroke-dasharray=%s" % chr(34) + dash + chr(34) if dash else ""} stroke-linejoin="round"/>')
        parts.append(f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="3.5" fill="#fff"/>'
                     f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="3.5" fill="#fff"/>')
        if e.get("etiket"):
            mx = (pts[1][0] + pts[2][0]) / 2
            my = (pts[1][1] + pts[2][1]) / 2
            tw = len(e["etiket"]) * 6.6 + 10
            parts.append(f'<rect x="{mx - tw / 2:.1f}" y="{my - 9:.1f}" width="{tw:.1f}" height="18" rx="3" '
                         f'fill="#0b3a8f" stroke="#9ccfff" stroke-width="1"/>'
                         f'<text x="{mx:.1f}" y="{my + 4:.1f}" text-anchor="middle" font-size="11" fill="#fff">'
                         f'{escape(e["etiket"])}</text>')
    for nid, n in nodes.items():
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#143f95" stroke="#e8f3ff" stroke-width="2"/>')
        for i, t in enumerate(n["lines"]):
            weight, size = ("700", 13) if i == 0 else ("400", 11.5)
            parts.append(f'<text x="{x + w / 2}" y="{y + 22 + i * 17}" text-anchor="middle" font-size="{size}" '
                         f'font-weight="{weight}" fill="#fff">{escape(t)}</text>')
    # açıklama (legend)
    lx = 24
    legend = []
    for s in used:
        w, dash, color, text = STYLES[s]
        legend.append(f'<line x1="{lx}" y1="{height - 40}" x2="{lx + 38}" y2="{height - 40}" stroke="{color}" stroke-width="{w}" '
                      f'{"stroke-dasharray=%s" % chr(34) + dash + chr(34) if dash else ""}/>'
                      f'<text x="{lx + 46}" y="{height - 36}" font-size="11" fill="#e8f3ff">{escape(text)}</text>')
        lx += 46 + len(text) * 6.8 + 22
    block = (f'<rect x="{width - 410}" y="{height - 62}" width="390" height="46" fill="none" stroke="#e8f3ff" stroke-width="1.5"/>'
             f'<line x1="{width - 410}" y1="{height - 39}" x2="{width - 20}" y2="{height - 39}" stroke="#e8f3ff" stroke-width="1"/>'
             f'<text x="{width - 215}" y="{height - 46}" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">'
             f'MERAL ROBOTİK KULÜBÜ · KABLOLAMA ŞEMASI</text>'
             f'<text x="{width - 215}" y="{height - 24}" text-anchor="middle" font-size="11" fill="#cfe6ff">{escape(title)} · REV A · ÖLÇEKSİZ</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" '
            f'font-family="ui-monospace,Menlo,Consolas,monospace">'
            f'<defs><pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse">'
            f'<path d="M20 0H0V20" fill="none" stroke="#fff" stroke-opacity=".07"/></pattern>'
            f'<pattern id="g2" width="100" height="100" patternUnits="userSpaceOnUse">'
            f'<rect width="100" height="100" fill="url(#g1)"/><path d="M100 0H0V100" fill="none" stroke="#fff" stroke-opacity=".14"/></pattern></defs>'
            f'<rect width="{width}" height="{height}" fill="#0b3a8f"/><rect width="{width}" height="{height}" fill="url(#g2)"/>'
            f'<rect x="6" y="6" width="{width - 12}" height="{height - 12}" fill="none" stroke="#fff" stroke-opacity=".6"/>'
            + "".join(parts) + "".join(legend) + block + "</svg>")


def wiring_html(title: str, nodes: dict, edges: list, width: int = 980, height: int = 400) -> str:
    svg = wiring_svg(title, nodes, edges, width, height)
    return ('<!DOCTYPE html><html><body style="margin:0;background:#04204f">'
            f'<div style="border:1px solid rgba(126,190,255,.55);border-radius:10px;overflow:hidden">{svg}</div></body></html>')
