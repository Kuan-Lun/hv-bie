from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Buff:
    name: str
    remaining_turns: float
    is_permanent: bool


@dataclass(frozen=True)
class Ability:
    name: str
    element_id: str
    available: bool
    cost: int
    cost_type: Optional[str]
    cooldown_turns: int


@dataclass(frozen=True)
class AbilitiesState:
    skills: dict[str, Ability] = field(default_factory=dict)
    spells: dict[str, Ability] = field(default_factory=dict)


@dataclass(frozen=True)
class PlayerState:
    hp_percent: float = 0.0
    hp_value: int = 0
    mp_percent: float = 0.0
    mp_value: int = 0
    sp_percent: float = 0.0
    sp_value: int = 0
    overcharge_value: int = 0
    buffs: dict[str, Buff] = field(default_factory=dict)


@dataclass(frozen=True)
class Monster:
    slot_index: int
    name: str
    alive: bool
    system_monster_type: Optional[str]
    hp_percent: float
    mp_percent: float
    sp_percent: float
    buffs: dict[str, Buff] = field(default_factory=dict)


@dataclass(frozen=True)
class CombatLog:
    lines: list[str] = field(default_factory=list)
    current_round: Optional[int] = None
    total_round: Optional[int] = None


@dataclass(frozen=True)
class Item:
    slot: str | int
    name: str
    element_id: str
    available: bool


@dataclass(frozen=True)
class QuickSlot:
    slot: str | int
    name: str


@dataclass(frozen=True)
class ItemsState:
    items: dict[str, Item] = field(default_factory=dict)
    quickbar: list[QuickSlot] = field(default_factory=list)


@dataclass(frozen=True)
class BattleSnapshot:
    player: PlayerState
    abilities: AbilitiesState
    monsters: dict[int, Monster]
    log: CombatLog
    items: ItemsState
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False)
