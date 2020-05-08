KEY_ATTR_MAPPER = {
    "gid": "game_id",
    "gdte": "date",
    "stt": "status",
}


class DataNbaGameItem(object):
    """
    Class for game data from data.nba.com

    :param dict item: dict with game data
    """

    def __init__(self, item):
        for key, value in KEY_ATTR_MAPPER.items():
            if item.get(key) is not None:
                setattr(self, value, item.get(key))
        self.home_team_id = item["h"]["tid"]
        self.home_team_abbreviation = item["h"]["ta"]
        self.home_score = item["h"]["s"]
        self.away_team_id = item["v"]["tid"]
        self.away_team_abbreviation = item["v"]["ta"]
        self.away_score = item["v"]["s"]

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
