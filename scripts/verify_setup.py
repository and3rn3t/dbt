"""Verification script to check project setup."""

import sys
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def check_mark():
    """Return a check mark."""
    return f"{GREEN}✓{RESET}"


def x_mark():
    """Return an X mark."""
    return f"{RED}✗{RESET}"


def test_imports():
    """Test that all required packages can be imported."""
    print(f"\n{BLUE}Testing Package Imports...{RESET}")

    packages = [
        ("pandas", "pd"),
        ("numpy", "np"),
        ("matplotlib.pyplot", "plt"),
        ("seaborn", "sns"),
        ("plotly", None),
        ("scipy", None),
        ("jupyter", None),
        ("black", None),
        ("pytest", None),
        ("isort", None),
    ]

    all_success = True
    for package, alias in packages:
        try:
            if alias:
                exec(f"import {package} as {alias}")
            else:
                exec(f"import {package}")
            print(f"  {check_mark()} {package}")
        except ImportError as e:
            print(f"  {x_mark()} {package} - {e}")
            all_success = False

    return all_success


def test_directories():
    """Test that all required directories exist."""
    print(f"\n{BLUE}Testing Directory Structure...{RESET}")

    required_dirs = [
        "data/raw",
        "data/processed",
        "data/staging",
        "data/external",
        "notebooks",
        "scripts",
        "tests",
        "templates",
        "dbt_project/models/staging",
        "dbt_project/models/marts",
        "dbt_project/seeds",
        "docs",
    ]

    all_exist = True
    project_root = Path(__file__).parent.parent

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"  {check_mark()} {dir_path}/")
        else:
            print(f"  {x_mark()} {dir_path}/ - Not found")
            all_exist = False

    return all_exist


def test_utilities():
    """Test utility functions."""
    print(f"\n{BLUE}Testing Utility Functions...{RESET}")

    try:
        from scripts.utils import (
            DATA_DIR,
            PROJECT_ROOT,
            get_data_path,
            load_csv,
            save_csv,
            validate_dataframe,
        )

        print(f"  {check_mark()} scripts.utils imported successfully")

        # Test get_data_path
        path = get_data_path("raw")
        print(f"  {check_mark()} get_data_path() works")

        # Test PROJECT_ROOT exists
        if PROJECT_ROOT.exists():
            print(f"  {check_mark()} PROJECT_ROOT exists: {PROJECT_ROOT}")
        else:
            print(f"  {x_mark()} PROJECT_ROOT doesn't exist")
            return False

        # Test DATA_DIR exists
        if DATA_DIR.exists():
            print(f"  {check_mark()} DATA_DIR exists: {DATA_DIR}")
        else:
            print(f"  {x_mark()} DATA_DIR doesn't exist")
            return False

        return True

    except Exception as e:
        print(f"  {x_mark()} Error testing utilities: {e}")
        return False


def test_environment():
    """Test Python environment."""
    print(f"\n{BLUE}Testing Python Environment...{RESET}")

    print(f"  {check_mark()} Python Version: {sys.version.split()[0]}")
    print(f"  {check_mark()} Python Executable: {sys.executable}")

    # Check if in virtual environment
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print(f"  {check_mark()} Virtual environment: Active")
    else:
        print(f"  {YELLOW}⚠{RESET}  Virtual environment: Not detected (may be OK)")

    return True


def test_config_files():
    """Test configuration files exist."""
    print(f"\n{BLUE}Testing Configuration Files...{RESET}")

    project_root = Path(__file__).parent.parent
    config_files = [
        ".env.example",
        ".gitignore",
        "pyproject.toml",
        "requirements-datascience.txt",
        "dbt_project/dbt_project.yml",
        "dbt_project/profiles.yml",
    ]

    all_exist = True
    for file_path in config_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  {check_mark()} {file_path}")
        else:
            print(f"  {x_mark()} {file_path} - Not found")
            all_exist = False

    return all_exist


def main():
    """Run all verification tests."""
    print(f"\n{'='*60}")
    print(f"{BLUE}Project Setup Verification{RESET}")
    print(f"{'='*60}")

    results = {
        "Environment": test_environment(),
        "Directories": test_directories(),
        "Config Files": test_config_files(),
        "Imports": test_imports(),
        "Utilities": test_utilities(),
    }

    print(f"\n{'='*60}")
    print(f"{BLUE}Summary{RESET}")
    print(f"{'='*60}")

    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())

    print(f"\n{'='*60}")
    if all_passed:
        print(f"{GREEN}✓ All checks passed! Setup is complete.{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("  1. Activate virtual environment: .venv\\Scripts\\Activate.ps1")
        print("  2. Start Jupyter: jupyter lab")
        print("  3. Run tests: pytest")
        print("  4. Check README.md for more information")
    else:
        print(f"{RED}✗ Some checks failed. Please review the output above.{RESET}")
    print(f"{'='*60}\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
