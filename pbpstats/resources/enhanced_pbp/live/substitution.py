from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Substitution


class LiveSubstitution(Substitution, LiveEnhancedPbpItem):
    """
    Class for Substitution events
    """

    action_type = "substitution"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def incoming_player_id(self):
        """
        returns player id of player coming in to the game
        """
        if self.sub_type == "out":
            return None
        return self.player1_id

    @property
    def outgoing_player_id(self):
        """
        returns player id of player coming in to the game
        """
        if self.sub_type == "in":
            return None
        return self.player1_id

    @property
    def current_players(self):
        """
        returns dict with list of player ids for each team
        with players on the floor following the sub
        """
        players = {}
        for team_id, team_players in self.previous_event.current_players.items():
            players[team_id] = [player_id for player_id in team_players]
        if self.player1_id is not None:
            if self.sub_type == "in":
                players[self.team_id].append(self.player1_id)
            elif self.sub_type == "out" and self.player1_id in players[self.team_id]:
                players[self.team_id].remove(self.player1_id)
            players[self.team_id] = list(set(players[self.team_id]))
        return players
