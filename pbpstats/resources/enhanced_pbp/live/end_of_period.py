from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import EndOfPeriod


class LiveEndOfPeriod(EndOfPeriod, LiveEnhancedPbpItem):
    """
    Class for end of period events
    """

    action_type = "period"
    sub_type = "end"

    def __init__(self, *args):
        super().__init__(*args)
