# Configuration Files Quick Reference

## ✅ Files Created

| File | Purpose | Status |
|------|---------|--------|
| `.gitignore` | Ignore Python, data, and temp files | ✅ Created |
| `.gitattributes` | Handle file types properly | ✅ Created |
| `.dockerignore` | Exclude files from Docker builds | ✅ Created |
| `.editorconfig` | Consistent code style | ✅ Created |
| `.env.example` | Environment variables template | ✅ Created |
| `.flake8` | Python linter config | ✅ Created |
| `.pre-commit-config.yaml` | Pre-commit hooks (optional) | ✅ Created |
| `pyproject.toml` | Python project & tools config | ✅ Created |
| `data/.gitkeep` | Keep data directory structure | ✅ Created |
| `CONFIGURATION.md` | Full configuration reference | ✅ Created |

## 🚀 Quick Start

### 1. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your credentials (NEVER commit .env!)
```

### 2. Optional: Enable Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 3. Optional: Better Notebook Diffs

```bash
pip install nbdime
nbdime config-git --enable
```

## 📝 Common Tasks

### Format Code

```bash
black .                    # Format Python files
isort .                    # Sort imports
```

### Check Code Quality

```bash
flake8 .                   # Lint Python code
pytest                     # Run tests
```

### Git Operations

```bash
# See ignored files
git status --ignored

# Check if file is ignored
git check-ignore -v path/to/file

# Remove tracked files that should be ignored
git rm -r --cached path/to/files
```

### Data Files

- **Small samples (<1MB)**: Can commit
- **Medium files (1-50MB)**: Add to `.gitignore`, document source
- **Large files (>50MB)**: Use Git LFS or external storage

## 🔐 Security Checklist

- [ ] Copied `.env.example` to `.env`
- [ ] Added credentials to `.env` (not `.env.example`)
- [ ] Verified `.env` is in `.gitignore`
- [ ] No API keys in code
- [ ] No passwords in notebooks
- [ ] Data files with PII are ignored

## 🎯 What's Protected

✅ **Ignored by Git:**

- Virtual environments
- Python cache files
- Large data files
- Notebook checkpoints
- IDE settings
- `.env` files
- DBT artifacts
- ML models
- Log files

✅ **Tracked by Git:**

- Source code
- Configuration files
- Documentation
- Small sample data
- Notebooks (optionally with outputs)

## 📚 Full Documentation

See `CONFIGURATION.md` for complete details on all configuration files.
