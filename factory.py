from models import *

from pathlib import Path
import yaml

from event import *
from macro import Macro


def parse_yaml(path: Path) -> MacroModel:
    with path.open(mode='r') as fp:
        data = yaml.safe_load(fp)

    return MacroModel.parse_obj(data)


def _parse_event(ev_model: EventModel) -> IEvent:
    if ev_model.type == EventType.DELAY:
        return DelayEvent(float(ev_model.value))
    if ev_model.type == EventType.KEY:
        return KeyPressEvent(str(ev_model.value))

    raise ValueError(f"Invalid event type '{ev_model.type}'")


def build_macro(model: MacroModel) -> Macro:
    macro = Macro()

    for ev_model in model.run_once:
        event = _parse_event(ev_model)
        macro.add_run_once(event)

    for ev_model in model.loop:
        event = _parse_event(ev_model)
        macro.add_looped(event)

    return macro
