import abc


class Substitution(object):
    """
    Class for Substitution events
    """

    @abc.abstractproperty
    def outgoing_player_id(self):
        pass

    @abc.abstractproperty
    def incoming_player_id(self):
        pass

    @property
    def current_players(self):
        """
        returns dict with list of player ids for each team
        with players on the floor following the sub
        """
        players = self.previous_event.current_players.copy()
        players[self.team_id] = [
            self.incoming_player_id if player == self.outgoing_player_id else player
            for player in players[self.team_id]
        ]
        return players

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
