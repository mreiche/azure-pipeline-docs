from pathlib import Path

from lib.models import Spec

__cwd = Path(__file__).parent

def test_spec_root():
    Spec.root_path = __cwd.parent
    spec = Spec(__cwd / "test-pipeline.yml")
    assert str(spec.relative_path) == "/test/test-pipeline.yml"
