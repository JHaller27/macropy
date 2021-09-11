from typing import Iterator

from pathlib import Path
import yaml

from models import *
from macro import *
from clock import Clock


def _parse_yaml(path: Path) -> Iterator[MacroModel]:
    with path.open(mode='r') as fp:
        data = yaml.safe_load(fp)

    for item in data:
        yield MacroModel.parse_obj(item)


def _parse_event(macro: Macro, ev_model: EventModel) -> IEvent:
    if ev_model.type == EventType.DELAY:
        time_delay = float(ev_model.value)
        tick_delay = Clock.instance().seconds_to_ticks(time_delay)

        if tick_delay <= 0:
            raise ValueError(f"Cannot set delay of {time_delay}s - produces tick delay of 0")

        return DelayEvent(macro, tick_delay)

    if ev_model.type == EventType.KEY:
        return KeyPressEvent(macro, str(ev_model.value))

    raise ValueError(f"Invalid event type '{ev_model.type}'")


def _model2macro(model: MacroModel) -> Macro:
    macro = Macro(name=model.name, kill_hotkey=model.kill)

    if model.run_once is not None:
        for ev_model in model.run_once:
            event = _parse_event(macro, ev_model)
            macro.add_run_once(event)

    if model.loop is not None:
        for ev_model in model.loop:
            event = _parse_event(macro, ev_model)
            macro.add_looped(event)

    return macro


def build_macros(path: Path) -> Iterator[Macro]:
    for model in _parse_yaml(path):
        yield _model2macro(model)
