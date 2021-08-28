from typing import Literal, Union
from pydantic import BaseModel
from enum import Enum

from time import sleep
import keyboard


class EventType(str, Enum):
    KEY = 'key'
    DELAY = 'delay'
    LOOP = 'loop'


class Event:
    def execute(self) -> None:
        raise NotImplementedError


class DelayEvent(BaseModel, Event):
    type: Literal[EventType.DELAY]
    value: int

    def execute(self) -> None:
        sleep(self.value)


class KeyEvent(BaseModel, Event):
    type: Literal[EventType.KEY]
    value: str

    def execute(self) -> None:
        keyboard.press_and_release(self.value)


class LoopEvent(BaseModel, Event):
    type: Literal[EventType.LOOP]
    value: list[Event]

    def execute(self) -> None:
        for item in self.value:
            item.execute()


class Config(BaseModel, Event):
    name: str
    sequence: list[Union[DelayEvent, KeyEvent, LoopEvent]]

    class Config:
        arbitrary_types_allowed = True

    def execute(self) -> None:
        for item in self.sequence:
            item.execute()
