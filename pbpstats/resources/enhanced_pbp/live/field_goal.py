from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import FieldGoal


class LiveFieldGoal(FieldGoal, LiveEnhancedPbpItem):
    """
    Class for field goal events
    """

    action_type = ["2pt", "3pt"]

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def shot_value(self):
        """
        returns 3 if shot is a 3 point attempt, 2 otherwise
        """
        return 3 if self.action_type == "3pt" else 2

    @property
    def is_made(self):
        """
        returns True if shot was made, False otherwise
        """
        return self.shot_result == "Made"
