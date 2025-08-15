from __future__ import annotations

from pathlib import Path
from time import perf_counter
from statistics import fmean
import os

from hv_bie import parse_snapshot


# Locate fixtures and preload HTML strings so file I/O is excluded from timing
FIX = Path(__file__).resolve().parents[1] / "fixtures" / "hv"


def _read_fixture(name: str) -> str:
    return (FIX / name).read_text(encoding="utf-8")


def test_nfr_p1_parse_snapshot_performance():
    # Config: allow overriding via env var to accommodate slower CI
    runs = int(os.getenv("NFR_P1_RUNS", "10"))
    threshold_ms = float(os.getenv("NFR_P1_MS", "50"))  # target ~50ms

    # Preload HTML fixtures (exclude I/O from timing by design)
    names = [
        "The HentaiVerse.htm",
        "The HentaiVerse1.htm",
        "The HentaiVerse3.htm",
        "The HentaiVerse4.htm",
        "The HentaiVerse5.htm",
    ]
    htmls = [_read_fixture(n) for n in names]

    durations = []  # seconds per parse
    # Measure parse_snapshot only
    for html in htmls:
        for _ in range(runs):
            t0 = perf_counter()
            _ = parse_snapshot(html)
            t1 = perf_counter()
            durations.append(t1 - t0)

    avg_ms = fmean(durations) * 1000.0

    # Assert average meets NFR-P1 target (lenient default; configurable via env)
    assert (
        avg_ms <= threshold_ms
    ), f"NFR-P1 violated: avg parse_snapshot time {avg_ms:.2f} ms > {threshold_ms:.2f} ms (runs={runs}, samples={len(durations)})"
