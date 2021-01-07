import pbpstats

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
    def is_flagrant(self):
        return hasattr(self, "descriptor") and self.stripped_descriptor in [
            "flagranttype1",
            "flagranttype2",
        ]

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

    @property
    def counts_towards_penalty(self):
        """
        returns True if foul is a foul type that counts towards the penalty, False otherwise
        """
        if self.is_personal_foul:
            return True
        if self.is_shooting_foul:
            return True
        if self.is_loose_ball_foul:
            return True
        if self.is_inbound_foul:
            return True
        if self.is_away_from_play_foul:
            return True
        if self.is_clear_path_foul:
            return True
        if self.is_flagrant:
            return True
        if self.is_personal_block_foul:
            return True
        if self.is_personal_take_foul:
            return True
        if self.is_shooting_block_foul:
            return True
        return False

    @property
    def counts_as_personal_foul(self):
        """
        returns True if fouls is a foul type that counts as a personal foul, False otherwise
        """
        if self.is_personal_foul:
            return True
        if self.is_shooting_foul:
            return True
        if self.is_loose_ball_foul:
            return True
        if self.is_offensive_foul:
            return True
        if self.is_inbound_foul:
            return True
        if self.is_away_from_play_foul:
            return True
        if self.is_clear_path_foul:
            return True
        if self.is_double_foul:
            return True
        if self.is_flagrant:
            return True
        if self.is_charge:
            return True
        if self.is_personal_block_foul:
            return True
        if self.is_personal_take_foul:
            return True
        if self.is_shooting_block_foul:
            return True

        return False

    @property
    def foul_type_string(self):
        """
        returns string description of foul type
        """
        if self.is_personal_foul:
            return pbpstats.PERSONAL_FOUL_TYPE_STRING
        if self.is_shooting_foul:
            return pbpstats.SHOOTING_FOUL_TYPE_STRING
        if self.is_loose_ball_foul:
            return pbpstats.LOOSE_BALL_FOUL_TYPE_STRING
        if self.is_offensive_foul:
            return pbpstats.OFFENSIVE_FOUL_TYPE_STRING
        if self.is_inbound_foul:
            return pbpstats.INBOUND_FOUL_TYPE_STRING
        if self.is_away_from_play_foul:
            return pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING
        if self.is_clear_path_foul:
            return pbpstats.CLEAR_PATH_FOUL_TYPE_STRING
        if self.is_double_foul:
            return pbpstats.DOUBLE_FOUL_TYPE_STRING
        if hasattr(self, "descriptor") and self.descriptor == "flagrant-type-1":
            return pbpstats.FLAGRANT_1_FOUL_TYPE_STRING
        if hasattr(self, "descriptor") and self.descriptor == "flagrant-type-2":
            return pbpstats.FLAGRANT_2_FOUL_TYPE_STRING
        if self.is_defensive_3_seconds:
            return pbpstats.DEFENSIVE_3_SECONDS_FOUL_TYPE_STRING
        if self.is_charge:
            return pbpstats.CHARGE_FOUL_TYPE_STRING
        if self.is_personal_block_foul:
            return pbpstats.PERSONAL_BLOCK_TYPE_STRING
        if self.is_personal_take_foul:
            return pbpstats.PERSONAL_TAKE_TYPE_STRING
        if self.is_shooting_block_foul:
            return pbpstats.SHOOTING_BLOCK_TYPE_STRING
