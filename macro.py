from itertools import cycle
from event import IEvent

import keyboard


class Macro:
    _name: str
    _run_once: list[IEvent]
    _looped: list[IEvent]
    _continue_loop: bool

    def __init__(self, name: str, kill_hotkey: str = 'esc'):
        self._name = name
        self._run_once = []
        self._looped = []

        keyboard.add_hotkey(kill_hotkey, self._kill)

    def _kill(self) -> None:
        self._continue_loop = False

    @property
    def name(self) -> str:
        return self._name

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
