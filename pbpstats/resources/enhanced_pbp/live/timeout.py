from pbpstats.resources.enhanced_pbp import Timeout
from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem


class LiveTimeout(Timeout, LiveEnhancedPbpItem):
    """
    Class for timeout events
    """

    action_type = "timeout"

    def __init__(self, *args):
        super().__init__(*args)
