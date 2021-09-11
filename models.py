from typing import Union, Optional
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
    kill: Optional[str]
    run_once: Optional[list[EventModel]]
    loop: Optional[list[EventModel]]
