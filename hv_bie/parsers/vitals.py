"""Player vitals parser."""

from __future__ import annotations

from bs4 import BeautifulSoup
import re
from typing import Tuple

from hv_bie.types import PlayerState

BAR_IDS = {
    "hp": "dvbh",
    "mp": "dvbm",
    "sp": "dvbs",
    "oc": "dvbc",
}

VALUE_IDS = {
    "hp": "dvrhd",
    "mp": "dvrm",
    "sp": "dvrs",
    "oc": "dvrc",
}

MAX_WIDTH = 414


def _extract_width(node: BeautifulSoup) -> float | None:
    """Extract width in pixels from style attribute."""

    if not node:
        return None
    style = node.get("style", "")
    match = re.search(r"width:(\d+)px", style)
    if match:
        return float(match.group(1))
    return None


def parse_vitals(soup: BeautifulSoup) -> Tuple[PlayerState, list[str]]:
    """Parse player vitals from soup.

    Returns the parsed ``PlayerState`` and a list of warning messages.
    """

    warnings: list[str] = []

    def get_value(key: str) -> int:
        div = soup.find(id=VALUE_IDS[key])
        if div and div.text.strip().isdigit():
            return int(div.text.strip())
        warnings.append(f"missing {key} value")
        return 0

    def get_percent(key: str) -> float:
        img = soup.select_one(f"#{BAR_IDS[key]} img")
        width = _extract_width(img)
        if width is None:
            warnings.append(f"missing {key} bar")
            return 0.0
        return max(0.0, min(100.0, width / MAX_WIDTH * 100))

    hp_val = get_value("hp")
    mp_val = get_value("mp")
    sp_val = get_value("sp")
    oc_val = get_value("oc")

    player = PlayerState(
        hp_percent=get_percent("hp"),
        hp_value=hp_val,
        mp_percent=get_percent("mp"),
        mp_value=mp_val,
        sp_percent=get_percent("sp"),
        sp_value=sp_val,
        overcharge_value=oc_val,
    )

    return player, warnings


__all__ = ["parse_vitals"]
