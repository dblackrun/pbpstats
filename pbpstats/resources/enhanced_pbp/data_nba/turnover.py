from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import DataEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Turnover


class DataTurnover(Turnover, DataEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)
