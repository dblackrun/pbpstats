from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Foul


class LiveFoul(Foul, LiveEnhancedPbpItem):
    """
    Class for foul events
    """

    action_type = "foul"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def number_of_fta_for_foul(self):
        """
        returns the number of free throws resulting from the foul
        """
        if "1freethrow" in self.qualifiers:
            return 1
        elif "2freethrow" in self.qualifiers:
            return 2
        elif "3freethrow" in self.qualifiers:
            return 3

    @property
    def is_personal_foul(self):
        return self.sub_type == "personal" and not hasattr(self, "descriptor")

    @property
    def is_shooting_foul(self):
        return hasattr(self, "descriptor") and self.descriptor == "shooting"

    @property
    def is_loose_ball_foul(self):
        return hasattr(self, "descriptor") and self.stripped_descriptor == "looseball"

    @property
    def is_offensive_foul(self):
        return self.sub_type == "offensive" and (
            not hasattr(self, "descriptor") or self.descriptor != "charge"
        )

    @property
    def is_inbound_foul(self):
        return hasattr(self, "descriptor") and self.descriptor == "inbound"

    @property
    def is_away_from_play_foul(self):
        return (
            hasattr(self, "descriptor") and self.stripped_descriptor == "awayfromplay"
        )

    @property
    def is_clear_path_foul(self):
        return hasattr(self, "descriptor") and self.stripped_descriptor == "clearpath"

    @property
    def is_double_foul(self):
        return (
            hasattr(self, "descriptor")
            and self.descriptor == "double"
            and not self.is_technical
        )

    @property
    def is_technical(self):
        return self.sub_type == "technical" and not self.is_defensive_3_seconds

    @property
    def is_flagrant1(self):
        return (
            hasattr(self, "descriptor") and self.stripped_descriptor == "flagranttype1"
        )

    @property
    def is_flagrant2(self):
        return (
            hasattr(self, "descriptor") and self.stripped_descriptor == "flagranttype2"
        )

    @property
    def is_double_technical(self):
        return (
            self.sub_type == "technical"
            and hasattr(self, "descriptor")
            and self.descriptor == "double"
        )

    @property
    def is_defensive_3_seconds(self):
        return (
            hasattr(self, "descriptor")
            and self.stripped_descriptor == "defensive3second"
        )

    @property
    def is_delay_of_game(self):
        return self.stripped_sub_type == "delayofgame"

    @property
    def is_charge(self):
        return (
            self.sub_type == "offensive"
            and hasattr(self, "descriptor")
            and self.descriptor == "charge"
        )

    @property
    def is_personal_block_foul(self):
        return hasattr(self, "descriptor") and self.descriptor == "block"

    @property
    def is_personal_take_foul(self):
        return hasattr(self, "descriptor") and self.descriptor == "take"

    @property
    def is_shooting_block_foul(self):
        return hasattr(self, "descriptor") and self.descriptor == "block"
