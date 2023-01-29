# DapperData

DapperData is an opinionated formatter for YAML and JSON files.

It has two options- fix files in place, or just yell about files that fail.

## Usage

### Install

```bash
pip install dapperdata
```

### Fix All Files in Place

If you want to fix all of the files in your current directory, recursively, run this command-

```bash
dapperdata pretty . --no-dry-run
```

### Test Files without Changing

You can use dapperdata to run a test in CI to confirm that all of the files already match the preferred styling.

```bash
dapperdata pretty .
```

This will return an list of all files to change, and will return a status code of 1 if any changes are needed. If no changes are needed the success status code (0) is returned.


## Configuration

### pyproject.toml

```toml
[tool.dapperdata]
exclude_paths = [".venv", "tests", ".git", ".vscode"]
```

### Environment Variables

```bash
DAPPERDATA_EXCLUDE_PATHS='[".venv", "tests", ".git", ".vscode"]'
```

## Excluded Files

If a `.gitignore` file is present the directories in it will be excluded from scans.
