"""
``LiveScheduleLoader`` loads schedule data for a season and
creates :obj:`~pbpstats.resources.games.data_nba_game_item.LiveGameItem` objects for each game

The following code will load schedule data for 2019-20 NBA Regular Season

.. code-block:: python

    from pbpstats.data_loader import LiveScheduleFileLoader, LiveScheduleLoader

    source_loader = LiveScheduleFileLoader("/data")
    schedule_loader = LiveScheduleLoader("nba", "2019-20", "Regular Season", source_loader)
    print(schedule_loader.items[0].data)  # prints dict with the first game of the season
"""
from pbpstats import (
    G_LEAGUE_GAME_ID_PREFIX,
    G_LEAGUE_STRING,
    NBA_GAME_ID_PREFIX,
    NBA_STRING,
    PLAY_IN_STRING,
    PLAYOFFS_STRING,
    REGULAR_SEASON_STRING,
    WNBA_GAME_ID_PREFIX,
    WNBA_STRING,
)
from pbpstats.data_loader.live.base import LiveLoaderBase
from pbpstats.resources.games.live_game_item import LiveGameItem


class LiveScheduleLoader(LiveLoaderBase):
    """
    Loads source schedule data for season.
    Games are stored in items attribute
    as :obj:`~pbpstats.resources.games.live_game_item.LiveGameItem` objects

    :param str league: Options are 'nba', 'wnba' or 'gleague'
    :param str season: Can be formatted as either 2019-20 or 2019.
    :param str season_type: Options are 'Regular Season' or 'Playoffs' or 'Play In'
    :param source_loader: :obj:`~pbpstats.data_loader.live.pbp.file.LiveScheduleFileLoader` or :obj:`~pbpstats.data_loader.live.pbp.web.LiveScheduleWebLoader` object
    """

    data_provider = "live"
    resource = "Games"
    parent_object = "Season"

    def __init__(self, league, season, season_type, source_loader):
        self.league_string = league
        self.source_data = source_loader.load_data(league, season)
        self._make_game_items(season_type, season)

    def _make_game_items(self, season_type, season):
        self.items = []
        if (
            self.data["seasonYear"] == season
            and self.league_id == self.data["leagueId"]
        ):
            self.season_type = season_type
            for daily_games in self.data["gameDates"]:
                for game in daily_games["games"]:
                    if self._is_season_type(game):
                        self.items.append(LiveGameItem(game))

    def _is_season_type(self, game):
        if game["gameId"][2] == "4" and self.season_type == PLAYOFFS_STRING:
            return True
        elif game["gameId"][2] == "2" and self.season_type == REGULAR_SEASON_STRING:
            return True
        elif game["gameId"][2] == "5" and self.season_type == PLAY_IN_STRING:
            return True
        return False

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["leagueSchedule"]

    @property
    def league_id(self):
        """
        Returns League Id for league.

        00 for nba, 10 for wnba, 20 for g-league
        """
        if self.league_string == NBA_STRING:
            return NBA_GAME_ID_PREFIX
        elif self.league_string == WNBA_STRING:
            return WNBA_GAME_ID_PREFIX
        elif self.league_string == G_LEAGUE_STRING:
            return G_LEAGUE_GAME_ID_PREFIX
