# Agents

AI agents and automated tools for this repository follow project-specific guidelines to keep changes aligned with the SRS and Python packaging goals.

## Purpose

Document AI agent interactions, configurations, and best practices for maintaining and developing the HV Battle Intelligence Extractor (HV-BIE) Python package.

## Agent Guidelines Index

本文件已分割為多個專門化的指導文件，以減少上下文閱讀量並便於添加詳細要求。AI Agent 應根據具體任務類型閱讀相應的指導文件：

### 按任務類型分類的指導文件

- **[程式碼生成與實作](/.agents/code-generation.md)** - 用於程式碼編寫、重構、新功能實作（依 SRS 中的資料模型與 API）
- **[測試相關](/.agents/testing.md)** - 用於編寫測試、驗證功能、測試驅動開發（pytest）
- **Git 工作流程** - 用於版本控制、分支管理、提交訊息
  - [分支管理](/.agents/git-workflow/branch-management.md)
  - [提交訊息規範](/.agents/git-workflow/commit-guidelines.md)
  - [版本更新](/.agents/git-workflow/version-update.md)
  - [程式碼審查準備](/.agents/git-workflow/code-review.md)
  - [協作規範](/.agents/git-workflow/collaboration.md)
  - [特殊注意事項](/.agents/git-workflow/special-notes.md)
- **[文件編寫](/.agents/documentation.md)** - 用於文件更新、API 文件、註解規範
- **[效能最佳化](/.agents/performance.md)** - 用於效能分析、最佳化建議、基準測試（解析耗時目標）

### 使用指南

1. **識別任務類型** - 確定當前任務屬於哪個類別
2. **閱讀對應指導** - 只閱讀相關的指導文件，減少不必要的上下文
3. **遵循具體規範** - 按照專門指導文件中的詳細要求執行
4. **組合使用** - 複雜任務可能需要參考多個指導文件

## 快速參考

### 專案概要（依 SRS.md）

- Python 套件：`hv_bie`，提供 `parse_snapshot(html: str) -> BattleSnapshot`
- 目的：從 HentaiVerse 戰鬥頁面 HTML 字串解析出結構化資料（玩家/怪物/技能/戰報/道具）
- 執行環境：Python 3.13+
- 依賴：`beautifulsoup4`（bs4）
- 交付：可發佈至 PyPI 的第三方套件

### 語言與訊息規範

- 使用者面向訊息與 API 文件：英文
- 內部實作註解：繁體中文
- Git 提交訊息：英文

### 程式碼品質與風格

- 使用型別註解與 `dataclasses` 定義公開資料模型
- 建議工具：Black（格式化）、Ruff（lint）、Mypy（型別檢查）
- 嚴禁：在解析過程進行任何網路請求或執行 HTML 腳本

### 測試與驗收

- 測試框架：pytest；對照 SRS 的 FR/NFR 撰寫測試
- 以樣本 HTML（本庫提供）驗證各解析器與整合輸出
- 效能目標：單頁解析平均 ≲ 50ms（一般桌機，作為指引值）

## 更新指南

當需要增加新的指導內容時：

1. 確定內容歸屬的類別
2. 更新對應的專門指導文件
3. 如需要新類別，建立新的指導文件
4. 在本文件中新增索引鏈接

## Notes

This modular approach keeps agents focused and consistent with the SRS, reducing context overhead while covering coding, testing, performance, docs, and Git workflow for a Python parsing library.
