from pathlib import Path

from lib.models import Spec, regex_replace

__cwd = Path(__file__).parent

def test_spec_root():
    Spec.root_path = __cwd.parent
    spec = Spec(__cwd / "test-pipeline.yml")
    assert str(spec.relative_path) == "test/test-pipeline.yml"

def test_replace_filter():
    ret = regex_replace("# This is a line", "^# ?", "")
    assert ret == "This is a line"
