from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import (
    StartOfPeriod,
    InvalidNumberOfStartersException,
)


class DataStartOfPeriod(StartOfPeriod, DataEnhancedPbpItem):
    """
    Class for start of period events
    """

    event_type = 12

    def __init__(self, *args):
        super().__init__(*args)

    def get_period_starters(self, file_directory=None):
        """
        Gets player ids of players who started the period for each team
         If players can't be determined from parsing pbp, will try to
        find them by making API request to stats.nba.com boxscore filtered by time.

        :param str file_directory: directory in which overrides subdirectory exists
            containing period starter overrides when period starters can't be determined
            from parsing pbp events
        :returns: dict with list of player ids for each team
            with players on the floor at start of period
        :raises: :obj:`~pbpstats.resources.enhanced_pbp.start_of_period.InvalidNumberOfStartersException`:
            If all 5 players that start the period for a team can't be determined.
        """
        try:
            return self._get_period_starters_from_period_events(file_directory)
        except InvalidNumberOfStartersException:
            # get starters from stats.nba.com boxcore data by time range
            return self._get_starters_from_boxscore_request()
