from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.data_nba.file_loader import DataNbaFileLoader


class DataNbaPbpFileLoader(DataNbaFileLoader):
    """
    A ``DataNbaPbpFileLoader`` object should be instantiated and passed into ``DataNbaPbpLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `data_<game_id>.json` in the `/pbp` subdirectory.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    @check_file_directory
    def load_data(self, game_id):
        self.game_id = game_id
        self.file_path = f"{self.file_directory}/pbp/data_{self.game_id}.json"
        return self._load_data_from_file()
