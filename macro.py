from itertools import cycle

import keyboard
from typer import secho

from clock import Clock


class IEvent:
    _macro: 'Macro'

    def __init__(self, macro: 'Macro') -> None:
        self._macro = macro

    def execute(self):
        raise NotImplementedError


class Macro:
    _name: str
    _run_once: list[IEvent]
    _looped: list[IEvent]
    _continue_loop: bool

    def __init__(self, name: str, kill_hotkey: str = None):
        self._name = name
        self._run_once = []
        self._looped = []

        if kill_hotkey is None:
            kill_hotkey = 'esc'
        keyboard.add_hotkey(kill_hotkey, self._kill)

    def _kill(self) -> None:
        if self._continue_loop:
            secho(f"Killing '{self.name}' macro...")
        self._continue_loop = False

    @property
    def name(self) -> str:
        return self._name

    def is_running(self) -> bool:
        return self._continue_loop

    def run(self):
        self._continue_loop = True

        for event in self._run_once:
            if not self._continue_loop:
                return
            event.execute()

        if len(self._looped) > 0:
            for event in cycle(self._looped):
                if not self._continue_loop:
                    return
                event.execute()

    def add_run_once(self, e: IEvent):
        self._run_once.append(e)

    def add_looped(self, e: IEvent):
        self._looped.append(e)


class DelayEvent(IEvent):
    _duration: int  # Ie target tick count

    def __init__(self, macro: Macro, duration: int):
        super().__init__(macro)
        self._duration = duration

    @property
    def duration(self) -> int:
        return self._duration

    def execute(self):
        secho(f"Delay for {self.duration} ticks")
        with Clock.instance().lock:
            for _ in range(self._duration):
                if not self._macro.is_running():
                    return
                Clock.instance().lock.wait()


class KeyPressEvent(IEvent):
    _key: str

    def __init__(self, macro: Macro, key: str):
        super().__init__(macro)
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    def execute(self):
        secho(f"Press & release {self.key}")
        keyboard.press_and_release(self.key)
