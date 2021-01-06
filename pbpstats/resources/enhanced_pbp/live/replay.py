from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Replay


class LiveReplay(Replay, LiveEnhancedPbpItem):
    """
    Class for replay events
    """

    action_type = "replay"

    def __init__(self, *args):
        super().__init__(*args)
