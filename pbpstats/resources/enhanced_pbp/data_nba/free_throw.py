from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import DataEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import FreeThrow


class DataFreeThrow(FreeThrow, DataEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_made(self):
        return ' Missed' not in self.description
