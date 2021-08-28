import threading

import yaml
import typer

from pathlib import Path

from models import Config


def main(path: Path) -> None:
    with path.open('r') as fp:
        config_lst = yaml.safe_load(fp)

    threads = []
    for item in config_lst:
        config: Config = Config.parse_obj(item)
        thread = threading.Thread(target=config.execute)
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    typer.run(main)
