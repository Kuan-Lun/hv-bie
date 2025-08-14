from bs4 import BeautifulSoup

from hv_bie.parsers import parse_vitals


def test_vitals_parses_percent_and_values(hv_html_loader):
    html = hv_html_loader("The HentaiVerse")
    soup = BeautifulSoup(html, "html.parser")
    player, warnings = parse_vitals(soup)

    assert player.hp_value == 23618
    assert player.mp_value == 1595
    assert player.sp_value == 1317
    assert player.overcharge_value == 0
    assert player.hp_percent == 100.0
    assert player.mp_percent == 100.0
    assert player.sp_percent == 100.0
    assert warnings == []
