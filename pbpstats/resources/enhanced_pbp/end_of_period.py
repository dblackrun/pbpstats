class EndOfPeriod(object):
    event_type = 13

    @property
    def event_stats(self):
        return self.base_stats
