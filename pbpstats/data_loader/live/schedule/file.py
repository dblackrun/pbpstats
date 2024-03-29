from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.live.file_loader import LiveFileLoader


class LiveScheduleFileLoader(LiveFileLoader):
    """
    A ``LiveScheduleFileLoader`` object should be instantiated and passed into ``LiveScheduleLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `live_<league>_<season_year>.json` in the `/schedule` subdirectory.
    """

    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    @check_file_directory
    def load_data(self, league, season):
        self.league_string = league
        self.season_year = season.split("-")[0]
        self.file_path = f"{self.file_directory}/schedule/live_{self.league_string}_{self.season_year}.json"
        return self._load_data_from_file()
