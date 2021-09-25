import requests

from pbpstats.data_loader.data_nba.base import DataNbaLoaderBase


class DataNbaWebLoader(DataNbaLoaderBase):
    """
    Base class for loading data from data.nba.com API request.

    All data.nba.com data loader classes should inherit from this class.

    This class should not be instantiated directly.
    """

    def _load_request_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.source_data = response.json()
            self._save_data_to_file()
            return self.source_data
        else:
            response.raise_for_status()
