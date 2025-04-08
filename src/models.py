from dataclasses import dataclass
from typing import TypeVar, Generic

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
