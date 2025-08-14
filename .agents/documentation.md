# Documentation Guidelines

本文件為文件編寫相關的 AI Agent 提供 HV-BIE（Python 套件）的文件指導。

## 文件編寫原則

### 內容品質

- 文件與程式碼更改同步（尤其是公開型別與鍵名）
- 提供清晰的使用範例（以 `parse_snapshot` 為中心）
- 記錄破壞性更改與遷移路徑
- 禁用表情符號於文件與提交訊息

### 語言規範

- 使用者面向文件：英文
- 內部技術文件：可使用繁體中文
- API 文件與錯誤訊息：英文
- 內部實作註解：繁體中文

## 程式碼註解規範（Python）

```python
def parse_snapshot(html: str) -> BattleSnapshot:
    """Parse one HentaiVerse battle HTML into a structured snapshot.

    Args:
        html: Raw HTML string of a battle page.

    Returns:
        BattleSnapshot with player, abilities, monsters, log, items, and warnings.
    """
    # 內部：解析流程說明（繁體中文），指出主要步驟與容錯策略
    ...
```

### 註解風格

- 公開 API 使用英文 docstring（含參數/回傳說明）
- 內部解析邏輯使用繁體中文行註解
- 複雜邏輯提供步驟化解釋，避免冗餘

## 文件維護

### 版本同步

- 任何公開資料模型/鍵名變更需更新 SRS 與 README/CHANGELOG
- 標記已棄用 API，提供遷移指南
- 維護變更日誌（語義化分類）

### 品質檢查

- 驗證 README 中的程式碼片段可執行
- 檢查連結有效性（相對路徑/錨點）
- 確保術語一致（與 SRS 對齊）
- 驗證技術準確性（依據樣本 HTML）

## 特殊要求

### 資料模型與 API 文件

- 列出 `BattleSnapshot` 與子型別欄位定義與語意（與 SRS 一致）
- 說明 `as_dict()` / `to_json()` 輔助方法

### 效能文件

- 簡述測試環境與樣本大小
- 提供解析耗時摘要與方法（非微觀 profiling）
- 如有最佳化變更，記錄前後差異
