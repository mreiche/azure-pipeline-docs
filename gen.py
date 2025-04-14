import glob
import logging
import os
import sys
from pathlib import Path

import jinja2
from is_empty import empty

from lib.models import Spec, regex_replace

LOGGER = logging.getLogger(__name__)

__output_dir = Path(os.getenv("OUTPUT_DIR", "out"))
__template_file = Path(os.getenv("TEMPLATE_FILE", "templates/template.j2.md"))
__spec_root = os.getenv("SPEC_ROOT")
__base_dir = Path(__file__).parent

def setup_jina_env():
    search_pathes = [
        __template_file.parent,
        __base_dir / "templates"
    ]
    if Spec.root_path:
        search_pathes.insert(0, Spec.root_path)

    template_loader = jinja2.FileSystemLoader(searchpath=search_pathes)
    template_env = jinja2.Environment(
        loader=template_loader,
        trim_blocks=True,
        lstrip_blocks=True
    )
    template_env.filters['regex_replace'] = regex_replace
    return template_env

def read_files(input_args: list[str]):
    if not empty(__spec_root):
        Spec.root_path = Path(__spec_root)
        assert Spec.root_path.is_dir(), "SPEC_ROOT must be a directory"

    jinja_env = setup_jina_env()
    jinja_template = jinja_env.get_template(__template_file.name)

    output_dir = Path(__output_dir)
    os.makedirs(__output_dir, exist_ok=True)

    for input_arg in input_args:
        files = glob.glob(input_arg)
        for input_file in files:
            try:
                spec = Spec(input_file)
            except Exception as e:
                LOGGER.error(f"Failed parsing '{input_file}'")
                LOGGER.exception(e)
                continue

            target_file = output_dir / f"{spec.file.stem}{__template_file.suffix}"
            try:
                with open(target_file, "w") as output_file:
                    output_file.write(jinja_template.render(spec=spec))
            except Exception as e:
                LOGGER.error(f"Failed rendering '{target_file}'")
                LOGGER.exception(e)

input_args = sys.argv
input_args.pop(0)
read_files(input_args)
