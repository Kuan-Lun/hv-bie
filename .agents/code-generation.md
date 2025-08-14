# Code Generation Guidelines

本文件為程式碼生成相關的 AI Agent 提供 HV-BIE（Python 套件）之實作指導。請以 `SRS.md` 為契約來源，所有對外資料結構與 API 必須符合 SRS。

## Python 專案規範

### 基本原則

- 遵循 Python 最佳實作與 PEP8/PEP20 精神
- 與現有程式碼風格一致，強制使用型別註解
- 公開資料模型使用 `@dataclass` 並保持鍵名/型別穩定
- 單一職責與清晰模組邊界（parsers/, types/）

### 程式碼註解與語言

- 使用者面向訊息與 docstring：英文
- 內部實作與解析細節註解：繁體中文
- 公開 API 使用清楚的 docstring（可含簡短範例）

### 錯誤處理與警告

- 解析缺漏或不一致時，不丟未捕捉例外：回傳預設值/空集合並收集警告字串（見 SRS NFR-R1）
- 不執行任何 HTML/JS 腳本，不進行網路請求（SRS NFR-S1/S2）
- 嚴禁以副作用修改輸入字串；純函式式解析

### 品質工具（建議）

- 格式化：Black
- Lint：Ruff（包含 flake8/pycodestyle 規則）
- 型別：Mypy（Python 3.13 模式）

## 專案特定要求（依 SRS）

### 解析輸入與輸出

- 輸入：`html: str`
- 主要輸出：`BattleSnapshot`（含 `player/abilities/monsters/log/items/warnings`）
- 選配方法：`as_dict()`, `to_json()`

### 模組與檔案結構（建議）

- `hv_bie/types/`：資料類別定義（dataclasses + typing）
- `hv_bie/parsers/`：各區塊解析器（vitals.py, buffs.py, abilities.py, monsters.py, log.py, items.py）
- `hv_bie/__init__.py`：`parse_snapshot` 聚合入口

### 解析策略原則

- 以 BeautifulSoup（bs4）解析 DOM；避免 fragile 的 CSS chain，保留容錯
- 對於百分比條或圖示，必要時允許近似與備援選擇器
- 保持解析器可重入，無全域可變狀態
- 對未知/新圖示：以人類可見文字為主，無法判斷時加入警告

### 效能與健壯性

- 目標：單頁解析平均 ≲ 50ms（參考值）；避免多次重複 DOM 遍歷
- 當節點缺失或格式偏差：以預設值處理，並記錄警告（aggregated warnings）

## 實作指導

### 資料模型契約（節錄）

- `parse_snapshot(html: str) -> BattleSnapshot`
- `BattleSnapshot` 需包含 SRS 指定欄位與型別；鍵名不得變動

### API 穩定性

- 任何變更公開型別或鍵名，需更新 SRS 與變更日誌（屬重大變更）

### 安全與相依

- 僅相依 `beautifulsoup4`；避免額外 heavyweight 相依
- 不讀取檔案、不進行 I/O；呼叫端提供 HTML 字串

### 交付與附帶品

- 提供最小 `pyproject.toml` 與 `README.md`（若建立套件目錄）
- 撰寫單元/整合測試（pytest）；覆蓋 FR-1 ~ FR-7

## 小技巧

- 遇到多種 DOM 版本：設計 fallback 解析路徑
- 將 CSS class 名稱映射集中管理，便於 DOM 改版時更新
- 將共通工具（如百分比解析、文字清理）抽出到 `parsers/utils.py`
