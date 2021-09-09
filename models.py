from typing import Union
from enum import Enum
from pydantic import BaseModel


class EventType(str, Enum):
    DELAY = 'delay'
    KEY = 'key'


class EventModel(BaseModel):
    type: EventType
    value: Union[str, float]


class MacroModel(BaseModel):
    name: str
    run_once: list[EventModel]
    loop: list[EventModel]
