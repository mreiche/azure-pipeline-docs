from pathlib import Path
from typing import Self

from ruamel import yaml


class Condition:
    def __init__(self, expression: str, items: list):
        #self.__expression = expression.lstrip("${{").rstrip("}}").strip()
        self.__expression = expression
        self.__items = items

    @property
    def expression(self):
        return self.__expression

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items: list):
        self.__items = items


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
