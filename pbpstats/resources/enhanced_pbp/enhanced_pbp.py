"""
The ``EnhancedPbp`` class has some basic properties for handling enhanced pbp data
"""
from pbpstats.resources.base import Base
from pbpstats.resources.enhanced_pbp import FieldGoal, FreeThrow, Rebound, Turnover


class EnhancedPbp(Base):
    """
    Class for enhanced play-by-play events

    :param list events: list of
        :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` items,
        typically from a enhanced pbp data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns list of pbp event dicts
        """
        return [item.data for item in self.items]

    @property
    def fgas(self):
        """
        returns list of :obj:`~pbpstats.resources.enhanced_pbp.field_goal.FieldGoal` events
        """
        return [item for item in self.items if isinstance(item, FieldGoal)]

    @property
    def fgms(self):
        """
        returns list of :obj:`~pbpstats.resources.enhanced_pbp.field_goal.FieldGoal` events with all made FGs
        """
        return [
            item for item in self.items if isinstance(item, FieldGoal) and item.is_made
        ]

    @property
    def ftas(self):
        """
        returns list of :obj:`~pbpstats.resources.enhanced_pbp.free_throw.FreeThrow` events
        """
        return [item for item in self.items if isinstance(item, FreeThrow)]

    @property
    def rebounds(self):
        """
        returns list of :obj:`~pbpstats.resources.enhanced_pbp.field_goal.Rebound` events
        """
        return [
            item
            for item in self.items
            if isinstance(item, Rebound) and item.is_real_rebound
        ]

    @property
    def turnovers(self):
        """
        returns list of :obj:`~pbpstats.resources.enhanced_pbp.field_goal.Turnover` events
        """
        return [
            item
            for item in self.items
            if isinstance(item, Turnover) and not item.is_no_turnover
        ]
