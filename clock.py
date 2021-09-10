from time import sleep
from threading import Condition


class Clock:
    _latency: float
    _lock: Condition
    _instance: 'Clock' = None
    _loop: bool

    def __init__(self, latency: float):
        self._latency = latency
        self._lock = Condition()

    @staticmethod
    def init(latency: float):
        assert Clock._instance is None, "Clock may not be initialized more than once"
        Clock._instance = Clock(latency)

    @staticmethod
    def instance() -> 'Clock':
        assert Clock._instance is not None, "Clock must be initialized"
        return Clock._instance

    @property
    def lock(self) -> Condition:
        return self._lock

    def seconds_to_ticks(self, seconds: float) -> int:
        return int(seconds / self._latency)

    def run(self) -> None:
        with self._lock:
            self._lock.notify_all()

        self._loop = True
        while self._loop:
            sleep(self._latency)
            with self._lock:
                self._lock.notify_all()

    def stop(self) -> None:
        self._loop = False
