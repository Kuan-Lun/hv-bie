# Testing Guidelines

本文件為測試相關的 AI Agent 提供 HV-BIE 專案之測試指導，對齊 `SRS.md` 中的 FR/NFR。

## 測試策略

### 測試組織

- 為新功能編寫對應的單元測試與整合測試
- 對照 SRS 功能：Vitals、Buffs、Abilities、Monsters、Log、Items、Snapshot 聚合
- 將測試放在 `tests/` 目錄（pytest 標準），避免與原始碼混雜

### 測試類型

#### 單元測試（parsers/*）

- 驗證各解析器對樣本 HTML 的正確性
- 測試邊界條件（缺漏節點、非預期 class、空 HTML）
- 驗證警告收集行為（不丟未捕捉例外）

#### 整合測試（parse_snapshot）

- 以整頁 HTML 字串呼叫 `parse_snapshot`
- 斷言輸出型別與鍵名穩定（符合資料模型）
- 覆核怪物系統稀有度標記、回合資訊與清單數量

#### 效能測試（選配）

- 粗略量測單頁解析耗時，目標 ≲ 50ms（一般桌機）
- 檢查不必要的多次 DOM 解析或重複遍歷

## 測試實作規範

### 測試檔案結構（建議）

```text
tests/
├── test_parse_vitals.py
├── test_parse_buffs.py
├── test_parse_abilities.py
├── test_parse_monsters.py
├── test_parse_log.py
├── test_parse_items.py
└── test_snapshot_integration.py
```

### 命名與可讀性

- 測試函數英文命名，表達情境與預期，例如：`test_vitals_parses_percent_and_values`
- 測試內以繁體中文註解說明目的與假設
- 合理拆分多情境，以維持單測試原子性

### 斷言與驗證

- 使用 pytest 斷言，必要時自訂 helper 驗證資料模型
- 驗證成功與失敗/缺漏兩種路徑
- 驗證 `warnings` 內容在不完整頁面下會出現

## 測試資料

- 使用本庫提供的樣本 HTML（位於 `tests/fixtures/hv/The HentaiVerse*.htm` 與對應的 `*_files/` 資源資料夾）
- 保持每個 `.htm` 與其對應的 `*_files/` 為相鄰同層，以確保 HTML 內相對資源路徑可用
- 測試程式以專案根目錄為基準組合路徑（避免硬編碼絕對路徑），統一使用 `utf-8` 讀取
- 建議以 fixtures 讀取樣本，集中重用（見下方示例）

範例資料夾結構（節錄）：

```text
tests/
└── fixtures/
 └── hv/
  ├── The HentaiVerse.htm
  ├── The HentaiVerse_files/
  ├── The HentaiVerse1.htm
  └── The HentaiVerse1_files/
```

Pytest fixture 範例（集中載入樣本 HTML）：

```python
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]  # 指向 tests/
FIXTURES = ROOT / "fixtures" / "hv"

@pytest.fixture
def hv_html_loader():
 """以名稱載入 HV 樣本 HTML，例如：loader("The HentaiVerse1")"""
 def loader(name: str) -> str:
  return (FIXTURES / f"{name}.htm").read_text(encoding="utf-8")
 return loader

# 使用示例
def test_snapshot_integration_basic(hv_html_loader):
 html = hv_html_loader("The HentaiVerse")
 # parse_snapshot(html) 並進行斷言...
```

- 若需新增樣本，請將來源與目的文件化（避免敏感資訊）
- 將重複使用的 HTML 讀取邏輯抽至測試 fixtures

## 持續整合

- 確保測試在 CI/本機能穩定執行，無外部網路依賴
- 測試需具等冪性，避免使用全域可變狀態
- 如採用 coverage，維持關鍵解析路徑覆蓋

## 特殊注意事項

- 不進行任何對目標網站的請求；所有測試以本地樣本 HTML 為主
- 避免解析器中的 sleep/等待等非必要延遲
- 將解析告警視為行為的一部分進行驗證
