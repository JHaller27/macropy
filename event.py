from time import sleep
import keyboard


class IEvent:
    def execute(self):
        raise NotImplementedError


class Delay(IEvent):
    _duration: float

    def __init__(self, duration: float):
        self._duration = duration

    @property
    def duration(self) -> float:
        return self._duration

    def execute(self):
        # TODO: Replace with Clock thread wait/notify
        sleep(self.duration)


class KeyPress(IEvent):
    _key: str

    def __init__(self, key: str):
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    def execute(self):
        keyboard.press_and_release(self.key)
