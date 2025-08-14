"""Data models for HV-BIE.

Public dataclasses representing parsed battle data.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json


@dataclass
class Buff:
    """Status effect on player or monster."""

    name: str
    remaining_seconds: float | None
    is_permanent: bool


@dataclass
class Ability:
    """Action available to the player."""

    name: str
    available: bool
    cost: float | None
    cost_type: str | None
    cooldown_seconds: float | None


@dataclass
class AbilitiesState:
    """Grouping of skills and spells."""

    skills: list[Ability] = field(default_factory=list)
    spells: list[Ability] = field(default_factory=list)


@dataclass
class Monster:
    """Enemy monster shown on the battlefield."""

    slot_index: int
    name: str
    alive: bool
    system_monster_type: str | None
    hp_percent: float
    mp_percent: float
    sp_percent: float
    buffs: list[Buff] = field(default_factory=list)


@dataclass
class CombatLog:
    """Combat text lines and round info."""

    lines: list[str] = field(default_factory=list)
    current_round: int | None = None
    total_round: int | None = None


@dataclass
class Item:
    """Item shown in battle."""

    slot: str | int
    name: str


@dataclass
class QuickSlot:
    """Quickbar slot item."""

    slot: str | int
    name: str


@dataclass
class ItemsState:
    """Items and quickbar grouping."""

    items: list[Item] = field(default_factory=list)
    quickbar: list[QuickSlot] = field(default_factory=list)


@dataclass
class PlayerState:
    """Player resource vitals and buffs."""

    hp_percent: float
    hp_value: int
    mp_percent: float
    mp_value: int
    sp_percent: float
    sp_value: int
    overcharge_value: int
    buffs: list[Buff] = field(default_factory=list)


@dataclass
class BattleSnapshot:
    """Aggregated view of one battle page."""

    player: PlayerState
    abilities: AbilitiesState
    monsters: list[Monster]
    log: CombatLog
    items: ItemsState
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        """Return a ``dict`` representation of the snapshot."""

        return asdict(self)

    def to_json(self) -> str:
        """Serialize the snapshot to JSON."""

        return json.dumps(self.as_dict())


__all__ = [
    "Buff",
    "Ability",
    "AbilitiesState",
    "Monster",
    "CombatLog",
    "Item",
    "QuickSlot",
    "ItemsState",
    "PlayerState",
    "BattleSnapshot",
]
