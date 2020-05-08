KEY_ATTR_MAPPER = {
    "GAME_ID": "game_id",
    "GAME_DATE_EST": "date",
    "HOME_TEAM_ID": "home_team_id",
    "VISITOR_TEAM_ID": "visitor_team_id",
    "GAME_STATUS_TEXT": "status",
}


class StatsNbaGameItem(object):
    """
    Class for game data from stats.nba.com

    :param dict item: dict with game data
    """

    def __init__(self, item):
        for key, value in KEY_ATTR_MAPPER.items():
            if item.get(key) is not None:
                setattr(self, value, item.get(key))

    @property
    def data(self):
        """
        returns game dict
        """
        return self.__dict__

    @property
    def is_final(self):
        """
        returns True if game is final, False otherwise
        """
        return self.status == "Final"
