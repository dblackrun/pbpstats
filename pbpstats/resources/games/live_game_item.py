KEY_ATTR_MAPPER = {
    "gameId": "game_id",
    "gameDateEst": "date",
    "gameStatusText": "status",
}


class LiveGameItem(object):
    """
    Class for game data from live data

    :param dict item: dict with game data
    """

    def __init__(self, item):
        for key, value in KEY_ATTR_MAPPER.items():
            if item.get(key) is not None:
                setattr(self, value, item.get(key))
        self.home_team_id = item["homeTeam"]["teamId"]
        self.home_team_abbreviation = item["homeTeam"]["teamTricode"]
        self.home_score = item["homeTeam"]["score"]
        self.away_team_id = item["awayTeam"]["teamId"]
        self.away_team_abbreviation = item["awayTeam"]["teamTricode"]
        self.away_score = item["awayTeam"]["score"]

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
        return "Final" in self.status
