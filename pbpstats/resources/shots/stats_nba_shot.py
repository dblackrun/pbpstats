class StatsNbaShot(object):
    """
    Class for shot data from stats.nba.com

    :param dict item: dict with shot data
    """

    def __init__(self, item):
        for key, value in item.items():
            setattr(self, key.lower(), value)

    @property
    def data(self):
        """
        returns shot data dict
        """
        return self.__dict__
