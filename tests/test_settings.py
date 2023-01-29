import pathlib

import pytest

from dapperdata.settings import settings


def test_settings_pyproject():
    assert "tests" in settings.exclude_paths


def test_settings_gitignore():
    assert ".vscode" in settings.exclude_paths
