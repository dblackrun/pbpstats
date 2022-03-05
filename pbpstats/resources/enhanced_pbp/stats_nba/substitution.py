from pbpstats.resources.enhanced_pbp import Substitution
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)


class StatsSubstitution(Substitution, StatsEnhancedPbpItem):
    """
    Class for Substitution events
    """

    event_type = 8

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def outgoing_player_id(self):
        """
        returns player id of player going out of the game
        """
        return self.player1_id

    @property
    def incoming_player_id(self):
        """
        returns player id of player coming in to the game
        """
        return self.player2_id
