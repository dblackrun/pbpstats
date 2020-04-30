from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import DataEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import StartOfPeriod


class DataStartOfPeriod(StartOfPeriod, DataEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    def get_period_starters(self, file_directory=None):
        return self._get_period_starters_from_period_events(file_directory)
