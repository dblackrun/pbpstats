from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Ejection


class LiveEjection(Ejection, LiveEnhancedPbpItem):
    """
    Class for Ejection events
    """

    action_type = "ejection"

    def __init__(self, *args):
        super().__init__(*args)
