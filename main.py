import typer
from pathlib import Path

import factory

from clock import Clock
import threading


def main(path: Path):
    Clock.init(0.25)

    macros = factory.build_macros(path)

    # Set up threads
    typer.secho("Initializing...")
    clock_thread = threading.Thread(target=Clock.instance().run)
    threads = []
    for macro in macros:
        t = threading.Thread(target=macro.run)
        threads.append(t)

    # Start threads
    typer.secho("Starting threads...")
    clock_thread.start()
    for t in threads:
        t.start()

    # Wait for threads to be done
    for t in threads:
        t.join()
    typer.secho("All macros stopped. Stopping clock...")
    Clock.instance().stop()
    clock_thread.join()
    typer.secho("Clock stopped. Exiting")


if __name__ == "__main__":
    typer.run(main)
