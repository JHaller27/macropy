from enum import Enum

from time import sleep
import keyboard

from typer import secho, colors


class EventType(str, Enum):
    KEY = 'key'
    DELAY = 'delay'
    LOOP = 'loop'


class MacroModel:
    @classmethod
    def parse_obj(cls, d: dict) -> 'MacroModel':
        raise NotImplementedError


class Event(MacroModel):
    @classmethod
    def parse_obj(cls, d: dict) -> 'Event':
        raise NotImplementedError

    def execute(self) -> None:
        raise NotImplementedError


class DelayEvent(Event):
    event_type = EventType.DELAY
    value: float

    def __init__(self, value: float):
        self.value = value

    @classmethod
    def parse_obj(cls, d: dict) -> 'DelayEvent':
        return cls(d['value'])

    def execute(self) -> None:
        secho(f"Delay for {self.value} sec... ", nl=False, fg=colors.BRIGHT_BLACK)
        sleep(self.value)
        secho("Done", fg=colors.BRIGHT_BLACK)


class KeyEvent(Event):
    event_type = EventType.KEY
    value: str

    def __init__(self, value: str):
        self.value = value

    @classmethod
    def parse_obj(cls, d: dict) -> 'KeyEvent':
        return cls(d['value'])

    def execute(self) -> None:
        secho(f"Press key '{self.value}'... ", nl=False, fg=colors.BRIGHT_BLACK)
        keyboard.press_and_release(self.value)
        secho("Done", fg=colors.BRIGHT_BLACK)


class LoopEvent(Event):
    event_type = EventType.LOOP
    value: list[Event]

    def __init__(self, value: list[Event]):
        self.value = value

    @classmethod
    def parse_obj(cls, d: dict) -> 'LoopEvent':
        return cls([create_event(sub_event) for sub_event in d['value']])

    def execute(self) -> None:
        secho(f"Enter infinite loop...", fg=colors.BRIGHT_BLACK)
        while True:
            for item in self.value:
                item.execute()


EVENT_CLASSES = [KeyEvent, DelayEvent, LoopEvent]


def create_event(d: dict) -> Event:
    d_type = d['type']

    for event_cls in EVENT_CLASSES:
        if d_type == event_cls.event_type:
            return event_cls.parse_obj(d)

    raise RuntimeError(f"Could not parse Event of type '{d_type}'")


class Config(MacroModel):
    name: str
    sequence: list[Event]

    def __init__(self, name: str, sequence: list[Event]):
        self.name = name
        self.sequence = sequence

    @classmethod
    def parse_obj(cls, d: dict) -> 'Config':
        return cls(d['name'], [create_event(event) for event in d['sequence']])

    def execute_config(self) -> None:
        for item in self.sequence:
            item.execute()
