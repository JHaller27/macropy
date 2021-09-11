from clock import Clock
import keyboard

from typer import secho


class IEvent:
    def execute(self):
        raise NotImplementedError


class DelayEvent(IEvent):
    _duration: int  # Ie target tick count

    def __init__(self, duration: int):
        self._duration = duration

    @property
    def duration(self) -> int:
        return self._duration

    def execute(self):
        secho(f"Delay for {self.duration} ticks")
        with Clock.instance().lock:
            for _ in range(self._duration):
                Clock.instance().lock.wait()


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
