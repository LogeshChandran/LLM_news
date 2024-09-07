
auto release
# Commit Message Guidelines

The following table shows how different types of commit messages will impact the version number according to Semantic Versioning (`major.minor.patch`) when using `semantic-release`:

| **Type**                  | **Example Commit Message**                                | **Current Version** | **New Version** |
|---------------------------|----------------------------------------------------------|---------------------|-----------------|
| **fix**                    | `fix: correct a typo`                                    | `0.0.0`             | `0.0.1`         |
| **feat**                   | `feat: add new feature`                                  | `0.0.0`             | `0.1.0`         |
| **docs**                   | `docs: update documentation`                             | `0.0.0`             | `0.0.0`         |
| **refactor**               | `refactor: refactor the codebase`                        | `0.0.0`             | `0.0.0`         |
| **chore**                  | `chore: update dependencies`                             | `0.0.0`             | `0.0.0`         |
| **perf**                   | `perf: improve performance of feature`                   | `0.0.0`             | `0.0.1`         |
| **test**                   | `test: add unit tests`                                   | `0.0.0`             | `0.0.0`         |
| **chore**                  | `chore: automate build script`                           | `0.0.0`             | `0.0.0`         |
| **feat** and **BREAKING CHANGE** | `feat: add API endpoint\nBREAKING CHANGE: update API response format` | `0.0.0`  | `1.0.0`         |

## Example Commands

- **fix**: A bug fix that causes a patch release.  
  Command:  
  ```bash
  git commit -m "fix: correct a typo"
