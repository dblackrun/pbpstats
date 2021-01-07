from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Rebound


class LiveRebound(Rebound, LiveEnhancedPbpItem):
    """
    Class for rebound events
    """

    action_type = "rebound"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def missed_shot(self):
        """
        returns :obj:`~pbpstats.resources.enhanced_pbp.field_goal.FieldGoal` or
        :obj:`~pbpstats.resources.enhanced_pbp.free_throw.FreeThrow` object
        for shot that was missed

        :raises: :obj:`~pbpstats.resources.enhanced_pbp.rebound.EventOrderError`:
            If rebound event is not immediately following a missed shot event.
        """
        prev_event = self.previous_event
        while prev_event is not None:
            if prev_event.event_num == self.shot_action_number:
                return prev_event
            prev_event = prev_event.previous_event

        raise Rebound.EventOrderError(
            f"previous event: {self.previous_event} is not a missed free throw or field goal"
        )

    @property
    def oreb(self):
        """
        returns True if rebound is an offensive rebound, False otherwise
        """
        return self.sub_type == "offensive"

    @property
    def is_placeholder(self):
        """
        returns True if rebound is a placeholder event, False otherwise.

        These are team rebounds on for example missed FT 1 of 2
        """
        if hasattr(self, "qualifiers") and "deadball" in self.qualifiers:
            return True
        if (
            hasattr(self.missed_shot, "is_flagrant_ft")
            and self.missed_shot.is_flagrant_ft
        ):
            return True
        return False
