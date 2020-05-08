OVERRIDES = {
    "PLAYER_NAME": "name",
}


class StatsNbaBoxscoreItem(object):
    """
    Class for boxscore items from stats.nba.com

    :param dict item: dict with boxscore stats from response
    """

    def __init__(self, item):
        for key, value in item.items():
            setattr(self, OVERRIDES.get(key, key.lower()), value)

    @property
    def data(self):
        """
        returns boxscore data dict
        """
        return self.__dict__
