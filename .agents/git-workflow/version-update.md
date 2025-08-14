# 版本更新

適用於 Python 套件（hv_bie）的版本管理與釋出說明維護，面向 PyPI 發布流程。

## 名詞定義

- 版本號（version）：程式庫的語意化版本號（例如 `1.2.3`），記錄在 `pyproject.toml` 或版本檔案中。
- 標籤（tag）：Git 上指向特定提交的標記，建議使用 `vX.Y.Z` 格式；可用附註標籤（annotated tag）。
- 釋出（release）：將某次變更以標籤定版；可選擇在 GitHub 建立 Releases 頁或上傳至 PyPI。

## 版本更新前的檢查

在更新版本號前，檢視自上一標籤以來的實際變更：

1. `git log --oneline v{上一版本}..HEAD` 檢視摘要
2. `git tag --list | findstr v{上一版本}` 確認標籤存在（Windows）
3. `git show --stat v{上一版本}..HEAD` 檢視變更統計

## 版本更新提交流程（SemVer）

進行兩個原子提交：

1. 版本號更新：

    - 若本庫已有 `pyproject.toml` 或版本檔案，更新其中的 `version`
    - 提交訊息：`chore(version): bump version from {old} to {new}`

2. 變更日誌更新（CHANGELOG）：

    - 編輯/新增 `CHANGELOG.md`，以實際提交與程式碼變更撰寫如下章節：
        - Breaking Changes
        - New Features
        - Bug Fixes
        - Refactoring/Improvements
        - Documentation
    - 提交訊息：`docs(changelog): update for {new}`

完成後建立並推送標籤（建議使用附註標籤 annotated tag）：
`git tag -a v{新版本} -m "Release: v{新版本}"`，`git push origin v{新版本}`。

### 實務命令範例

針對 CHANGELOG 更新後建立釋出提交與標籤（將 `vX.Y.Z` 替換為實際版本號）：

    ```bash
    git add CHANGELOG.md
    git commit -m "chore(release): vX.Y.Z"
    git tag -a vX.Y.Z -m "Release: vX.Y.Z"
    git push origin main
    git push origin vX.Y.Z
    ```

## 備註

- 發布至 PyPI 並不要求 GitHub Releases；如需對外展示版本頁或附加資產，可另行建立 Releases（可選）。
- 名詞一致性建議：提交訊息沿用慣例式類型（如 `chore(version)`, `docs(changelog)`），標籤訊息使用大寫 `Release: vX.Y.Z` 以便與一般提交區分。
