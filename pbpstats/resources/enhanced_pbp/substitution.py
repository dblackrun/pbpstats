class Substitution(object):
    event_type = 8

    @property
    def outgoing_player_id(self):
        return self.player1_id

    @property
    def incoming_player_id(self):
        return self.player2_id

    @property
    def current_players(self):
        """
        overrides EnhancedPbpItem current_players property
        """
        players = self.previous_event.current_players.copy()
        players[self.team_id] = [self.incoming_player_id if player == self.outgoing_player_id else player for player in players[self.team_id]]
        return players

    @property
    def event_stats(self):
        return self.base_stats
