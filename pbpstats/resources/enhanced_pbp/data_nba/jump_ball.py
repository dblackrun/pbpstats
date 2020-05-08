from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import JumpBall


class DataJumpBall(JumpBall, DataEnhancedPbpItem):
    """
    Class for jump ball events
    """

    def __init__(self, *args):
        super().__init__(*args)
