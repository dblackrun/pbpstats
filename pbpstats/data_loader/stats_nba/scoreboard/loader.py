"""
``StatsNbaScoreboardLoader`` loads all games for a date and
creates :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem`
objects for each game

The following code will load data for 02/03/2020

.. code-block:: python

    from pbpstats.data_loader import StatsNbaScoreboardFileLoader, StatsNbaScoreboardLoader

    source_loader = StatsNbaScoreboardFileLoader("/data")
    game_finder_loader = StatsNbaScoreboardLoader("02/03/2020", "nba", source_loader)
    print(game_finder_loader.items[0].data) # prints dict for first game
"""
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class StatsNbaScoreboardLoader(StatsNbaFileLoader, StatsNbaWebLoader):
    """
    Loads stats.nba.com source data for date.
    Games are stored in items attribute
    as :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem` objects

    :param str date: Formatted as MM/DD/YYYY
    :param str league_string: Options are 'nba', 'wnba' or 'gleague'
    :param source_loader: :obj:`~pbpstats.data_loader.stats_nba.scoreboard.file.StatsNbaScoreboardFileLoader` or :obj:`~pbpstats.data_loader.stats_nba.scoreboard.web.StatsNbaScoreboardWebLoader` object
    """
    data_provider = "stats_nba"
    resource = "Games"
    parent_object = "Day"

    def __init__(self, date, league_string, source_loader):
        self.date = date
        self.league_string = league_string
        self.source_data = source_loader.load_data(date, league_string)
        self._make_scoreboard_items()

    def _make_scoreboard_items(self):
        self.items = [StatsNbaGameItem(item) for item in self.data]
