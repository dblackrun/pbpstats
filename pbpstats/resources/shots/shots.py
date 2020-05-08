"""
The ``Shots`` class has some basic properties for handling shot data
"""
from pbpstats.resources.base import Base


class Shots(Base):
    """
    Class for games items

    :param list items: list of
        :obj:`~pbpstats.resources.shots.stats_nba_shot.StatsNbaShot` items,
        typically from a shots data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts with shots
        """
        return [item.data for item in self.items]
