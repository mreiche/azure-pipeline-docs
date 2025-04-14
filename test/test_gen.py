import subprocess
from pathlib import Path
import os
import shutil

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
    ret = subprocess.run(
        ["python", __base_dir / "../gen.py", __base_dir / "test-pipeline.yml"],
        capture_output=True,
        text=True,
        env=test_env
    )
    assert ret.returncode == 0
    with open(output_dir / "test-pipeline.md", "r") as file:
        file_content = file.read()
        assert "This is an\ninline comment.\\" in file_content
        assert "## Workflow" in file_content
        assert "## Parameters" in file_content
        assert "## Usage" in file_content


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

    with open(output_dir / "test-pipeline.md", "r") as file:
        file_content = file.read()
        assert "This is a special template for testing custom templates" in file_content
        assert "## Workflow" in file_content
