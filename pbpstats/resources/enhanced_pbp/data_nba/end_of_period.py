from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import EndOfPeriod


class DataEndOfPeriod(EndOfPeriod, DataEnhancedPbpItem):
    """
    Class for end of period events
    """

    def __init__(self, *args):
        super().__init__(*args)
