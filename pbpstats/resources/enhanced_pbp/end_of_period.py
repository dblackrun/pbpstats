class EndOfPeriod(object):
    """
    Class for end of period events
    """

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
