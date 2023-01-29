import pathlib

import pytest

from dapperdata.formatters.json import json_formatter

JSON_TEST_PATH = pathlib.Path(__file__).parent.resolve() / "json_tests"


def run_test(test_name: str):
    with open(f"{JSON_TEST_PATH}/{test_name}.in.json") as fp:
        yaml_input = fp.read()

    with open(f"{JSON_TEST_PATH}/{test_name}.out.json") as fp:
        expected_output = fp.read()

    assert json_formatter(yaml_input) == expected_output


def test_yaml_formatter_compact():
    run_test("compact")
