import subprocess
from pathlib import Path
import os
import shutil

import pytest
from is_empty import empty

from lib.models import Spec

__base_dir = Path(__file__).parent

def clear_dir(dir: Path):
    if dir.exists():
        shutil.rmtree(dir)
        assert dir.exists() == False

def test_rendering():
    output_dir = __base_dir / "out"
    clear_dir(output_dir)

    test_env = os.environ.copy()
    test_env["OUTPUT_DIR"] = str(output_dir)
    test_env["SPEC_ROOT"] = str(__base_dir)
    test_env["TEMPLATES_DIR"] = str(__base_dir / "templates")
    ret = subprocess.run(
        ["python", __base_dir / "../gen.py", __base_dir / "test-pipeline.yml"],
        capture_output=True,
        text=True,
        env=test_env
    )
    assert ret.returncode == 0
    assert ret.stderr == "INFO:gen.py:1 files generated\n", ret.stderr

    with open(output_dir / "test-pipeline.md", "r") as file:
        file_content = file.read()
        assert "This is an\ninline comment.\\" in file_content
        assert "## Workflow" in file_content
        assert "## Parameters" in file_content
        assert "## Other Usage" in file_content
        assert "| paramWithValues | `hund`, `katze`, `kuh` |  | `None` |" in file_content
        assert "| paramWithDisplayName | `None` | This parameter has a description | `None` |" in file_content
        assert "| parameterWithDefault | `string` | This parameter has a default | `Any string` |" in file_content
        assert "| objectParameter | `object` |  | `{'vmImage': 'Ubuntu-latest'}` |" in file_content


def test_rendering_with_custom_template():
    output_dir = __base_dir / "out2"
    clear_dir(output_dir)

    test_env = os.environ.copy()
    test_env["OUTPUT_DIR"] = str(output_dir)
    test_env["TEMPLATE_FILE"] = str(__base_dir / "templates/other-template.j2.md")
    ret = subprocess.run(
        ["python", __base_dir / "../gen.py", __base_dir / "test-pipeline.yml"],
        capture_output=True,
        text=True,
        env=test_env
    )
    assert ret.returncode == 0
    assert ret.stderr == "INFO:gen.py:1 files generated\n", ret.stderr

    with open(output_dir / "test-pipeline.md", "r") as file:
        file_content = file.read()
        assert "This is a special template for testing custom templates" in file_content
        assert "## Workflow" in file_content

def test_validate():
    Spec.validate = True
    with pytest.raises(expected_exception=ValueError, match="Parameters not supported by template.*\['affe'\]"):
        Spec(__base_dir / "test-pipeline-fails-validate.yml")

def test_rendering_structured():
    output_dir = __base_dir / "out3"
    clear_dir(output_dir)

    test_env = os.environ.copy()
    test_env["OUTPUT_DIR"] = str(output_dir)
    test_env["SPEC_ROOT"] = str(__base_dir)
    ret = subprocess.run(
        ["python", __base_dir / "../gen.py", __base_dir / "test-directory/test-pipeline3.yml"],
        capture_output=True,
        text=True,
        env=test_env
    )
    assert ret.returncode == 0
    with open(output_dir / "test-directory/test-pipeline3.md", "r") as file:
        file_content = file.read()
        assert "required: bool" in file_content
        assert "defaultNone: string" not in file_content
        assert "emptyStringDefault: string" not in file_content
        assert "Included Stage" in file_content

    assert "WARNING:lib.models:Skip reading template from repo reference 'stage-template.yml@repoReference' in template: test-directory/test-pipeline3.yml" in ret.stderr


def test_rendering_job_template():
    output_dir = __base_dir / "out4"
    clear_dir(output_dir)

    test_env = os.environ.copy()
    test_env["OUTPUT_DIR"] = str(output_dir)
    ret = subprocess.run(
        ["python", __base_dir / "../gen.py", __base_dir / "test-job-template.yml"],
        capture_output=True,
        text=True,
        env=test_env
    )
    assert ret.returncode == 0
    assert ret.stderr == "INFO:gen.py:1 files generated\n", ret.stderr

    with open(output_dir / "test-job-template.md", "r") as file:
        file_content = file.read()
        assert "First Step" in file_content
        assert "parameters: {}" in file_content
