import json
from pathlib import Path

from pbpstats.data_loader.live.base import LiveLoaderBase


class LiveFileLoader(LiveLoaderBase):
    """
    Base class for loading live data files saved on disk.

    All live data data loader classes should inherit from this class.

    This class should not be instantiated directly.
    """

    def _load_data_from_file(self):
        data_file = Path(self.file_path)
        if not data_file.is_file():
            raise Exception(f"{self.file_path} does not exist")
        with open(self.file_path) as json_data:
            self.source_data = json.load(json_data)
            return self.source_data
