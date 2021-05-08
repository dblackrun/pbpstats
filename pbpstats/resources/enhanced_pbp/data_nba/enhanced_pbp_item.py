"""
``DataEnhancedPbpItem`` is the base class for all data.nba.com enhanced pbp event types
"""
from collections import defaultdict

from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.enhanced_pbp import StartOfPeriod

KEY_ATTR_MAPPER = {
    "evt": "event_num",
    "cl": "clock",
    "de": "description",
    "locX": "locX",
    "locY": "locY",
    "opt1": "opt1",
    "opt2": "opt2",
    "mtype": "event_action_type",
    "etype": "event_type",
    "opid": "player3_id",
    "tid": "team_id",
    "pid": "player1_id",
    "hs": "home_score",
    "vs": "away_score",
    "epid": "player2_id",
    "oftid": "offense_team_id",
    "ord": "order",
}


class DataEnhancedPbpItem(EnhancedPbpItem):
    """
    Base class for enhanced pbp events from data.nba.com

    :param dict item: dict with event data
    :param int period: period in which event occurs
    :param str game_id: NBA Stats Game Id
    """

    def __init__(self, item, period, game_id):
        self.game_id = game_id
        self.period = period
        for key, value in KEY_ATTR_MAPPER.items():
            attr_value = item.get(key)
            if attr_value is not None and attr_value != "":
                try:
                    # convert string values that should be ints
                    setattr(self, value, int(attr_value))
                except ValueError:
                    setattr(self, value, attr_value)
        self.player_game_fouls = defaultdict(int)
        self.possession_changing_override = False
        self.non_possession_changing_override = False
        self.score = defaultdict(int)

    @property
    def data(self):
        """
        returns event as a dict
        """
        return self.__dict__

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats

    def get_offense_team_id(self):
        """
        returns team id for team on offense for event
        """
        return self.offense_team_id

    @property
    def seconds_remaining(self):
        """
        returns seconds remaining in period as a ``float``
        """
        split = self.clock.split(":")
        return float(split[0]) * 60 + float(split[1])

    @property
    def is_possession_ending_event(self):
        """
        returns True if event ends a possession, False otherwise
        """
        if self.next_event is None:
            return True
        elif self.next_event is not None:
            oftid_changed = self.offense_team_id != self.next_event.offense_team_id
            # offense_team_id is 0 for first event of first quarter and overtimes - don't count it
            # sometimes there is an event before period start event that breaks things so check that too
            oftid_is_0 = (
                self.offense_team_id == 0 or self.next_event.offense_team_id == 0
            )
            start_of_period = isinstance(self, StartOfPeriod) or isinstance(
                self.next_event, StartOfPeriod
            )
            if oftid_changed and not oftid_is_0 and not start_of_period:
                return True
        return False
