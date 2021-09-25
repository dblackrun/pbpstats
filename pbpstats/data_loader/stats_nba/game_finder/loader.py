"""
``StatsNbaGameFinderLoader`` loads all games for a season and
creates :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem`
objects for each game

The following code will load data for the 2019-20 NBA Regular Season

.. code-block:: python

    from pbpstats.data_loader import StatsNbaGameFinderWebLoader, StatsNbaGameFinderLoader

    source_loader = StatsNbaGameFinderWebLoader("/data")
    game_finder_loader = StatsNbaGameFinderLoader("nba", "2019-20", "Regular Season", source_loader)
    print(game_finder_loader.items[0].data) # prints dict for first game
"""
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class StatsNbaGameFinderLoader(StatsNbaLoaderBase):
    """
    Loads stats.nba.com source data for season.
    Games are stored in items attribute
    as :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem` objects

    :param str league: Options are 'nba', 'wnba' or 'gleague'
    :param str season: Formatted as 2019-20 for NBA and G-League, 2019 of WNBA.
    :param str season_type: Options are 'Regular Season' or 'Playoffs' or 'Play In'
    :param source_loader: :obj:`~pbpstats.data_loader.stats_nba.game_finder.file.StatsNbaGameFinderFileLoader` or :obj:`~pbpstats.data_loader.stats_nba.game_finder.web.StatsNbaGameFinderWebLoader` object
    """

    data_provider = "stats_nba"
    resource = "Games"
    parent_object = "Season"

    def __init__(self, league, season, season_type, source_loader):
        self.league_string = league
        self.season_string = season
        self.season_type_string = season_type
        self.source_data = source_loader.load_data(league, season, season_type)
        self._make_game_data_items()

    def _make_game_data_items(self):
        self.items = []
        sorted_games = sorted(self.data, key=lambda k: k["GAME_ID"])
        for team1, team2 in zip(sorted_games[0::2], sorted_games[1::2]):
            item = self._make_single_dict_for_game(team1, team2)
            self.items.append(StatsNbaGameItem(item))

    @staticmethod
    def _make_single_dict_for_game(team1, team2):
        """
        MATCHUP is vistor team @ home team for visitor
        MATCHUP is home team vs visitor team for home
        """
        item = {
            "GAME_ID": team1["GAME_ID"],
            "GAME_DATE_EST": team1["GAME_DATE"],
            "GAME_STATUS_TEXT": "Final",
            "HOME_TEAM_ID": team1["TEAM_ID"]
            if "@" not in team1["MATCHUP"]
            else team2["TEAM_ID"],
            "VISITOR_TEAM_ID": team1["TEAM_ID"]
            if "@" in team1["MATCHUP"]
            else team2["TEAM_ID"],
        }
        return item
