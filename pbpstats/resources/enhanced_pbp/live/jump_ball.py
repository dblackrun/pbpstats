from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import JumpBall


class LiveJumpBall(JumpBall, LiveEnhancedPbpItem):
    """
    Class for jump ball events
    """

    action_type = "jumpball"

    def __init__(self, *args):
        super().__init__(*args)
