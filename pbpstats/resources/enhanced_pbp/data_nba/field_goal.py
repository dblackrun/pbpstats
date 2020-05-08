from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import FieldGoal


class DataFieldGoal(FieldGoal, DataEnhancedPbpItem):
    """
    Class for field goal events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def shot_value(self):
        """
        returns 3 if shot is a 3 point attempt, 2 otherwise
        """
        return 3 if "3pt Shot" in self.description else 2
