"""HV-BIE public API."""

from __future__ import annotations

from bs4 import BeautifulSoup

from hv_bie.types import (
    AbilitiesState,
    BattleSnapshot,
    CombatLog,
    ItemsState,
    PlayerState,
)
from hv_bie.parsers.vitals import parse_vitals


def parse_snapshot(html: str) -> BattleSnapshot:
    """Parse one HentaiVerse battle HTML into a structured snapshot."""

    soup = BeautifulSoup(html, "html.parser")
    warnings: list[str] = []

    player, player_warnings = parse_vitals(soup)
    warnings.extend(player_warnings)

    snapshot = BattleSnapshot(
        player=player,
        abilities=AbilitiesState(),
        monsters=[],
        log=CombatLog(),
        items=ItemsState(),
        warnings=warnings,
    )
    return snapshot


__all__ = ["parse_snapshot", "BattleSnapshot", "PlayerState"]
