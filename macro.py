from itertools import cycle
from event import IEvent


class Macro:
    _name: str
    _run_once: list[IEvent]
    _looped: list[IEvent]

    def __init__(self, name: str):
        self._name = name
        self._run_once = []
        self._looped = []

    @property
    def name(self) -> str:
        return self._name

    def run(self):
        for event in self._run_once:
            event.execute()

        if len(self._looped) > 0:
            for event in cycle(self._looped):
                event.execute()

    def add_run_once(self, e: IEvent):
        self._run_once.append(e)

    def add_looped(self, e: IEvent):
        self._looped.append(e)
