class Timeout(object):
    event_type = 9

    @property
    def event_stats(self):
        return self.base_stats
