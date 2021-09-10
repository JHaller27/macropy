import typer
from pathlib import Path

import factory

import threading


def main(path: Path):
    macros = factory.build_macros(path)

    threads = []
    for macro in macros:
        t = threading.Thread(target=macro.run)
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    typer.run(main)
