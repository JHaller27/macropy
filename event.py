from time import sleep
import keyboard

from typer import secho


class IEvent:
    def execute(self):
        raise NotImplementedError


class DelayEvent(IEvent):
    _duration: float

    def __init__(self, duration: float):
        self._duration = duration

    @property
    def duration(self) -> float:
        return self._duration

    def execute(self):
        # TODO: Replace with Clock thread wait/notify
        secho(f"Delay for {self.duration}s")
        sleep(self.duration)


class KeyPressEvent(IEvent):
    _key: str

    def __init__(self, key: str):
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    def execute(self):
        secho(f"Press & release {self.key}")
        keyboard.press_and_release(self.key)
