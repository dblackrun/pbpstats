from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader


class StatsNbaScoreboardFileLoader(StatsNbaFileLoader):
    """
    A ``StatsNbaScoreboardFileLoader`` object should be instantiated and passed into ``StatsNbaScoreboardLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `stats_<league>_<date>.json` in the `/schedule` subdirectory.
    """
    def __init__(self, file_directory):
        self.file_directory = file_directory

    @check_file_directory
    def load_data(self, date, league_string):
        self.file_path = f'{self.file_directory}/schedule/stats_{league_string}_{date.replace("/", "_")}.json'
        return self._load_data_from_file()
