import pbpstats
from pbpstats.resources.enhanced_pbp.timeout import Timeout


class Replay(object):
    event_type = 18

    @property
    def support_ruling(self):
        return self.event_action_type == 4

    @property
    def overturn_ruling(self):
        return self.event_action_type == 5

    @property
    def ruling_stands(self):
        return self.event_action_type == 6

    @property
    def event_stats(self):
        stats = []
        events = self.get_all_events_at_current_time()
        for event in events:
            if isinstance(event, Timeout):
                team_id = event.team_id
                if self.support_ruling:
                    stats.append({'player_id': 0, 'team_id': team_id, 'stat_key': pbpstats.CHALLENGE_SUPPORT_RULING_STRING, 'stat_value': 1})
                elif self.overturn_ruling:
                    stats.append({'player_id': 0, 'team_id': team_id, 'stat_key': pbpstats.CHALLENGE_OVERTURN_RULING_STRING, 'stat_value': 1})
                elif self.ruling_stands:
                    stats.append({'player_id': 0, 'team_id': team_id, 'stat_key': pbpstats.CHALLENGE_RULING_STANDS_STRING, 'stat_value': 1})
                team_ids = list(self.current_players.keys())
                lineups_ids = self.lineup_ids
                for stat in stats:
                    opponent_team_id = team_ids[0] if stat['team_id'] == team_ids[1] else team_ids[1]
                    stat['lineup_id'] = lineups_ids[stat['team_id']]
                    stat['opponent_team_id'] = opponent_team_id
                    stat['opponent_lineup_id'] = lineups_ids[opponent_team_id]
        return self.base_stats + stats
