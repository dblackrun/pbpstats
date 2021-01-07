OVERRIDES = {"personId": "player_id"}


class LiveBoxscoreItem(object):
    """
    Class for boxscore items from live data endpoint

    :param dict item: dict with boxscore stats from response
    :param int team_id: (optional) team id is not in dict with stats and can be added in here
    :param str team_abbreviation: (optional) team abbreviation is not in dict with stats and can be added in here
    """

    def __init__(self, item, team_id=None, team_abbreviation=None):
        self.team_id = team_id
        self.team_abbreviation = team_abbreviation
        for key, value in item.items():
            if key == "statistics":
                for stat_key, stat_value in value.items():
                    setattr(self, stat_key, stat_value)
            else:
                setattr(self, OVERRIDES.get(key, key), value)
        if hasattr(self, "firstName") and hasattr(self, "familyName"):
            self.name = f"{self.firstName} {self.familyName}"

    @property
    def data(self):
        """
        returns boxscore data dict
        """
        return self.__dict__

    @property
    def total_seconds(self):
        split = (
            self.minutes.replace("PT", "").replace("M", ":").replace("S", "").split(":")
        )
        return float(split[0]) * 60 + float(split[1])
