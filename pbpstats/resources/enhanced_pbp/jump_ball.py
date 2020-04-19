class JumpBall(object):
    event_type = 10

    @property
    def winning_team(self):
        return self.team_id

    @property
    def event_stats(self):
        return self.base_stats
