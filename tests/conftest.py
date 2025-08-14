import pathlib
import sys
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
FIXTURES = ROOT / "tests" / "fixtures" / "hv"


@pytest.fixture
def hv_html_loader():
    """Load HV sample HTML by name."""

    def loader(name: str) -> str:
        return (FIXTURES / f"{name}.htm").read_text(encoding="utf-8")

    return loader
