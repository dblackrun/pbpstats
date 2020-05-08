class Ejection(object):
    """
    Class for Ejection events
    """

    event_type = 11

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
