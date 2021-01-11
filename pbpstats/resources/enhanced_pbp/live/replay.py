from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Replay


class LiveReplay(Replay, LiveEnhancedPbpItem):
    """
    Class for replay events
    """

    action_type = "replay"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def support_ruling(self):
        return False

    @property
    def overturn_ruling(self):
        return False

    @property
    def ruling_stands(self):
        return False
