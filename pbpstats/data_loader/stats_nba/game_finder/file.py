from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader



class StatsNbaGameFinderFileLoader(StatsNbaFileLoader):
    """
    A ``StatsNbaGameFinderFileLoader`` object should be instantiated and passed into ``StatsNbaGameFinderLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `stats_<league>_<season>_<season_type>.json` in the `/schedule` subdirectory.
    """
    def __init__(self, file_directory):
        self.file_directory = file_directory

    @check_file_directory
    def load_data(self, league, season, season_type):
        self.league_string = league
        self.season_string = season
        self.season_type_string = season_type
        self.file_path = f'{self.file_directory}/schedule/stats_{self.league_string}_{self.season_string.replace("-", "_")}_{self.season_type_string.replace(" ", "_")}.json'
        return self._load_data_from_file()
