from typing import Literal, Union, Optional
from pydantic import BaseModel
from enum import Enum

from time import sleep
import keyboard

from typer import secho, colors


class EventType(str, Enum):
    KEY = 'key'
    DELAY = 'delay'
    LOOP = 'loop'


class DelayEvent(BaseModel):
    type: Literal[EventType.DELAY]
    value: float

    def execute(self) -> None:
        secho(f"Delay for {self.value} sec... ", nl=False, fg=colors.BRIGHT_BLACK)
        sleep(self.value)
        secho("Done", fg=colors.BRIGHT_BLACK)


class KeyEvent(BaseModel):
    type: Literal[EventType.KEY]
    value: str

    def execute(self) -> None:
        secho(f"Press key '{self.value}'... ", nl=False, fg=colors.BRIGHT_BLACK)
        keyboard.press_and_release(self.value)
        secho("Done", fg=colors.BRIGHT_BLACK)


class LoopEvent(BaseModel):
    type: Literal[EventType.LOOP]
    value: list[Union[DelayEvent, KeyEvent, 'LoopEvent']]
    times: Optional[int]

    def execute(self) -> None:
        if self.times is None:
            self._execute_infinitely()
        else:
            self._execute_times()

    def _execute_times(self) -> None:
        assert self.times is not None

        secho(f"Looping {self.times} times... ", fg=colors.BRIGHT_BLACK)
        for _ in range(self.times):
            for item in self.value:
                item.execute()
        secho("End loop", fg=colors.BRIGHT_BLACK)

    def _execute_infinitely(self) -> None:
        assert self.times is None

        secho(f"Looping infinitely... ", fg=colors.BRIGHT_BLACK)
        while True:
            for item in self.value:
                item.execute()


class Config(BaseModel):
    name: str
    sequence: list[Union[DelayEvent, KeyEvent, LoopEvent]]

    class Config:
        arbitrary_types_allowed = True

    def execute(self) -> None:
        for item in self.sequence:
            item.execute()
