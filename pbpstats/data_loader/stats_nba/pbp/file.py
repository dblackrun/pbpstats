from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader


class StatsNbaPbpFileLoader(StatsNbaFileLoader):
    """
    A ``StatsNbaPbpFileLoader`` object should be instantiated and passed into ``StatsNbaPbpLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `stats_<game_id>.json` in the `/pbp` subdirectory.
    """
    def __init__(self, file_directory):
        self.file_directory = file_directory

    @check_file_directory
    def load_data(self, game_id):
        self.game_id = game_id
        self.file_path = f"{self.file_directory}/pbp/stats_{self.game_id}.json"
        return self._load_data_from_file()
