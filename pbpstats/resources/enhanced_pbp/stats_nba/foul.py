from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Foul


class StatsFoul(Foul, StatsEnhancedPbpItem):
    """
    Class for foul events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def number_of_fta_for_foul(self):
        """
        returns the number of free throws resulting from the foul
        """
        clock = self.clock
        event = self
        while (
            event is not None
            and event.clock == clock
            and not (
                hasattr(event, "is_first_ft")
                and not event.is_technical_ft
                and self.team_id != event.team_id
            )
        ):
            event = event.next_event

        if (
            event is not None
            and hasattr(event, "is_first_ft")
            and not event.is_technical_ft
            and event.clock == clock
            and (not hasattr(self, "player3_id") or self.player3_id == event.player1_id)
        ):
            # player3 id check is to make sure player who got fouled is player shooting free throws, prior to 2005-06 because foul drawning player isn't in pbp
            if "of 1" in event.description:
                return 1
            elif "of 2" in event.description:
                return 2
            elif "of 3" in event.description:
                return 3

        # if we haven't found ft yet, try going backwards
        event = self
        while (
            event is not None
            and event.clock == clock
            and not (
                hasattr(event, "is_first_ft")
                and not event.is_technical_ft
                and self.team_id != event.team_id
            )
        ):
            event = event.previous_event

        if (
            event is not None
            and hasattr(event, "is_first_ft")
            and not event.is_technical_ft
            and event.clock == clock
            and (not hasattr(self, "player3_id") or self.player3_id == event.player1_id)
        ):
            # player3 id check is to make sure player who got fouled is player shooting free throws, prior to 2005-06 because foul drawning player isn't in pbp
            if "of 1" in event.description:
                return 1
            elif "of 2" in event.description:
                return 2
            elif "of 3" in event.description:
                return 3
        return None
