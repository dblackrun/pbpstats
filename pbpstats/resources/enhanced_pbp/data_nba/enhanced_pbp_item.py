from collections import defaultdict

from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.enhanced_pbp import StartOfPeriod

KEY_ATTR_MAPPER = {
    'evt': 'event_num',
    'cl': 'clock',
    'de': 'description',
    'locX': 'locX',
    'locY': 'locY',
    'opt1': 'opt1',
    'opt2': 'opt2',
    'mtype': 'event_action_type',
    'etype': 'event_type',
    'opid': 'player3_id',
    'tid': 'team_id',
    'pid': 'player1_id',
    'hs': 'home_score',
    'vs': 'away_score',
    'epid': 'player2_id',
    'oftid': 'offense_team_id',
    'ord': 'order',
}


class DataEnhancedPbpItem(EnhancedPbpItem):
    def __init__(self, item, period, game_id):
        self.game_id = game_id
        self.period = period
        for key, value in KEY_ATTR_MAPPER.items():
            attr_value = item.get(key)
            if attr_value is not None and attr_value != '':
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
        return self.__dict__

    @property
    def event_stats(self):
        return self.base_stats

    def get_offense_team_id(self):
        return self.offense_team_id

    @property
    def is_possession_ending_event(self):
        """
        data.pbp.com pbp has offense team id attribute
        when offense team id is different in next event, event is a possession ending event
        """
        if self.next_event is None:
            return True
        elif self.next_event is not None:
            oftid_changed = self.offense_team_id != self.next_event.offense_team_id
            # offense_team_id is 0 for first event of first quarter and overtimes - don't count it
            # sometimes there is an event before period start event that breaks things so check that too
            oftid_is_0 = self.offense_team_id == 0 or self.next_event.offense_team_id == 0
            start_of_period = isinstance(self, StartOfPeriod) or isinstance(self.next_event, StartOfPeriod)
            if oftid_changed and not oftid_is_0 and not start_of_period:
                return True
        return False
