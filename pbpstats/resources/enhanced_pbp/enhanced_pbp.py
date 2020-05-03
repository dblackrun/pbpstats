from pbpstats.resources.base import Base
from pbpstats.resources.enhanced_pbp import FieldGoal, FreeThrow, Rebound, Turnover


class EnhancedPbp(Base):
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        return [item.data for item in self.items]

    @property
    def fgas(self):
        return [item for item in self.items if isinstance(item, FieldGoal)]

    @property
    def fgms(self):
        return [item for item in self.items if isinstance(item, FieldGoal) and item.is_made]

    @property
    def ftas(self):
        return [item for item in self.items if isinstance(item, FreeThrow)]

    @property
    def rebounds(self):
        return [item for item in self.items if isinstance(item, Rebound) and item.is_real_rebound]

    @property
    def turnovers(self):
        return [item for item in self.items if isinstance(item, Turnover) and not item.is_no_turnover]
