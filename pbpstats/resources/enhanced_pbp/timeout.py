class Timeout(object):
    """
    Class for timeout events
    """

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
