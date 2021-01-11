from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Timeout


class DataTimeout(Timeout, DataEnhancedPbpItem):
    """
    Class for timeout events
    """

    event_type = 9

    def __init__(self, *args):
        super().__init__(*args)
