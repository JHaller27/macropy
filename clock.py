import time


class TimedEvent:
    def on_tick(self) -> None:
        raise NotImplementedError


class Clock:
    _precision: float
    _events: list[tuple[TimedEvent, int]]  # (event, tick-count before notifying)
    _ticks: int

    def __init__(self, precision: float):
        self._precision = precision
        self._events = []
        self._ticks = 0

    def register(self, event: TimedEvent, delay: float) -> None:
        tick_count = int(delay // self._precision)
        self._events.append((event, tick_count))

    def _tick(self) -> None:
        time.sleep(self._precision)
        for event, tick_target in self._events:
            if self._ticks % tick_target == 0:
                event.on_tick()
        self._ticks += 1
