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
    assert flee_skill.cost_type is None
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
    # basic abilities shape
    assert isinstance(snap.abilities.skills, dict)
    assert isinstance(snap.abilities.spells, dict)

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
    assert isinstance(snap.log.lines, list)

    # items
    assert "health draught" in snap.items.items
    needed_items = {
        "health draught",
        "health potion",
        "health elixir",
        "mana draught",
        "mana potion",
        "mana elixir",
        "spirit draught",
        "spirit potion",
        "spirit elixir",
    }
    assert needed_items.issubset(set(snap.items.items.keys()))
    # quickbar placeholders parsed (16 slots in fixture, empty names)
    assert len(snap.items.quickbar) == 16
    assert all(q.name == "" for q in snap.items.quickbar)
    # item model shape
    for it in snap.items.items.values():
        assert it.name
        assert it.slot in {"p", "s1", "s2", "s3", "s4", "s5", "s6"} or isinstance(
            it.slot, int
        )

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
    assert any(any(b.name for b in m.buffs.values()) for m in snap.monsters.values())

    # abilities present
    assert isinstance(snap.abilities.skills, dict) and snap.abilities.skills
    assert isinstance(snap.abilities.spells, dict) and snap.abilities.spells

    # items + quickbar present
    assert isinstance(snap.items.items, dict) and snap.items.items
    assert len(snap.items.quickbar) >= 1

    # log present and has lines
    assert isinstance(snap.log.lines, list) and len(snap.log.lines) >= 1
    assert snap.log.total_round is None or snap.log.total_round >= 1

    # warnings empty and snapshot serializable
    assert snap.warnings == []
    _ = snap.as_dict()
    _ = snap.to_json()


def test_parse_fixture_2():
    html = read_fixture("The HentaiVerse3.htm")
    snap = parse_snapshot(html)

    # vitals
    assert 99.0 <= snap.player.hp_percent <= 100.0
    assert snap.player.hp_value == 23421
    assert 67.0 <= snap.player.mp_percent <= 69.0
    assert snap.player.mp_value == 1021
    assert 99.0 <= snap.player.sp_percent <= 100.0
    assert snap.player.sp_value == 1269
    assert snap.player.overcharge_value == 194

    # player buffs include spirit stance and a mix of timed/permanent
    pbuf = snap.player.buffs
    assert "Spirit Stance" in pbuf and pbuf["Spirit Stance"].is_permanent is True
    expect_some = {
        "Protection",
        "Haste",
        "Shadow Veil",
        "Spark of Life",
        "Spirit Shield",
    }
    assert expect_some.issubset(set(pbuf.keys()))
    # has at least one numeric-duration buff
    assert any(
        (b.remaining_turns >= 0) or (b.remaining_turns == float("inf"))
        for b in pbuf.values()
    )

    # abilities
    assert "Shield Bash" in snap.abilities.skills
    sb = snap.abilities.skills["Shield Bash"]
    assert (
        sb.available is True
        and sb.cost_type == "Overcharge"
        and sb.cost == 25
        and sb.cooldown_turns == 10
    )
    assert "Vital Strike" in snap.abilities.skills
    vs = snap.abilities.skills["Vital Strike"]
    assert (
        vs.available is False
        and vs.cost_type == "Overcharge"
        and vs.cost == 50
        and vs.cooldown_turns == 10
    )
    assert (
        "Fiery Blast" in snap.abilities.spells
        and snap.abilities.spells["Fiery Blast"].cost == 22
    )
    assert (
        "Cure" in snap.abilities.spells
        and snap.abilities.spells["Cure"].cost == 64
        and snap.abilities.spells["Cure"].cooldown_turns == 2
    )

    # monsters
    assert len(snap.monsters) == 6
    m1 = snap.monsters[1]
    assert (
        m1.name == "Yuki Nagato"
        and m1.alive is False
        and m1.hp_percent == 0.0
        and m1.mp_percent == 0.0
        and m1.sp_percent == 0.0
    )
    assert any(m.alive for m in snap.monsters.values())
    assert any(m.buffs for m in snap.monsters.values())
    # percentages sane for living monsters
    for m in snap.monsters.values():
        if m.alive:
            assert 0.0 <= m.hp_percent <= 100.0
            assert 0.0 <= m.mp_percent <= 100.0
            assert 0.0 <= m.sp_percent <= 100.0

    # log (reversed: most recent first)
    assert (
        snap.log.lines
        and snap.log.lines[0] == "You hit Ryouko Asakura for 17057 void damage."
    )

    # items
    items = snap.items.items
    assert items["spirit gem"].slot == "p" and items["spirit gem"].available is True
    assert items["health draught"].available is False
    assert items["health potion"].available is True
    assert items["mana draught"].available is False
    assert items["mana potion"].available is False
    assert items["mana elixir"].available is True
    assert items["spirit draught"].available is True
    assert items["spirit potion"].available is True
    assert items["spirit elixir"].available is True
    assert len(snap.items.quickbar) == 16 and all(
        q.name == "" for q in snap.items.quickbar
    )

    # warnings and serialization
    assert snap.warnings == []
    _ = snap.as_dict()
    _ = snap.to_json()


def test_parse_fixture_4():
    html = read_fixture("The HentaiVerse4.htm")
    snap = parse_snapshot(html)

    assert "spirit gem" in snap.items.items
    spirit_gem = snap.items.items["spirit gem"]
    assert spirit_gem.slot == "p"
    assert spirit_gem.available

    # vitals
    assert 98.0 <= snap.player.hp_percent <= 100.0
    assert snap.player.hp_value == 23295
    assert 71.0 <= snap.player.mp_percent <= 73.0
    assert snap.player.mp_value == 1083
    assert 99.0 <= snap.player.sp_percent <= 100.0
    assert snap.player.sp_value == 1272
    assert snap.player.overcharge_value == 230

    # no spirit stance
    assert "Spirit Stance" not in snap.player.buffs
    # has Overwhelming Strikes stack notation
    assert any(k.startswith("Overwhelming Strikes") for k in snap.player.buffs.keys())

    # abilities samples
    assert snap.abilities.skills["Shield Bash"].available is True
    assert snap.abilities.skills["Vital Strike"].available is True
    assert snap.abilities.spells["Fiery Blast"].cost == 29
    ab_absorb = snap.abilities.spells["Absorb"]
    assert (
        ab_absorb.available is False
        and ab_absorb.cost_type == "MP"
        and ab_absorb.cost == 128
        and ab_absorb.cooldown_turns == 20
    )

    # monsters and buffs
    assert len(snap.monsters) == 5
    # At least one monster has a system type; Mikuru Asahina is defined as Legendary in mapping
    assert any(m.system_monster_type for m in snap.monsters.values())
    assert (
        snap.monsters[5].name == "Mikuru Asahina"
        and snap.monsters[5].system_monster_type == "Legendary"
    )
    assert any("Stunned" in m.buffs for m in snap.monsters.values())
    for m in snap.monsters.values():
        assert m.alive is True
        assert 0.0 < m.hp_percent <= 100.0
        assert 0.0 <= m.mp_percent <= 100.0
        assert 0.0 <= m.sp_percent <= 100.0

    # log and items
    assert (
        snap.log.lines
        and "You hit Mikuru Asahina for 9793 void damage."
        in {snap.log.lines[0], snap.log.lines[-1]}
        or "You hit Mikuru Asahina for 9793 void damage." in snap.log.lines
    )
    it = snap.items.items
    assert it["health draught"].available is True
    assert it["health potion"].available is True
    assert it["health elixir"].available is True
    assert it["mana draught"].available is False
    assert it["mana potion"].available is True
    assert it["mana elixir"].available is True
    assert it["spirit draught"].available is True
    assert it["spirit potion"].available is True
    assert it["spirit elixir"].available is True
    assert len(snap.items.quickbar) == 16 and all(
        q.name == "" for q in snap.items.quickbar
    )

    assert snap.warnings == []
    _ = snap.as_dict()
    _ = snap.to_json()


def test_parse_fixture_5():
    html = read_fixture("The HentaiVerse5.htm")
    snap = parse_snapshot(html)

    assert "scroll of the avatar" in snap.items.items
    avatar_scroll = snap.items.items["scroll of the avatar"]
    assert avatar_scroll.slot == "s1"
    assert avatar_scroll.available
    assert not snap.items.items["scroll of the gods"].available

    # vitals
    assert 98.0 <= snap.player.hp_percent <= 100.0
    assert snap.player.hp_value == 38267
    assert 99.0 <= snap.player.mp_percent <= 100.0
    assert snap.player.mp_value == 2434
    assert 99.0 <= snap.player.sp_percent <= 100.0
    assert snap.player.sp_value == 2474
    assert snap.player.overcharge_value == 16

    # buffs present, no spirit stance
    assert "Spirit Stance" not in snap.player.buffs
    assert {
        "Protection",
        "Haste",
        "Shadow Veil",
        "Spark of Life",
        "Spirit Shield",
    }.issubset(set(snap.player.buffs))

    # abilities include higher-tier spells; some skills disabled
    spells = snap.abilities.spells
    for n in [
        "Flames of Loki",
        "Fimbulvetr",
        "Wrath of Thor",
        "Storms of Njord",
        "Paradise Lost",
        "Ragnarok",
    ]:
        assert n in spells
    assert (
        spells["Fiery Blast"].cost == 36
        and spells["Cure"].cost == 120
        and spells["Cure"].cooldown_turns == 2
    )
    assert (
        spells["Absorb"].available is True
        and spells["Absorb"].cost == 180
        and spells["Absorb"].cooldown_turns == 20
    )
    assert snap.abilities.skills["Shield Bash"].available is False
    assert snap.abilities.skills["Vital Strike"].available is False
    assert snap.abilities.skills["Merciful Blow"].available is False

    # monsters
    assert len(snap.monsters) == 6
    m1 = snap.monsters[1]
    assert {"Stunned", "Deep Burns"}.issubset(set(m1.buffs))
    assert (
        snap.monsters[6].name == "Thundaga"
        and "Penetrated Armor" in snap.monsters[6].buffs
    )
    for m in snap.monsters.values():
        assert m.alive is True
        assert 0.0 < m.hp_percent <= 100.0
        assert 0.0 <= m.mp_percent <= 100.0
        assert 0.0 <= m.sp_percent <= 100.0

    # log
    assert (
        snap.log.lines
        and snap.log.lines[0] == "You crit Thundaga for 7327 void damage."
    )

    # items
    it = snap.items.items
    assert it["health draught"].available is True
    assert it["mana draught"].available is True
    assert it["spirit draught"].available is True
    assert it["last elixir"].available is False
    assert len(snap.items.quickbar) == 16 and all(
        q.name == "" for q in snap.items.quickbar
    )

    # warnings and serialization
    assert snap.warnings == []
    _ = snap.as_dict()
    _ = snap.to_json()


def test_parse_fixture_sprite():
    """Test CSS-sprite UI variant (anti-scraping version)."""
    html = read_fixture("The HentaiVerse6.html")
    snap = parse_snapshot(html)

    # vitals (sprite version uses dvrhb instead of dvrhd)
    assert 86.0 <= snap.player.hp_percent <= 87.0
    assert snap.player.hp_value == 2243
    assert 48.0 <= snap.player.mp_percent <= 49.0
    assert snap.player.mp_value == 101
    assert 52.0 <= snap.player.sp_percent <= 53.0
    assert snap.player.sp_value == 60
    assert snap.player.overcharge_value == 115

    # buffs
    pbuf = snap.player.buffs
    assert "Spirit Stance" in pbuf
    assert "Protection" in pbuf and pbuf["Protection"].is_permanent
    assert "Haste" in pbuf and pbuf["Haste"].is_permanent
    assert "Regen" in pbuf and pbuf["Regen"].remaining_turns == 16.0

    # abilities: names extracted from onmouseover
    assert "Flee" in snap.abilities.skills
    assert "Shield Bash" in snap.abilities.skills
    sb = snap.abilities.skills["Shield Bash"]
    assert sb.available is True
    assert sb.cost_type == "Overcharge" and sb.cost == 25 and sb.cooldown_turns == 10

    assert "Fiery Blast" in snap.abilities.spells
    assert snap.abilities.spells["Fiery Blast"].cost == 6
    assert "Cure" in snap.abilities.spells
    cure = snap.abilities.spells["Cure"]
    assert cure.cost == 19 and cure.cooldown_turns == 2
    assert snap.abilities.spells["Absorb"].available is False

    # monsters: names decoded from CSS sprites
    assert len(snap.monsters) == 6
    names = {m.name for m in snap.monsters.values()}
    assert "Saw World New New" in names
    assert "Sleeping Dragon" in names
    assert "Blue Slime" in names
    assert "Scary Ghost" in names
    # alive/dead
    assert snap.monsters[1].alive is False  # Saw World New New
    assert snap.monsters[5].alive is True  # Scary Ghost
    assert snap.monsters[5].hp_percent == 100.0
    assert snap.monsters[6].alive is True  # Low-Grade Farmer 153
    for m in snap.monsters.values():
        if m.alive:
            assert 0.0 <= m.hp_percent <= 100.0
            assert 0.0 <= m.mp_percent <= 100.0

    # items: names decoded from CSS sprites
    it = snap.items.items
    assert "mana gem" in it and it["mana gem"].slot == "p"
    assert it["mana gem"].available
    assert "health potion" in it and it["health potion"].available is True
    assert "health draught" in it and it["health draught"].available is False
    assert "mana potion" in it and it["mana potion"].available is True
    assert "mana draught" in it and it["mana draught"].available is False
    assert "spirit potion" in it and it["spirit potion"].available is True
    assert "spirit draught" in it and it["spirit draught"].available is False

    # log (plain text, works the same)
    assert snap.log.current_round == 12
    assert snap.log.total_round == 1000
    assert snap.log.lines[0].startswith("Initializing Grindfest")

    # quickbar
    assert len(snap.items.quickbar) == 16

    # no warnings, serializable
    assert snap.warnings == []
    _ = snap.as_dict()
    _ = snap.to_json()
