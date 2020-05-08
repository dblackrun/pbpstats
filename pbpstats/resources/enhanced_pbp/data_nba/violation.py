from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Violation


class DataViolation(Violation, DataEnhancedPbpItem):
    """
    Class for violation events
    """

    def __init__(self, *args):
        super().__init__(*args)
