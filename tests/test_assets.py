import re
from pathlib import Path
from robot_lab.data import HOLO_FILES, ROBOTS, COMPARE_ROWS, RADAR_SCORES, RADAR_AXES, parts_df

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "holograms"


def test_all_holograms_exist_and_are_blueprint_blue():
    assert set(HOLO_FILES) == set(ROBOTS) == {"araba", "kol", "hexapod", "quad", "tank", "rover"}
    for key, fn in HOLO_FILES.items():
        txt = (ASSETS / fn).read_text(encoding="utf-8")
        assert "blueprint" in txt.lower() and "MERAL Robotik Kulübü" in txt and "three.min.js" in txt, fn
        assert not re.search(r"0x00e5ff|229,255", txt), fn          # camgöbeği kalmamalı
        assert "const bp=" in txt and "c=bp(c)" in txt, fn          # tüm parçalar mavi tona çevrilir


def test_robot_data_consistent():
    for key, r in ROBOTS.items():
        df = parts_df(key)
        assert len(df) >= 7 and df["Parça"].is_unique, key
        assert len(r["metrikler"]) == 3
    assert len(COMPARE_ROWS) == len(RADAR_SCORES) == 6
    assert all(len(v) == len(RADAR_AXES) for v in RADAR_SCORES.values())
