"""
``StatsNbaShotsLoader`` loads shot data for a game and
creates :obj:`~pbpstats.resources.shots.stats_nba_shot.StatsNbaShot`
objects for all shots

The following code will load shot data for game id "0021900001" from
a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import StatsNbaShotsFileLoader, StatsNbaShotsLoader

    source_loader = StatsNbaShotsFileLoader("/data")
    shot_loader = StatsNbaShotsLoader("0021900001", source_loader)
    print(shot_loader.items[0].data) # prints dict with data for one shot from game
"""
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase
from pbpstats.resources.shots.stats_nba_shot import StatsNbaShot


class StatsNbaShotsLoader(StatsNbaLoaderBase):
    """
    Loads stats.nba.com source shot data for game.
    Shots are stored in items attribute
    as :obj:`~pbpstats.resources.shots.stats_nba_shot.StatsNbaShot` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.stats_nba.shots.file.StatsNbaShotsFileLoader` or :obj:`~pbpstats.data_loader.stats_nba.shots.web.StatsNbaShotsWebLoader` object
    """

    data_provider = "stats_nba"
    resource = "Shots"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.home_source_data, self.away_source_data = source_loader.load_data(self.game_id)
        self._make_shot_items()

    def _make_shot_items(self):
        self.items = [StatsNbaShot(item) for item in self.data]

    def make_list_of_dicts(self, results_set_index=0):
        """
        Creates list of dicts from home and away source data

        :param int results_set_index: Index results are in. Default is 0
        :returns: list of dicts with shot data for all shots
        """
        headers = self.home_source_data["resultSets"][results_set_index]["headers"]
        home_rows = self.home_source_data["resultSets"][results_set_index]["rowSet"]
        home_deduped_rows = self.dedupe_events_row_set(home_rows)
        away_rows = self.away_source_data["resultSets"][results_set_index]["rowSet"]
        away_deduped_rows = self.dedupe_events_row_set(away_rows)
        return [dict(zip(headers, row)) for row in home_deduped_rows] + [
            dict(zip(headers, row)) for row in away_deduped_rows
        ]
