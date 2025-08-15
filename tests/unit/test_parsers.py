from pathlib import Path
from hv_bie.parsers import (
    parse_player_vitals,
    parse_player_buffs,
    parse_abilities,
    parse_monsters,
    parse_log,
    parse_items,
)
from bs4 import BeautifulSoup

FIX = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "hv"


def soup_of(name: str):
    return BeautifulSoup((FIX / name).read_text(encoding="utf-8"), "html.parser")


def test_vitals_and_buffs():
    s0 = soup_of("The HentaiVerse.htm")
    warnings: list[str] = []
    p = parse_player_vitals(s0, warnings)
    assert p.hp_value > 0 and p.mp_value > 0 and p.sp_value > 0

    buffs = parse_player_buffs(s0, warnings)
    assert any(b.name == "Protection" or b.name == "Spirit Shield" for b in buffs)


def test_abilities_tables():
    s0 = soup_of("The HentaiVerse.htm")
    warnings: list[str] = []
    ab = parse_abilities(s0, warnings)
    assert ab.skills and ab.spells
    assert "Shield Bash" in ab.skills
    assert "Fiery Blast" in ab.spells


def test_monsters_and_buffs():
    s1 = soup_of("The HentaiVerse1.htm")
    warnings: list[str] = []
    ms = parse_monsters(s1, warnings)
    assert len(ms) >= 3
    assert any(m.system_monster_type is not None for m in ms)
    assert any(m.buffs for m in ms)


def test_log_and_items():
    s0 = soup_of("The HentaiVerse.htm")
    warnings: list[str] = []
    log = parse_log(s0, warnings)
    assert log.lines
    assert (log.current_round is None) or log.current_round >= 1

    items = parse_items(s0, warnings)
    assert any(i.name == "Health Draught" for i in items.items)
