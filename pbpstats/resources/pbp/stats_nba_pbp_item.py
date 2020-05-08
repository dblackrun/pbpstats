class StatsNbaPbpItem(object):
    """
    Class for pbp events from stats.nba.com

    :param dict event: dict with event data
    :param int order: sequential order in which event occurs
    """

    def __init__(self, event, order):
        for key, value in event.items():
            setattr(self, key.lower(), value)
        self.order = order

    @property
    def data(self):
        """
        returns pbp event dict
        """
        return self.__dict__
