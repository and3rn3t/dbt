# Configuration Files Reference

This document explains all configuration and ignore files in the workspace.

## Version Control Files

### `.gitignore`

**Purpose**: Specifies files that Git should ignore

**Key exclusions**:

- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `.venv/`)
- Data files (large datasets in `data/` directories)
- Jupyter notebook checkpoints
- IDE settings (`.vscode/`, `.idea/`)
- Environment variables (`.env`)
- DBT artifacts (`target/`, `logs/`)
- Machine learning models (`*.pkl`, `*.h5`)

**Important**: Sample data files (e.g., `sample_*.csv`) are allowed for examples.

### `.gitattributes`

**Purpose**: Defines how Git handles different file types

**Features**:

- Forces LF line endings for text files
- Treats data files (CSV, Parquet, etc.) as binary
- Configures Jupyter notebook diff support
- Sets language detection for GitHub

### `.dockerignore`

**Purpose**: Files to exclude when building Docker images

**Similar to `.gitignore`** but optimized for Docker builds to reduce image size.

## Environment Configuration

### `.env.example`

**Purpose**: Template for environment variables

**Usage**:

```bash
# Copy and customize
cp .env.example .env
# Edit .env with your actual credentials
# NEVER commit .env to Git!
```

**Contains templates for**:

- Database credentials
- API keys
- DBT configuration
- Python paths

## Code Quality & Formatting

### `pyproject.toml`

**Purpose**: Python project configuration (PEP 518)

**Configures**:

- **Black**: Code formatter (line length: 88)
- **isort**: Import sorting
- **pytest**: Testing framework
- **mypy**: Type checking
- **coverage**: Code coverage reporting
- **ruff**: Fast Python linter

### `.flake8`

**Purpose**: Flake8 linter configuration

**Settings**:

- Max line length: 88 (matches Black)
- Excludes virtual environments, build artifacts
- Ignores certain style rules that conflict with Black

### `.editorconfig`

**Purpose**: Maintains consistent coding styles across editors

**Defines**:

- Character encoding (UTF-8)
- Line endings (LF)
- Indent styles for different file types:
  - Python: 4 spaces
  - YAML/JSON: 2 spaces
  - SQL: 4 spaces
  - Markdown: 2 spaces

## Data Organization

### `data/.gitkeep`

**Purpose**: Keeps empty `data/` directory in Git

Git doesn't track empty directories, so this file ensures the structure is preserved.

### `data/README.md`

**Purpose**: Documents data directory structure and guidelines

**Describes**:

- Purpose of each subdirectory (`raw/`, `processed/`, `staging/`, `external/`)
- Naming conventions
- Data handling policies
- Large file management

## Jupyter Notebooks

### `notebooks/.jupyterconfig.md`

**Purpose**: Documents Jupyter notebook best practices

**Covers**:

- Notebook diff tools (nbdime)
- Pre-commit hooks
- Best practices for version control

## VS Code Settings

### `.vscode/settings.json`

**Purpose**: VS Code workspace settings

**Configures**:

- Python environment
- Jupyter notebooks
- Data Wrangler
- CSV/TSV handling
- Code formatting on save

### `.vscode/extensions.json`

**Purpose**: Recommended VS Code extensions

**Extensions**:

- Python
- Jupyter
- Data Wrangler
- Rainbow CSV
- YAML, TOML support

## Usage Guide

### Initial Setup

1. **Environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements-datascience.txt
   ```

3. **Install development tools** (optional):

   ```bash
   pip install nbdime pre-commit
   nbdime config-git --enable
   ```

### Before Committing

1. **Format code**:

   ```bash
   black .
   isort .
   ```

2. **Run linter**:

   ```bash
   flake8 .
   ```

3. **Run tests**:

   ```bash
   pytest
   ```

4. **Clear notebook outputs** (for most notebooks):
   - In VS Code: "Clear All Outputs"
   - Or keep outputs for documentation notebooks

### Adding New Data Files

1. **Small files (<1MB)**: Can be committed if useful as examples
2. **Medium files (1-50MB)**: Add to `.gitignore`, document in `data/SOURCES.md`
3. **Large files (>50MB)**:
   - Use Git LFS or external storage
   - Provide download scripts
   - Document in `data/SOURCES.md`

## Security Notes

⚠️ **Never commit**:

- API keys
- Passwords
- Database credentials
- Private keys (`.pem`, `.key`)
- Personal data

✅ **Always**:

- Use `.env` for secrets
- Add credentials to `.gitignore`
- Use `.env.example` as a template
- Review changes before committing

## Maintenance

### Updating `.gitignore`

When adding new file types or directories:

```bash
# Add pattern to .gitignore
echo "new_pattern/" >> .gitignore

# Remove already tracked files
git rm -r --cached path/to/files
git commit -m "Update .gitignore"
```

### Checking Ignored Files

```bash
# See what's ignored in a directory
git status --ignored

# Check if a specific file is ignored
git check-ignore -v path/to/file
```

## Tools Installation

### Optional but recommended

```bash
# Better notebook diffs
pip install nbdime

# Pre-commit hooks
pip install pre-commit

# Code quality tools (if not already installed)
pip install black isort flake8 mypy pytest coverage ruff
```

## References

- [Python .gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [EditorConfig](https://editorconfig.org/)
- [Black documentation](https://black.readthedocs.io/)
- [Git LFS](https://git-lfs.github.com/)
- [nbdime](https://nbdime.readthedocs.io/)
