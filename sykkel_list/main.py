import logging

from urllib.request import Request, urlopen
from .osmgr import OsloSykkelManager
from .ui import WindowSykkelList

LOGGER = logging.getLogger(__name__)


def main():
    # Setup logging
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", encoding='utf-8', level=logging.INFO)


    # Retrieve
    osmgr = OsloSykkelManager()
    osmgr.update_station_status()

    window = WindowSykkelList(osmgr.stations)
    window.show()


if __name__ == "__main__":
    main()

