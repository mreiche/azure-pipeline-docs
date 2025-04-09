import glob
import logging
import os
import sys
from pathlib import Path

import jinja2

from lib.models import Spec

output_dir = Path(os.getenv("OUTPUT_DIR", "out"))
template_file = Path(os.getenv("TEMPLATE_FILE", "templates/template.j2"))
os.makedirs(output_dir, exist_ok=True)

LOGGER = logging.getLogger(__name__)

__base_dir = Path(__file__).parent

def read_files(input_args: list[str]):
    search_pathes = [
        template_file.parent,
        __base_dir / "templates"
    ]
    template_loader = jinja2.FileSystemLoader(searchpath=search_pathes)
    template_env = jinja2.Environment(
        loader=template_loader,
        trim_blocks=True,
        lstrip_blocks=True
    )
    jinja_template = template_env.get_template(template_file.name)

    for input_arg in input_args:
        files = glob.glob(input_arg)
        for input_file in files:
            try:
                spec = Spec(input_file)
            except Exception as e:
                LOGGER.error(f"Failed loading '{input_file}'")
                LOGGER.exception(e)
                continue

            target_file = Path(output_dir) / f"{spec.file.stem}.md"
            try:
                with open(target_file, "w") as output_file:
                    output_file.write(jinja_template.render(spec=spec))
            except Exception as e:
                LOGGER.error(f"Failed rendering '{target_file}'")
                LOGGER.exception(e)

input_args = sys.argv
input_args.pop(0)
read_files(input_args)
