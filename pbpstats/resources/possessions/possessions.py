"""
The ``Possessions`` class has some basic properties for aggregating possession stats
"""
from itertools import groupby
from operator import itemgetter

from pbpstats import KEYS_OFF_BY_FACTOR_OF_5_WHEN_AGGREGATING_FOR_TEAM_AND_LINEUPS
from pbpstats.resources.base import Base


class Possessions(Base):
    """
    Class for possession items

    :param list items: list of
        :obj:`~pbpstats.resources.possessions.possession.Possession` items,
        typically from a possession data loader
    """

    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        """
        returns possessions dict
        """
        return self.__dict__

    def _aggregate_event_stats(self, *args):
        stats = [
            event_stat
            for item in self.items
            for event in item.events
            for event_stat in event.event_stats
        ]
        grouper = itemgetter(*args)
        results = []
        for key, grp in groupby(sorted(stats, key=grouper), grouper):
            temp_dict = dict(zip([*args], key))
            value = sum(item["stat_value"] for item in grp)
            if (
                temp_dict["stat_key"]
                in KEYS_OFF_BY_FACTOR_OF_5_WHEN_AGGREGATING_FOR_TEAM_AND_LINEUPS
                and "player_id" not in args
            ):
                # since stat keys are summed up from player stats
                # team and lineup stats will need some stats to be divided by 5
                value = value / 5
            temp_dict["stat_value"] = (
                value if isinstance(value, int) else round(value, 1)
            )
            results.append(temp_dict)
        return results

    @property
    def team_stats(self):
        """
        returns list of dicts with aggregated stats by team
        """
        return self._aggregate_event_stats("team_id", "stat_key")

    @property
    def opponent_stats(self):
        """
        returns list of dicts with aggregated stats by opponent
        """
        return self._aggregate_event_stats("opponent_team_id", "stat_key")

    @property
    def player_stats(self):
        """
        returns list of dicts with aggregated stats by player
        """
        return self._aggregate_event_stats("player_id", "team_id", "stat_key")

    @property
    def lineup_stats(self):
        """
        returns list of dicts with aggregated stats by lineup
        """
        return self._aggregate_event_stats("lineup_id", "team_id", "stat_key")

    @property
    def lineup_opponent_stats(self):
        """
        returns list of dicts with aggregated stats by lineup opponent
        """
        return self._aggregate_event_stats(
            "opponent_lineup_id", "opponent_team_id", "stat_key"
        )
