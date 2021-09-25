"""
``DataNbaScheduleLoader`` loads schedule data for a season and
creates :obj:`~pbpstats.resources.games.data_nba_game_item.DataNbaGameItem` objects for each game

The following code will load schedule data for 2019-20 NBA Regular Season

.. code-block:: python

    from pbpstats.data_loader import DataNbaScheduleFileLoader, DataNbaScheduleLoader

    source_loader = DataNbaScheduleFileLoader("/data")
    schedule_loader = DataNbaScheduleLoader("nba", "2019-20", "Regular Season", source_loader)
    print(schedule_loader.items[0].data)  # prints dict with the first game of the season
"""
from pbpstats import (
    PLAYOFFS_STRING,
    REGULAR_SEASON_STRING,
    PLAY_IN_STRING,
)
from pbpstats.data_loader.data_nba.base import DataNbaLoaderBase
from pbpstats.resources.games.data_nba_game_item import DataNbaGameItem


class DataNbaScheduleLoader(DataNbaLoaderBase):
    """
    Loads data.nba.com source schedule data for season.
    Games are stored in items attribute
    as :obj:`~pbpstats.resources.games.data_nba_game_item.DataNbaGameItem` objects

    :param str league: Options are 'nba', 'wnba' or 'gleague'
    :param str season: Can be formatted as either 2019-20 or 2019.
    :param str season_type: Options are 'Regular Season' or 'Playoffs' or 'Play In'
    :param source_loader: :obj:`~pbpstats.data_loader.data_nba.pbp.file.DataNbaScheduleFileLoader` or :obj:`~pbpstats.data_loader.data_nba.pbp.web.DataNbaScheduleWebLoader` object
    """

    data_provider = "data_nba"
    resource = "Games"
    parent_object = "Season"

    def __init__(self, league, season, season_type, source_loader):
        self.league_string = league
        self.season_year = season.split("-")[0]
        self.source_data = source_loader.load_data(league, season)
        self._make_game_items(season_type)

    def _make_game_items(self, season_type):
        self.season_type = season_type
        self.items = [
            DataNbaGameItem(game)
            for item in self.data
            for game in item["mscd"]["g"]
            if self._is_season_type(game)
        ]

    def _is_season_type(self, game):
        if game["gid"][2] == "4" and self.season_type == PLAYOFFS_STRING:
            return True
        elif game["gid"][2] == "2" and self.season_type == REGULAR_SEASON_STRING:
            return True
        elif game["gid"][2] == "5" and self.season_type == PLAY_IN_STRING:
            return True
        return False

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["lscd"]
