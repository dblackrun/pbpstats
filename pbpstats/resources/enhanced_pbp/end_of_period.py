class EndOfPeriod(object):
    """
    Class for end of period events
    """

    event_type = 13

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
