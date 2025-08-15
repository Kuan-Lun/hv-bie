# HV-BIE API 規格書（API Specification）

本文件定義套件 hv_bie 對外可用的程式介面（Public API）與資料模型契約。

- 套件名稱：hv_bie（HV Battle Intelligence Extractor）
- 目的：將 HentaiVerse 戰鬥頁面的 HTML 字串解析為結構化的 Python dataclasses
- 主要相依：beautifulsoup4（bs4）
- Python 版本：3.13+
- 參考文件：[`SRS.md`](/SRS.md)

---

## 公開 API 一覽

最低穩定介面：

```python
from hv_bie import parse_snapshot
from hv_bie.types.models import BattleSnapshot

snapshot = parse_snapshot(html: str)  # -> BattleSnapshot
```

- `parse_snapshot(html: str) -> BattleSnapshot`
  - 自單一戰鬥 HTML（字串）產生一次「戰鬥快照」。
  - 保證容錯：若網頁某區塊缺漏，函式不會拋出例外，改以「預設值」並記錄警告（warnings）。

資料模型（回傳型別）定義見「資料模型契約」。

---

## 安裝與相依

- Python 3.13+
- 依賴：`beautifulsoup4>=4.13.4`

---

## 介面行為與契約

### parse_snapshot(html: str) -> BattleSnapshot

- 輸入
  - `html`: 單一 HV 戰鬥頁面之 HTML 原始碼字串。
- 輸出
  - `BattleSnapshot`（見下方「資料模型契約」）。
- 容錯與警告（重要）
  - 不因缺漏 DOM 區塊而拋例外；會在 `BattleSnapshot.warnings` 陣列中加入說明字串（例如：`"pane_vitals not found"`, `"table_skills not found"` 等）。
- 一致性
  - 以同一份 HTML 輸入，所有子解析結果（玩家、技能/法術、怪物、戰報、道具）在同一快照中彼此一致。

實作出處：`hv_bie/snapshot.py`（聚合各解析器於 `hv_bie/parsers/core.py`）。

---

## 資料模型契約（Dataclasses）

資料類型定義於 `hv_bie/types/models.py`。下列內容視為「對外契約」：鍵名、型別、語意與允許值範圍皆需維持穩定。

### BattleSnapshot

- 欄位
  - `player: PlayerState`
  - `abilities: AbilitiesState`
  - `monsters: dict[int, Monster]`（以怪物插槽/索引作為鍵）
  - `log: CombatLog`
  - `items: ItemsState`
  - `warnings: list[str]`（解析告警訊息）

- 輔助方法
  - `as_dict() -> dict`：遞迴轉為 `dict`（適合序列化）
  - `to_json() -> str`：輸出 JSON 字串（`ensure_ascii=False`）

### PlayerState

- 欄位（皆有預設值，以利缺漏時填補）
  - `hp_percent: float`（0.0–100.0）
  - `hp_value: int`
  - `mp_percent: float`（0.0–100.0）
  - `mp_value: int`
  - `sp_percent: float`（0.0–100.0）
  - `sp_value: int`
  - `overcharge_value: int`（整數 OC 值）
  - `buffs: dict[str, Buff]`（以 Buff 名稱為鍵）

### Buff

- 欄位
  - `name: str`
  - `remaining_turns: float | None`（秒/回合等數值；若為自動施放/永久則為 `None` 並搭配 `is_permanent=True`）
  - `is_permanent: bool`

### AbilitiesState

- 欄位
  - `skills: dict[str, Ability]`（以技能顯示名稱為鍵）
  - `spells: dict[str, Ability]`（以法術顯示名稱為鍵）

### Ability

- 欄位
  - `name: str`
  - `available: bool`（是否可用）
  - `cost: int`（資源成本；對於 Overcharge 以 25 點/charge 換算到整數 OC 點）
  - `cost_type: str | None`（可能值：`"MP"`、`"Overcharge"`、或 `None`）
  - `cooldown_turns: int`（冷卻回合數）

解析規則摘要（來自 `parsers/core.py`）：

- 可用狀態：以樣式 `opacity:0.5` 判斷禁用。
- 成本推斷：依 onmouseover 文本數值組態判斷 `MP` 與 `Overcharge`；OC 以 25 點/charge 計算。

### Monster

- 欄位
  - `slot_index: int`（怪物插槽序號）
  - `name: str`（顯示名稱；可能為一般名稱或裝備名等）
  - `alive: bool`（是否存活）
  - `system_monster_type: str | None`（若為系統怪物，可能值：`"Rare"` / `"Legendary"` / `"Ultimate"`）
  - `hp_percent: float`（0.0–100.0；若死亡則為 0.0）
  - `mp_percent: float`（0.0–100.0；若死亡則為 0.0）
  - `sp_percent: float`（0.0–100.0；若死亡則為 0.0）
  - `buffs: dict[str, Buff]`

備註：

- 系統怪物類型主要以名稱對照表判斷（見 `hv_bie/types/system_monsters.py`），若無法辨識則回傳 `None`；部分情況會以樣式啟發式標示為 `"Rare"`。

### CombatLog

- 欄位
  - `lines: list[str]`
  - `current_round: int | None`
  - `total_round: int | None`

- 順序約定
  - 解析後之 `lines` 以「由舊到新（最早 -> 最新）」順序提供（索引 0 為最早）。

### ItemsState

- 欄位
  - `items: dict[str, Item]`（以道具顯示名稱為鍵）
  - `quickbar: list[QuickSlot]`（快捷列槽位，名稱可能為空字串）

### Item

- 欄位
  - `slot: str | int`（可能值：`"p"`、`"s1".."s6"`、或整數槽位）
  - `name: str`
  - `available: bool`（是否可用）

### QuickSlot

- 欄位
  - `slot: str | int`
  - `name: str`（在現有樣本中，快捷列名稱為空字串）

---

## 例外與錯誤處理

- `parse_snapshot` 對於缺漏或不可解析的區塊不拋出例外，改以「預設值」並在 `warnings` 記錄文字訊息。
- 可能的告警（非詳盡）：
  - `"pane_vitals not found"`, `"hp bar width missing"`
  - `"table_skills not found"`, `"table_magic not found"`
  - `"pane_monster not found"`, `"textlog not found"`, `"pane_item not found"`, `"quickbar not found"`
- 呼叫端應：
  - 檢查 `warnings` 以利觀測缺漏情形。
  - 對於缺漏資料（例如百分比 0.0、空集合），自行決定後續流程（忽略、重試、記錄）。

---

## 使用範例

```python
from hv_bie import parse_snapshot

html = load_html_somehow()  # e.g., from a file you saved previously
snap = parse_snapshot(html)

# 讀取玩家資訊
print(snap.player.hp_value, snap.player.hp_percent)
print("Spirit Stance" in snap.player.buffs)

# 讀取技能/法術
for name, sk in snap.abilities.skills.items():
    print(name, sk.available, sk.cost_type, sk.cost, sk.cooldown_turns)

# 讀取怪物與其 Buff
for idx, m in snap.monsters.items():
    print(idx, m.name, m.alive, m.system_monster_type, m.hp_percent)
    print("buffs:", list(m.buffs))

# 戰報（由新到舊）
print(snap.log.current_round, "/", snap.log.total_round)
print(snap.log.lines[0], "->", snap.log.lines[-1])

# 道具與快捷列
print("Health Draught" in snap.items.items)
print(len(snap.items.quickbar))

# 輸出 JSON
print(snap.to_json())
```

---

## 輔助模組（選擇性公開知識）

`hv_bie/types/system_monsters.py`：提供系統怪物名稱到稀有度（`Rare`/`Legendary`/`Ultimate`）的對照表與查詢函式：

```python
from hv_bie.types.system_monsters import get_system_monster_type
kind = get_system_monster_type(name)  # -> 'Rare' | 'Legendary' | 'Ultimate' | None
```

- 名稱比對採大小寫不敏感（`casefold()`）。
- 對照清單可隨版本擴充；若未知則回傳 `None`。解析器在必要時以樣式啟發式補充為 `"Rare"`（最佳努力）。

---

## 相容性與穩定性

- 資料模型鍵名與型別視為穩定契約；維護時需保持向後相容（新增欄位需提供預設值）。
- 版本對應：`pyproject.toml` 中目前版本為 `0.2.0`（未來更新請於此處同步說明）。
- 效能目標與更多非功能性需求，請參閱 [`SRS.md`](/SRS.md)（例：NFR-P1 效能、NFR-R1 容錯）。

---

## 測試對應與驗證

- 單元測試：`tests/unit/test_parsers.py` 檢查各子解析器（Vitals/Buffs/Abilities/Monsters/Log/Items）。
- 整合測試：`tests/unit/test_snapshot_integration.py` 驗證 `parse_snapshot` 的整體結構與序列化（`as_dict`, `to_json`）。
- 測試用 HTML 樣本：`tests/fixtures/hv/`。

---

## 與 SRS 的關聯

- 本 API 規格對應 [`SRS.md`](/SRS.md) 中的：
  - 功能性需求 FR-1 ~ FR-7（玩家、Buff、技能/法術、怪物、戰報、道具、整體快照）。
  - 非功能性需求 NFR（容錯、效能、可維護性、可攜性、安全性）。
- 若需更完整的業務語意、名詞定義與風險評估，請直接參考 [`SRS.md`](/SRS.md) 對應章節。

---

## 變更紀錄（摘要）

- 初版（對應程式碼 v0.2.0）：建立 `parse_snapshot` 單一入口；資料模型如上；`warnings` 為容錯訊息匯總；戰報行列提供由舊到新的順序。
