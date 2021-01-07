from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import FreeThrow


class LiveFreeThrow(FreeThrow, LiveEnhancedPbpItem):
    """
    Class for free throw events
    """

    action_type = "freethrow"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_made(self):
        """
        returns True if shot was made, False otherwise
        """
        return self.shot_result == "Made"

    @property
    def is_ft_1_of_1(self):
        return self.sub_type == "1 of 1" and not hasattr(self, "descriptor")

    @property
    def is_ft_1_of_2(self):
        return self.sub_type == "1 of 2"

    @property
    def is_ft_2_of_2(self):
        return self.sub_type == "2 of 2"

    @property
    def is_ft_1_of_3(self):
        return self.sub_type == "1 of 3"

    @property
    def is_ft_2_of_3(self):
        return self.sub_type == "2 of 3"

    @property
    def is_ft_3_of_3(self):
        return self.sub_type == "3 of 3"

    @property
    def is_technical_ft(self):
        return hasattr(self, "descriptor") and self.descriptor == "technical"

    @property
    def is_ft_1pt(self):
        """
        returns True if free throw is a 1 point free throw, False otherwise
        Only used in g-league, starting in 2019-20 season
        """
        # TODO: add this if/when this is available for gleague
        return False

    @property
    def is_ft_2pt(self):
        """
        returns True if free throw is a 2 point free throw, False otherwise
        Only used in g-league, starting in 2019-20 season
        """
        # TODO: add this if/when this is available for gleague
        return False

    @property
    def is_ft_3pt(self):
        """
        returns True if free throw is a 3 point free throw, False otherwise
        Only used in g-league, starting in 2019-20 season
        """
        # TODO: add this if/when this is available for gleague
        return False

    @property
    def is_away_from_play_ft(self):
        """
        returns True if free throw is from an away from the play foul, False otherwise.
        """
        return (
            hasattr(self, "descriptor") and self.stripped_descriptor == "awayfromplay"
        )

    @property
    def is_flagrant_ft(self):
        """
        returns True if free throw is from a flagrant foul, False otherwise.
        """
        return hasattr(self, "descriptor") and self.stripped_descriptor == "flagrant"
