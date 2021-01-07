"""
The ``Boxscore`` class has some basic properties for handling boxscore data
"""
from pbpstats.resources.base import Base


class Boxscore(Base):
    """
    Class for boxscore items

    :param list items: list of either
        :obj:`~pbpstats.resources.boxscore.stats_nba_boxscore_item.StatsNbaBoxscoreItem` or
        :obj:`~pbpstats.resources.boxscore.live_boxscore_item.LiveBoxscoreItem` or
        :obj:`~pbpstats.resources.boxscore.data_nba_boxscore_item.DataNbaBoxscoreItem` items,
        typically from a boxscore data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns dict with boxscore items split up by player and team
        """
        return {"player": self.player_items, "team": self.team_items}

    @property
    def player_items(self):
        """
        returns list of player boxscore items
        """
        return [item.data for item in self.items if hasattr(item, "player_id")]

    @property
    def team_items(self):
        """
        returns list of team boxscore items
        """
        return [item.data for item in self.items if not hasattr(item, "player_id")]

    @property
    def player_name_map(self):
        """
        returns dict mapping player id to player name
        """
        return {item["player_id"]: item["name"] for item in self.player_items}

    @property
    def player_team_map(self):
        """
        returns dict mapping player id to team id
        """
        return {item["player_id"]: item["team_id"] for item in self.player_items}
