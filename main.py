import typer
from pathlib import Path

import factory

from clock import Clock
import threading


def main(path: Path):
    Clock.init(0.25)

    macros = factory.build_macros(path)

    threads = [threading.Thread(target=Clock.instance().run)]
    for macro in macros:
        t = threading.Thread(target=macro.run)
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    typer.run(main)
