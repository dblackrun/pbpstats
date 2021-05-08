class JumpBall(object):
    """
    Class for jump ball events
    """

    @property
    def winning_team(self):
        """
        returns team id that won the jump ball
        """
        return self.team_id

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
