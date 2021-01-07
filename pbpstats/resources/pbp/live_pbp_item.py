class LivePbpItem(object):
    """
    Class for pbp events from live data

    :param dict item: dict with event data
    :param int period: period in which event occurs
    """

    def __init__(self, item):
        for key, value in item.items():
            setattr(self, key, value)

    @property
    def data(self):
        """
        returns pbp event dict
        """
        return self.__dict__
