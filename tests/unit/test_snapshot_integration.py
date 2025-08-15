from pathlib import Path
from hv_bie import parse_snapshot

FIX = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "hv"


def read_fixture(name: str) -> str:
    return (FIX / name).read_text(encoding="utf-8")


def test_parse_fixture_0():
    html = read_fixture("The HentaiVerse.htm")
    snap = parse_snapshot(html)

    # vitals
    assert 99.0 <= snap.player.hp_percent <= 100.0
    assert snap.player.hp_value == 23618
    assert 99.0 <= snap.player.mp_percent <= 100.0
    assert snap.player.mp_value == 1595
    assert 99.0 <= snap.player.sp_percent <= 100.0
    assert snap.player.sp_value == 1317
    assert snap.player.overcharge_value == 0

    # player buffs (from effects pane) and no Spirit Stance (spirit_n)
    pbuf_names = set(snap.player.buffs.keys())
    assert {
        "Protection",
        "Haste",
        "Shadow Veil",
        "Spark of Life",
        "Spirit Shield",
    }.issubset(pbuf_names)
    assert "Spirit Stance" not in pbuf_names

    # abilities
    # skills
    assert len(snap.abilities.skills) == 5
    skills_names = set(snap.abilities.skills.keys())
    assert "Flee" in skills_names
    flee_skill = snap.abilities.skills["Flee"]
    assert flee_skill.available is True
    assert flee_skill.cost_type == None
    assert flee_skill.cost == 0
    assert flee_skill.cooldown_turns == 0
    assert "Shield Bash" in skills_names
    shield_bash_skill = snap.abilities.skills["Shield Bash"]
    assert shield_bash_skill.available is False
    assert shield_bash_skill.cost_type == "Overcharge"
    assert shield_bash_skill.cost == 25
    assert shield_bash_skill.cooldown_turns == 10
    assert "Vital Strike" in skills_names
    shield_bash_skill = snap.abilities.skills["Vital Strike"]
    assert shield_bash_skill.available is False
    assert shield_bash_skill.cost_type == "Overcharge"
    assert shield_bash_skill.cost == 50
    assert shield_bash_skill.cooldown_turns == 10
    # spells
    assert len(snap.abilities.spells) == 32
    spells_names = set(snap.abilities.spells.keys())
    assert "Fiery Blast" in spells_names
    fiery_blast_spell = snap.abilities.spells["Fiery Blast"]
    assert fiery_blast_spell.available is True
    assert fiery_blast_spell.cost_type == "MP"
    assert fiery_blast_spell.cost == 29
    assert fiery_blast_spell.cooldown_turns == 0
    assert "Cure" in spells_names
    cure_spell = snap.abilities.spells["Cure"]
    assert cure_spell.available is True
    assert cure_spell.cost_type == "MP"
    assert cure_spell.cost == 85
    assert cure_spell.cooldown_turns == 2

    # monsters
    assert len(snap.monsters) == 2
    names = {m.name for m in snap.monsters.values()}
    # first monster name exists and is parsed (from title)
    monster0 = snap.monsters[1]
    assert "Touch" in names
    assert monster0.alive is True
    assert len(monster0.buffs) == 0
    assert monster0.hp_percent == 100.0
    assert 34.0 <= monster0.mp_percent <= 35.0
    assert 11.0 <= monster0.sp_percent <= 12.0
    assert monster0.name == "Touch"
    assert monster0.slot_index == 1
    assert monster0.system_monster_type is None
    # second monster name exists and is parsed (from title)
    monster1 = snap.monsters[2]
    assert "Peerlesssss2 Oak Staff" in names
    assert monster1.alive is True
    assert len(monster1.buffs) == 0
    assert monster1.hp_percent == 100.0
    assert 44.5 <= monster1.mp_percent <= 45.5
    assert 8.0 <= monster1.sp_percent <= 9.0
    assert monster1.name == "Peerlesssss2 Oak Staff"
    assert monster1.slot_index == 2
    assert monster1.system_monster_type is None
    # all monsters have valid percentages when alive
    for m in snap.monsters.values():
        if m.alive:
            assert 0.0 <= m.hp_percent <= 100.0
            assert 0.0 <= m.mp_percent <= 100.0
            assert 0.0 <= m.sp_percent <= 100.0

    # log
    assert snap.log.lines[-1] == "You gain the effect Spirit Shield."
    assert snap.log.lines[0] == "Initializing arena challenge #32 (Round 1 / 85) ..."
    assert snap.log.current_round == 1
    assert snap.log.total_round == 85

    # items
    assert "Health Draught" in snap.items.items
    needed_items = {
        "Health Draught",
        "Health Potion",
        "Health Elixir",
        "Mana Draught",
        "Mana Potion",
        "Mana Elixir",
        "Spirit Draught",
        "Spirit Potion",
        "Spirit Elixir",
    }
    assert needed_items.issubset(set(snap.items.items.keys()))
    # quickbar placeholders parsed (16 slots in fixture, empty names)
    assert len(snap.items.quickbar) == 16
    assert all(q.name == "" for q in snap.items.quickbar)

    # warnings should be empty for a complete page
    assert snap.warnings == []

    # serialization helpers
    d = snap.as_dict()
    assert isinstance(d, dict) and "player" in d and "abilities" in d
    js = snap.to_json()
    import json as _json

    obj = _json.loads(js)
    assert isinstance(obj, dict) and obj.get("items", {}).get("items")


def test_parse_fixture_1():
    html = read_fixture("The HentaiVerse1.htm")
    snap = parse_snapshot(html)

    # vitals
    assert 99.0 <= snap.player.hp_percent <= 100.0
    assert snap.player.hp_value == 23621
    assert 93.0 <= snap.player.mp_percent <= 94.0
    assert snap.player.mp_value == 1498
    assert 92.0 <= snap.player.sp_percent <= 93.0
    assert snap.player.sp_value == 1218
    assert snap.player.overcharge_value == 133

    # spirit stance in effects
    names = set(snap.player.buffs.keys())
    assert "Spirit Stance" in names

    # system monster present (heuristic sets Rare for the one with style)
    assert any(m.system_monster_type for m in snap.monsters.values())

    # monster buffs parsed
    assert any(any(b.name for b in m.buffs) for m in snap.monsters.values())


def test_parse_fixture_4():
    html = read_fixture("The HentaiVerse4.htm")
    snap = parse_snapshot(html)

    assert "Spirit Gem" in snap.items.items
    spirit_gem = snap.items.items["Spirit Gem"]
    assert spirit_gem.slot == "p"
    assert spirit_gem.available == True


def test_parse_fixture_5():
    html = read_fixture("The HentaiVerse5.htm")
    snap = parse_snapshot(html)

    assert "Scroll of the Avatar" in snap.items.items
    avatar_scroll = snap.items.items["Scroll of the Avatar"]
    assert avatar_scroll.slot == "s1"
    assert avatar_scroll.available == True
    assert snap.items.items["Scroll of the Gods"].available == False
