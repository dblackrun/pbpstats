"""
The ``Pbp`` class has some basic properties for handling pbp data
"""
from pbpstats.resources.base import Base


class Pbp(Base):
    """
    Class for pbp items

    :param list items: list of either
        :obj:`~pbpstats.resources.pbp.stats_nba_pbp_item.StatsNbaPbpItem` or
        :obj:`~pbpstats.resources.pbp.data_nba_pbp_item.DataNbaPbpItem` items,
        typically from a pbp data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of dicts with each event
        """
        return [item.data for item in self.items]
