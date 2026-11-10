import importlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from robot_lab import diagrams
from robot_lab.data import HOLO_FILES, ROBOTS
from robot_lab.guides import GUIDES

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "holograms"
NAME_RE = re.compile(r"""(\w+)"?:\s*\{\s*"?n"?\s*:\s*["']([^"']+)["']""")


def holo_keys(key):
    return [k for k, _ in NAME_RE.findall((ASSETS / HOLO_FILES[key]).read_text(encoding="utf-8"))]


def test_every_robot_has_complete_guide():
    assert set(GUIDES) == set(ROBOTS)
    for key, g in GUIDES.items():
        for f in ("zorluk", "sure", "butce", "hedef", "beceri", "ogrenme", "araclar", "malzeme", "adimlar", "kablolama",
                  "kod", "test", "sorun", "guvenlik", "gelistir"):
            assert g[f], (key, f)
        assert len(g["adimlar"]) >= 8 and len(g["malzeme"]) >= 8 and len(g["test"]) >= 6 and len(g["sorun"]) >= 6
        for s in g["adimlar"]:
            assert s["baslik"] and s["yap"] and s["kontrol"] and s["sure"], (key, s["baslik"])
            assert len(s["yap"]) >= 2


def test_steps_cover_exactly_the_hologram_parts():
    for key, g in GUIDES.items():
        keys = holo_keys(key)
        assert keys, key
        new = [k for s in g["adimlar"] for k in s["yeni"]]
        assert sorted(new) == sorted(keys), (key, sorted(set(keys) ^ set(new)))        # her parça tam bir kez eklenir
        for s in g["adimlar"]:
            assert set(s["vurgu"]) <= set(keys), (key, s["baslik"])


def test_wiring_diagrams_are_valid():
    for key, g in GUIDES.items():
        kb = g["kablolama"]
        w, h = kb["boyut"]
        assert diagrams.layout_issues(kb["nodes"], kb["edges"], w, h) == [], key
        root = ET.fromstring(diagrams.wiring_svg(key, kb["nodes"], kb["edges"], w, h))       # geçerli XML
        assert root.tag.endswith("svg")
        assert kb["pinler"] and all(len(r) == 4 for r in kb["pinler"])


def test_code_items_are_resolvable_and_balanced():
    for key, g in GUIDES.items():
        for it in g["kod"]:
            assert it["baslik"] and it["dosya"] and it["dil"] and it["aciklama"]
            if "fn" in it:
                mod, name = it["fn"].split(".")
                assert callable(getattr(importlib.import_module(f"robot_lab.{mod}"), name)), it["fn"]
            elif it["dil"] == "cpp":
                code = it["kod"]
                assert code.count("{") == code.count("}") and code.count("(") == code.count(")"), (key, it["dosya"])
                assert "void setup()" in code and "void loop()" in code or "void steering" in code
