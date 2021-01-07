"""
``LiveEnhancedPbpItem`` is the base class for all live data enhanced pbp event types
"""
from collections import defaultdict

from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.enhanced_pbp import StartOfPeriod

KEY_ATTR_MAPPER = {
    "period": "period",
    "actionNumber": "event_num",
    "clock": "clock",
    "description": "description",
    "xLegacy": "locX",
    "yLegacy": "locY",
    "actionType": "action_type",
    "subType": "sub_type",
    "descriptor": "descriptor",
    "shotResult": "shot_result",
    "assistPersonId": "player2_id",
    "blockPersonId": "player3_id",
    "stealPersonId": "player3_id",
    "foulDrawnPersonId": "player3_id",
    "shotActionNumber": "shot_action_number",
    "qualifiers": "qualifiers",
    "teamId": "team_id",
    "personId": "player1_id",
    "scoreHome": "home_score",
    "scoreAway": "away_score",
    "possession": "offense_team_id",
    "orderNumber": "order",
}


class LiveEnhancedPbpItem(EnhancedPbpItem):
    """
    Base class for enhanced pbp events from live data

    :param dict item: dict with event data
    :param int period: period in which event occurs
    :param str game_id: NBA Stats Game Id
    """

    def __init__(self, item, game_id):
        self.game_id = game_id
        for key, value in KEY_ATTR_MAPPER.items():
            attr_value = item.get(key)
            if attr_value is not None and attr_value != "":
                try:
                    # convert string values that should be ints
                    setattr(self, value, int(attr_value))
                except (ValueError, TypeError):
                    setattr(self, value, attr_value)
            if key == "description" and attr_value is None:
                setattr(self, value, "")
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

    @property
    def seconds_remaining(self):
        """
        returns seconds remaining in period as a ``float``
        """
        stripped = self.clock.replace("PT", "").replace("M", ":").replace("S", "")
        split = stripped.split(":")
        return float(split[0]) * 60 + float(split[1])

    @property
    def stripped_sub_type(self):
        return self.sub_type.replace("-", "").replace(" ", "")

    @property
    def stripped_descriptor(self):
        return self.descriptor.replace("-", "").replace(" ", "")
