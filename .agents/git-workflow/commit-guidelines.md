# 提交訊息規範

## 提交前檢查流程

在編寫提交訊息之前，請依序執行以下命令：

1. `git log --oneline -30` - 瀏覽最近 30 筆提交訊息，了解整體格式與風格
2. `git log -15` - 查看最近 15 筆提交的詳細訊息，學習撰寫技巧與慣例
3. `git status` - 確認已修改的檔案清單及其狀態
4. `git diff <file>` - 檢查每個檔案的具體修改內容

## 提交訊息格式

```text
<type>(scope): <description>

[optional body]

[optional footer]
```

### 類型（Type）

- `feat` - 新功能
- `fix` - 錯誤修復
- `docs` - 文件修改
- `style` - 程式碼格式調整（不影響邏輯）
- `refactor` - 程式碼重構（不新增功能也不修正錯誤）
- `test` - 新增或修改測試
- `chore` - 建構流程或輔助工具變更
- `perf` - 效能優化

### 範圍（Scope）

請使用有意義的範圍名稱，表示受影響的模組或元件：

- `parsers` - HTML 解析器相關
- `types` - 資料類別/型別定義
- `snapshot` - 聚合入口/快照組裝
- `perf` - 效能最佳化
- `tests` - 測試相關
- `docs` - 文件相關

### 描述（Description）

- 使用英文撰寫，簡潔明瞭
- 採用祈使語氣（如 "add"，非 "adds" 或 "added"）
- 不要以大寫字母開頭
- 不要以句號結尾
- 限制在 50 字元以內

#### 具體性（Specificity）

- 主旨需具體點出此次修改的「內容與重點」；盡量包含被影響的檔案、章節或主題名稱（如 version、branch-mgmt、release、git-workflow）。
- 若主旨長度限制無法完整表達，請在 body 以 1–3 個條列補充「做了什麼／為什麼」與關鍵影響。
- 文件／政策性變更，優先使用能辨識主題的 scope，例如：`version`、`branch-mgmt`、`release`、`git-workflow`。

#### 文件（docs）提交範例

- Good: `docs(version): clarify bump/changelog/tag process`
- Good: `docs(branch-mgmt): define naming and protection rules`
- Bad: `docs(git-workflow): update docs`
- Bad: `docs: update`

簡短 body 範例（當主旨不敷表達時）：

```text
docs(version): clarify bump/changelog/tag process

- add pre-release checks
- separate atomic commits for version and changelog
- recommend annotated tagging and push steps
```

#### 原子性提交

- 根據檔案差異與修改內容撰寫提交訊息
- 若修改多個檔案，請依類型（feat、fix、docs、style、refactor、test、chore）分組，分別提交
- 每次提交應代表一個邏輯變更單元
- 避免在同一提交中混合不同類型的修改

#### 多類型修改處理

當涉及多種類型的修改時，請依照以下流程：

1. 建立臨時分支
2. 完成所有程式碼修改
3. 按類型分別提交
4. 使用 `git merge --no-ff` 合併回主分支
5. 清理 AI 建立的分支（僅刪除 AI 建立的分支，不刪除使用者建立的分支）

**格式說明**：請使用圓括號 `(scope)`，而非方括號 `[scope]`，例如：

- 正確：`feat(matrix): add eigenvalue calculation`
- 正確：`fix(johansen): correct statistical test logic`
- 錯誤：`feat[matrix]: add eigenvalue calculation`
