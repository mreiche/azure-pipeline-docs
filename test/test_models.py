from pathlib import Path

import pytest

from lib import models
from lib.models import Spec, regex_replace, Parameters

__cwd = Path(__file__).parent

def test_spec_root():
    Spec.root_path = __cwd.parent
    spec = Spec(__cwd / "test-pipeline.yml")
    assert str(spec.relative_path) == "test/test-pipeline.yml"

def test_replace_filter():
    ret = regex_replace("# This is a line", "^# ?", "")
    assert ret == "This is a line"

def test_parameters_from_list():
    input = [{
        "name": "test-param",
        "value": "Affe"
    }]
    parameters = Parameters(input)
    assert "test-param" in parameters
    assert parameters["test-param"]["value"] == "Affe"

    assert len(parameters) == 1

    for param in parameters:
        assert param["name"] == "test-param"
        assert param["value"] == "Affe"


def test_parameters_from_dict():
    input = {
        "my-param": "my-value",
    }

    parameters = Parameters(input)
    assert "my-param" in parameters
    assert parameters["my-param"]["value"] == "my-value"

def test_default_values():
    template = Spec(__cwd / "test-directory/test-pipeline3.yml")
    parameters = template.doc["parameters"]
    pass
