OVERRIDES = {"pid": "player_id"}


class DataNbaBoxscoreItem(object):
    """
    Class for boxscore items from data.nba.com

    :param dict item: dict with boxscore stats from response
    :param int team_id: (optional) team id is not in dict with stats and can be added in here
    :param str team_abbreviation: (optional) team abbreviation is not in dict with stats and can be added in here
    """

    def __init__(self, item, team_id=None, team_abbreviation=None):
        self.team_id = team_id
        self.team_abbreviation = team_abbreviation
        for key, value in item.items():
            setattr(self, OVERRIDES.get(key, key), value)
        if hasattr(self, "fn") and hasattr(self, "ln"):
            self.name = f"{self.fn} {self.ln}"

    @property
    def data(self):
        """
        returns boxscore data dict
        """
        return self.__dict__
