from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Substitution


class DataSubstitution(Substitution, DataEnhancedPbpItem):
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
