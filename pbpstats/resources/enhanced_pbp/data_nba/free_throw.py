from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import FreeThrow


class DataFreeThrow(FreeThrow, DataEnhancedPbpItem):
    """
    Class for free throw events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_made(self):
        """
        returns True if shot was made, False otherwise
        """
        return " Missed" not in self.description
