import pathlib

import pytest

from dapperdata.formatters.yaml import yaml_formatter

YAML_TEST_PATH = pathlib.Path(__file__).parent.resolve() / "yaml_tests"


def run_test(test_name: str):
    with open(f"{YAML_TEST_PATH}/{test_name}.in.yaml") as fp:
        yaml_input = fp.read()

    with open(f"{YAML_TEST_PATH}/{test_name}.out.yaml") as fp:
        expected_output = fp.read()

    assert yaml_formatter(yaml_input) == expected_output


def test_yaml_formatter_newlines():
    run_test("newlines")
