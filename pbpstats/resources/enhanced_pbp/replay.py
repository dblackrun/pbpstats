class Replay(object):
    event_type = 18

    @property
    def support_ruling(self):
        return self.event_action_type == 4

    @property
    def overturn_ruling(self):
        return self.event_action_type == 5

    @property
    def ruling_stands(self):
        return self.event_action_type == 6

    @property
    def event_stats(self):
        return self.base_stats
