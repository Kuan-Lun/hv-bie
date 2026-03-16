# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hv-bie** is a Python library that parses HentaiVerse battle HTML pages into structured dataclasses. Single public API: `parse_snapshot(html: str) -> BattleSnapshot`.

## Commands

```bash
# Install for development
uv pip install -e ".[dev]"

# Run all tests
uv run pytest -q

# Run a single test file
uv run pytest tests/unit/test_parsers.py -q

# Lint
uv run ruff check hv_bie tests

# Type check
uv run mypy hv_bie

# Format
uv run black hv_bie tests
```

## Architecture

```
HTML string → parse_snapshot() → BattleSnapshot dataclass
```

`parse_snapshot()` in `hv_bie/snapshot.py` orchestrates six sub-parsers from `hv_bie/parsers/core.py`:

| Sub-parser | Output |
|---|---|
| `parse_player_vitals()` | `PlayerState` (HP/MP/SP/Overcharge percentages + values) |
| `parse_player_buffs()` | `dict[str, Buff]` |
| `parse_abilities()` | `AbilitiesState` (skills + spells dicts) |
| `parse_monsters()` | `dict[int, Monster]` (keyed by slot index) |
| `parse_log()` | `CombatLog` (lines oldest→newest, round info) |
| `parse_items()` | `ItemsState` (items + quickbar) |

All sub-parsers accept a `warnings: list[str]` parameter and append diagnostic messages rather than raising exceptions. The library never raises on missing DOM sections — it fills defaults and records warnings.

Data models are immutable dataclasses in `hv_bie/types/models.py`. `BattleSnapshot` has `as_dict()` and `to_json()` serialization methods.

## Key Parsing Details

- **CSS sprite decoding**: HV obfuscates text via CSS sprites. `_decode_sprite_text()` and `_extract_name()` handle both plaintext and sprite UI variants.
- **Width-to-percent conversion**: Player bar = 414px at 100%, monster bar = 120px at 100%.
- **Data extraction**: Uses regex on `onmouseover` attributes and style hints (border-color, background, opacity) as heuristic fallbacks.
- **Monster classification**: `hv_bie/types/system_monsters.py` maps monster names to rarity types via case-insensitive lookup.

## Documentation Sync

When modifying code (adding/changing/removing features, fields, or API behavior), **must** also update:
- `SRS.md` — Software Requirements Specification
- `API_SPEC.md` — Public API contract

Both documents are written in Traditional Chinese. Keep them consistent with the actual code.

## Design Principles (SOLID)

- **Single Responsibility**: Each sub-parser handles exactly one DOM section. Models (`types/`) are separate from parsing logic (`parsers/`).
- **Open/Closed**: Add new parsers or model fields without modifying existing sub-parsers. The warning system is extensible by appending, not by changing control flow.
- **Liskov Substitution**: All dataclass outputs conform to their type contracts — callers rely on the interface, not implementation details.
- **Interface Segregation**: Consumers import only `parse_snapshot()` from the public API. Internal modules expose fine-grained functions (`parse_player_vitals`, `parse_monsters`, etc.) so callers need not depend on the full pipeline.
- **Dependency Inversion**: `snapshot.py` (high-level orchestration) depends on parser function signatures, not on concrete DOM traversal details. Models define the data contract; parsers produce it.

When adding or refactoring code, follow these principles: keep each module/function focused on one concern, extend via new functions rather than modifying existing ones, and ensure high-level modules depend on abstractions (dataclass contracts) rather than low-level parsing internals.

## Code Style

- **Formatter**: Black (88 char line length)
- **Linter**: Ruff with isort (I) enabled, E501 ignored
- **Type checking**: mypy (strict=False, ignore_missing_imports=True)
- **Python**: 3.9+ compatibility required
- **Sole runtime dependency**: beautifulsoup4
- **Documentation**: README, API_SPEC, and SRS are in Traditional Chinese; code comments/identifiers are in English

## Testing

- **Unit tests**: `tests/unit/test_parsers.py` — individual parser functions
- **Integration tests**: `tests/unit/test_snapshot_integration.py` — full snapshot + serialization
- **Performance tests**: `tests/perf/test_nfr_p1_performance.py` — parsing must complete in <50ms
- **Fixtures**: Real HV battle HTML samples in `tests/fixtures/hv/`

## CI/CD

Publishing to PyPI is automated via `.github/workflows/publish.yml` — triggers on push to main when the version in `pyproject.toml` is bumped. Uses OIDC trusted publishing (no API keys).
