from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp.jump_ball import JumpBall


class StatsJumpBall(JumpBall, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)
