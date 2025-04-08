from dataclasses import dataclass
from typing import TypedDict, Literal, TypeVar, Generic

type Types = Literal["string"]

type Variables = dict[str, any]
T = TypeVar('T')

class Parameter(TypedDict, total=False):
    name: str
    default: str
    type: Types

@dataclass
class Condition(Generic[T]):
    expression: str
    items: list[T]

class Step(TypedDict, total=False):
    clean: bool
    template: str
    parameters: Variables
    bash: str
    checkout: str
    fetchTags: bool
    fetchDepth: int

class Job(TypedDict, total=False):
    job: str
    displayName: str
    variables: Variables
    steps: list[Step|Condition[Step]]

class Stage(TypedDict, total=False):
    stage: str
    jobs: list[Job|Condition[Job]]
    dependsOn: list[str]

class Pipeline(TypedDict, total=False):
    parameters: list[Parameter]
    stages: list[Stage|Condition[Stage]]
