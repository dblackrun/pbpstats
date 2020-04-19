from itertools import groupby
from operator import itemgetter


class Possession(object):
    def __init__(self, events):
        self.game_id = events[0].game_id
        self.period = events[0].period
        self.events = events

    def __repr__(self):
        return (
            f'<{type(self).__name__} GameId: {self.game_id}, Period: {self.period}, '
            f'Number: {self.number}, StartTime: {self.start_time}, EndTime: {self.end_time}, '
            f'OffenseTeamId: {self.offense_team_id}>'
        )

    @property
    def data(self):
        return self.__dict__

    @property
    def start_time(self):
        if not hasattr(self, 'previous_possession') or self.previous_possession is None:
            return self.events[0].clock
        return self.previous_possession.events[-1].clock

    @property
    def end_time(self):
        return self.events[-1].clock

    @property
    def offense_team_id(self):
        return self.events[0].get_offense_team_id()

    @property
    def possession_stats(self):
        grouper = itemgetter('player_id', 'team_id', 'opponent_team_id', 'lineup_id', 'opponent_lineup_id', 'stat_key')
        results = []
        event_stats = [event_stat for event in self.events for event_stat in event.event_stats]
        for key, group in groupby(sorted(event_stats, key=grouper), grouper):
            temp_dict = dict(zip(['player_id', 'team_id', 'opponent_team_id', 'lineup_id', 'opponent_lineup_id', 'stat_key'], key))
            temp_dict['stat_value'] = sum(item['stat_value'] for item in group)
            results.append(temp_dict)

        return results
