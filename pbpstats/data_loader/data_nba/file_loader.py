import json
from pathlib import Path

from pbpstats.data_loader.abs_data_loader import AbsDataLoader


class DataNbaFileLoader(AbsDataLoader):
    """
    base class for loading data.nba.com saved on disk
    should not be called directly
    """
    def _load_data_from_file(self):
        data_file = Path(self.file_path)
        if not data_file.is_file():
            raise Exception(f'{self.file_path} does not exist')
        with open(self.file_path) as json_data:
            self.source_data = json.load(json_data)
