from hv_bie import parse_snapshot
from hv_bie.types import BattleSnapshot


def test_snapshot_integration_basic(hv_html_loader):
    html = hv_html_loader("The HentaiVerse")
    snapshot = parse_snapshot(html)

    assert isinstance(snapshot, BattleSnapshot)
    assert snapshot.player.hp_value == 23618
    assert snapshot.player.mp_percent == 100.0
    assert snapshot.abilities.skills == []
    assert snapshot.warnings == []
