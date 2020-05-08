"""
The ``Games`` class has some basic properties for handling game data
"""
from pbpstats.resources.base import Base


class Games(Base):
    """
    Class for games items

    :param list items: list of either
        :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem` or
        :obj:`~pbpstats.resources.games.data_nba_game_item.DataNbaGameItem` items,
        typically from a games data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts with game items
        """
        return [item.data for item in self.items]

    @property
    def final_games(self):
        """
        returns list of dicts with final game items
        """
        return [item.data for item in self.items if item.is_final]
