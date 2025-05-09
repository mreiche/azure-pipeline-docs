import glob
import os
import sys
from pathlib import Path

import jinja2
from is_empty import empty
from jinja2 import TemplateError

from lib import models
from lib.log import logging
from lib.models import Spec, regex_replace

__file = Path(__file__)
LOGGER = logging.getLogger(__file.name)

__output_dir = Path(os.getenv("OUTPUT_DIR", "out"))
__template_file = os.getenv("TEMPLATE_FILE", "")
__templates_dir = os.getenv("TEMPLATES_DIR", "")
__spec_root = os.getenv("SPEC_ROOT", "").strip('\"')
__base_dir = __file.parent

if not empty(__template_file):
    __template_file_path = Path(__template_file)
else:
    __template_file_path = __base_dir /  "templates/template.j2.md"

def setup_jina_env():

    def _assert_path(path: Path):
        assert path.exists(), f"{path} doesn't exist"

    search_paths = []
    if not empty(__templates_dir):
        templates_path = Path(__templates_dir)
        _assert_path(templates_path)
        search_paths.append(templates_path)

    if Spec.root_path:
        _assert_path(Spec.root_path)
        search_paths.append(Spec.root_path)

    search_paths.append(__template_file_path.parent)
    search_paths.append(__base_dir / "templates")

    template_loader = jinja2.FileSystemLoader(searchpath=search_paths)
    template_env = jinja2.Environment(
        loader=template_loader,
        trim_blocks=True,
        lstrip_blocks=True
    )
    template_env.filters['regex_replace'] = models.regex_replace
    template_env.tests['is_not_defined'] = models.is_not_defined
    template_env.tests['is_defined'] = models.is_defined
    return template_env

def read_files(input_args: list[str]):
    if not empty(__spec_root):
        Spec.root_path = Path(__spec_root)
        assert Spec.root_path.is_dir(), f"SPEC_ROOT '{Spec.root_path.absolute()}' must be a directory"

    Spec.validate = os.getenv("VALIDATE", "true").lower() in ["true", "yes", "1", "on"]

    jinja_env = setup_jina_env()
    jinja_template = jinja_env.get_template(__template_file_path.name)

    output_dir = Path(__output_dir)

    generated = 0

    for input_arg in input_args:
        files = glob.glob(input_arg)
        for input_file in files:
            try:
                spec = Spec(input_file)
            except Exception as e:
                LOGGER.error(f"Failed parsing '{input_file}'")
                LOGGER.exception(e)
                continue

            if Spec.root_path:
                relative_output_dir = output_dir / spec.relative_path.parent
            else:
                relative_output_dir = output_dir

            os.makedirs(relative_output_dir, exist_ok=True)
            target_file = relative_output_dir / f"{spec.file.stem}{__template_file_path.suffix}"
            try:
                with open(target_file, "w") as output_file:
                    output_file.write(jinja_template.render(spec=spec))
                    generated += 1
            except TemplateError as e:
                LOGGER.error(f"Failed rendering '{target_file}'")
                raise e
            except Exception as e:
                LOGGER.warning(f"Skipped rendering '{target_file}'")
                LOGGER.exception(e)

    LOGGER.info(f"{generated} files generated")

input_args = sys.argv
input_args.pop(0)
read_files(input_args)
