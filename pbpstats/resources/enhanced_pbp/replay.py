import abc


class Replay(object):
    """
    Class for replay events
    """

    @abc.abstractproperty
    def support_ruling(self):
        pass

    @abc.abstractproperty
    def overturn_ruling(self):
        pass

    @abc.abstractproperty
    def ruling_stands(self):
        pass

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
