import typer
from pathlib import Path

import factory


def main(path: Path):
    macros = factory.build_macros(path)

    # TODO: Run each macro in own thread
    for macro in macros:
        macro.run()


if __name__ == "__main__":
    typer.run(main)
