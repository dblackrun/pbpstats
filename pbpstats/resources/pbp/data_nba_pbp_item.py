class DataNbaPbpItem(object):
    """
    Class for pbp events from data.nba.com

    :param dict item: dict with event data
    :param int period: period in which event occurs
    """

    def __init__(self, item, period):
        self.period = period
        for key, value in item.items():
            setattr(self, key, value)

    @property
    def data(self):
        """
        returns pbp event dict
        """
        return self.__dict__
