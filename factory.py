from typing import Iterator

from pathlib import Path
import yaml

from event import *
from models import *
from macro import Macro


def _parse_yaml(path: Path) -> Iterator[MacroModel]:
    with path.open(mode='r') as fp:
        data = yaml.safe_load(fp)

    for item in data:
        yield MacroModel.parse_obj(item)


def _parse_event(ev_model: EventModel) -> IEvent:
    if ev_model.type == EventType.DELAY:
        return DelayEvent(float(ev_model.value))
    if ev_model.type == EventType.KEY:
        return KeyPressEvent(str(ev_model.value))

    raise ValueError(f"Invalid event type '{ev_model.type}'")


def _model2macro(model: MacroModel) -> Macro:
    macro = Macro()

    for ev_model in model.run_once:
        event = _parse_event(ev_model)
        macro.add_run_once(event)

    for ev_model in model.loop:
        event = _parse_event(ev_model)
        macro.add_looped(event)

    return macro


def build_macros(path: Path) -> Iterator[Macro]:
    for model in _parse_yaml(path):
        yield _model2macro(model)
