from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import DataEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import FieldGoal


class DataFieldGoal(FieldGoal, DataEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def shot_value(self):
        return 3 if '3pt Shot' in self.description else 2
