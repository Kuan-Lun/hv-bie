# 版本更新

適用於 Python 套件（hv_bie）的版本管理與釋出說明維護，面向 PyPI 發布流程。

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

完成後建立並推送標籤：`git tag v{新版本}`，`git push --tags`。

## 備註

- 發布至 PyPI 並不要求 GitHub Releases；如需對外展示版本頁或附加資產，可另行建立 Releases（可選）。
