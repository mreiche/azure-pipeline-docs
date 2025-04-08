import glob
import os
import sys
from pathlib import Path
from typing import TypeVar, Self
import jinja2
from ruamel import yaml

from src.models import Condition

output_dir = Path(os.getenv("OUTPUT_DIR", "out"))
template_file = Path(os.getenv("TEMPLATE_PATH", "templates/template.j2"))
os.makedirs(output_dir, exist_ok=True)

T = TypeVar("T")

class Spec:

    cache: dict[str, Self] = {}

    def __init__(self, file: str):
        self.__file = Path(file)
        self.__doc = self.__load()

    @property
    def file(self) -> Path:
        return self.__file

    @property
    def doc(self):
        return self.__doc

    def __load(self):
        doc = self.load_yaml(self.__file)
        if "stages" in doc:
            doc["stages"] = self.load_items(doc["stages"], ["jobs", "steps"])

        elif "jobs" in doc:
            doc["jobs"] = self.load_items(doc["jobs"], ["steps"])

        elif "steps" in doc:
            doc["steps"] = self.load_items(doc["steps"], [])

        return doc

    def wrap_condition(self, obj: dict) -> Condition:
        keys = obj.keys()
        cond = None
        for key in keys:
            cond = Condition(expression=key, items=obj[key])

        return cond

    def load_template(self, obj: dict) -> Self:
        template_path = str(self.__file.parent / obj["template"].lstrip("/"))
        if template_path not in Spec.cache:
            Spec.cache[template_path] = Spec(template_path)

        template = Template(spec=Spec.cache[template_path])
        if "parameters" in obj:
            template.parameters = obj["parameters"]

        return template

    def load_items(self, items: list, hierarchy: list) -> list:
        i = 0
        sub_hierarchy = hierarchy.copy()
        this_level = sub_hierarchy.pop(0) if len(sub_hierarchy) > 0 else None
        for item in items:
            if self.is_condition(item):
                condition = self.wrap_condition(item)
                items[i] = condition
                condition.items = self.load_items(condition.items, hierarchy)
            elif "template" in item:
                item = self.load_template(item)
                items[i] = item
            elif this_level and this_level in item:
                item[this_level] = self.load_items(item[this_level], sub_hierarchy)

            i += 1

        return items

    def is_condition(self, obj: dict[str, any]) -> bool:
        keys = obj.keys()
        for key in keys:
            return key.strip().startswith("${{")
        return False

    def load_yaml(self, file: Path) -> dict:
        yml = yaml.YAML(typ='rt')
        with open(file, "r") as file:
            data = yml.load(file)
            return data

class Template:
    def __init__(self, spec: Spec):
        self.__spec = spec
        self.__parameters = None

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters: dict):
        self.__parameters = parameters

    @property
    def spec(self):
        return self.__spec


def read_files(input_args: list[str]):
    template_loader = jinja2.FileSystemLoader(searchpath=template_file.parent)
    template_env = jinja2.Environment(
        loader=template_loader,
        trim_blocks=True,
        lstrip_blocks=True
    )
    jinja_template = template_env.get_template(template_file.name)

    # with open(template_file, "r") as file:
    #     template_code = file.read()
    #     jinja_template = jinja2.Template(template_code)

    for input_arg in input_args:
        files = glob.glob(input_arg)
        for input_file in files:
            spec = Spec(input_file)
            target_file = Path(output_dir) / f"{spec.file.stem}.md"
            with open(target_file, "w") as output_file:
                output_file.write(jinja_template.render(spec=spec))

input_args = sys.argv
input_args.pop(0)
read_files(input_args)