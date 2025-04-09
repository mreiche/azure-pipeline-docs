import subprocess
from pathlib import Path
import os

__cwd__ = Path(__file__)

def test_hierarchy(monkeypatch):
    test_env = os.environ.copy()
    test_env["OUTPUT_DIR"] = str(__cwd__ / "out")
    ret = subprocess.run(
        ["python", __cwd__ / "../gen.py", __cwd__ / "test-pipeline.yml"],
        capture_output=True,
        text=True,
        env=test_env
    )
    assert ret.returncode == 0
