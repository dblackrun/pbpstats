import abc

import pbpstats
from pbpstats.resources.enhanced_pbp import (
    EndOfPeriod,
    FieldGoal,
    FreeThrow,
    Replay,
    Turnover,
)


class EventOrderError(Exception):
    """
    Class for exception raised when rebound event is
    not immediately following a missed shot event.

    You can manually edit the event order in the pbp file
    stored on disk to fix this.
    """

    pass


class Rebound(object):
    """
    Class for rebound events
    """

    @property
    def is_real_rebound(self):
        """
        Returns True if rebound should be counted as a rebound, False otherwise.

        All missed shots have a rebound in the play-by-play but
        not all of these rebounds should be counted as actual rebounds. Some are just
        placeholder events.
        """
        if self.is_placeholder:
            return False

        if self.is_buzzer_beater_placeholder:
            return False

        if self.is_turnover_placeholder:
            return False

        if self.is_non_live_ft_placeholder:
            return False

        if self.is_buzzer_beater_rebound_at_shot_time:
            return False

        return True

    @abc.abstractproperty
    def is_placeholder(self):
        """
        returns True if rebound is a placeholder event, False otherwise.

        These are team rebounds on for example missed FT 1 of 2
        """
        return self.event_action_type != 0 and self.player1_id == 0

    @property
    def is_turnover_placeholder(self):
        """
        returns True if rebound is a placeholder event when a turnover occurs, False otherwise.

        Example shot clock violation or kicked ball turnover at time of team rebound
        """
        events_at_event_time = self.get_all_events_at_current_time()
        for event in events_at_event_time:
            if (
                isinstance(event, Turnover)
                and (event.is_shot_clock_violation or event.is_kicked_ball)
            ) and self.player1_id == 0:
                return True
        return False

    @property
    def is_non_live_ft_placeholder(self):
        """
        returns True if rebound is a placeholder event after a missed free throw that is not a live ball, False otherwise.

        Example: rebound after missed flagrant FT 2 of 2
        """
        if isinstance(self.missed_shot, FreeThrow) and not self.missed_shot.is_end_ft:
            return True
        return False

    @property
    def is_buzzer_beater_placeholder(self):
        """
        returns True if rebound is a placeholder event after a missed buzzer beater, False otherwise.

        Rebounds occur after time has expired but are still logged in play-by-play,
        but should not be counted in rebound totals
        """
        next_event = self.next_event
        if isinstance(next_event, Replay):
            next_event = next_event.next_event
        if (
            (self.clock == "00:00.0" or self.clock == "0:00")
            and self.player1_id == 0
            and (
                next_event is not None
                and isinstance(next_event, EndOfPeriod)
                or next_event is None
            )
        ):
            return True
        return False

    @property
    def is_buzzer_beater_rebound_at_shot_time(self):
        """
        returns True if rebound is a placeholder event after a missed buzzer beater, False otherwise.

        Sometimes rebound on buzzer beater is given the same time as shot - don't count these.
        Only don't count if rebound is last event before end of period event, ignoring replay events
        """
        if (
            self.missed_shot.seconds_remaining <= 3
            and self.seconds_remaining == self.missed_shot.seconds_remaining
            and self.player1_id == 0
        ):
            next_event = self.next_event
            if isinstance(next_event, Replay):
                next_event = next_event.next_event
            if isinstance(next_event, EndOfPeriod):
                return True
        return False

    @abc.abstractproperty
    def missed_shot(self):
        pass

    @abc.abstractproperty
    def oreb(self):
        pass

    @property
    def self_reb(self):
        """
        returns True if rebound was gotten by player who missed the shot, False otherwise
        """
        return self.player1_id == self.missed_shot.player1_id

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        stats = []
        if self.is_real_rebound:
            shot_type = self.missed_shot.shot_type
            if isinstance(self.missed_shot, FieldGoal) and self.missed_shot.is_blocked:
                if not self.oreb:
                    blocked_recovered_key = (
                        pbpstats.BLOCKED_STRING + shot_type + "Recovered"
                    )
                    block_player_id = self.missed_shot.player3_id
                    stats.append(
                        {
                            "player_id": block_player_id,
                            "team_id": self.team_id,
                            "stat_key": blocked_recovered_key,
                            "stat_value": 1,
                        }
                    )
                shot_type += pbpstats.BLOCKED_STRING
            if self.oreb:
                reb_key = (
                    shot_type
                    + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUNDS_STRING
                )
                opportunity_key = (
                    shot_type
                    + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUND_OPPORTUNITIES_STRING
                )
                opponent_opportunity_key = (
                    shot_type
                    + pbpstats.DEFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUND_OPPORTUNITIES_STRING
                )
            else:
                reb_key = (
                    shot_type
                    + pbpstats.DEFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUNDS_STRING
                )
                opportunity_key = (
                    shot_type
                    + pbpstats.DEFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUND_OPPORTUNITIES_STRING
                )
                opponent_opportunity_key = (
                    shot_type
                    + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUND_OPPORTUNITIES_STRING
                )

            stats.append(
                {
                    "player_id": self.player1_id,
                    "team_id": self.team_id,
                    "stat_key": reb_key,
                    "stat_value": 1,
                }
            )

            # rebound opportunites for all players on floor
            for team_id, players in self.current_players.items():
                stat_key = (
                    opportunity_key
                    if team_id == self.team_id
                    else opponent_opportunity_key
                )
                for player_id in players:
                    stat_item = {
                        "player_id": player_id,
                        "team_id": team_id,
                        "stat_key": stat_key,
                        "stat_value": 1,
                    }
                    stats.append(stat_item)
                if team_id == self.team_id and self.oreb:
                    for player_id in players:
                        on_floor_oreb_stat_item = {
                            "player_id": player_id,
                            "team_id": team_id,
                            "stat_key": pbpstats.ON_FLOOR_OFFENSIVE_REBOUND_STRING,
                            "stat_value": 1,
                        }
                        stats.append(on_floor_oreb_stat_item)

            # player missed shot rebound stats
            shooter_player_id = self.missed_shot.player1_id
            missed_shot_rebounded_opportunity_key = (
                shot_type
                + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX
                + pbpstats.REBOUNDED_OPPORTUNITIES_STRING
            )
            stats.append(
                {
                    "player_id": shooter_player_id,
                    "team_id": self.missed_shot.team_id,
                    "stat_key": missed_shot_rebounded_opportunity_key,
                    "stat_value": 1,
                }
            )
            if self.oreb:
                missed_shot_rebounded_key = (
                    shot_type
                    + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX
                    + pbpstats.REBOUNDED_STRING
                )
                stats.append(
                    {
                        "player_id": shooter_player_id,
                        "team_id": self.missed_shot.team_id,
                        "stat_key": missed_shot_rebounded_key,
                        "stat_value": 1,
                    }
                )
                if self.self_reb:
                    self_rebounded_key = shot_type + pbpstats.SELF_REBOUND_STRING
                    stats.append(
                        {
                            "player_id": shooter_player_id,
                            "team_id": self.missed_shot.team_id,
                            "stat_key": self_rebounded_key,
                            "stat_value": 1,
                        }
                    )

            team_ids = list(self.current_players.keys())
            opponent_team_id = (
                team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
            )
            lineups_ids = self.lineup_ids
            for stat in stats:
                opponent_team_id = (
                    team_ids[0] if stat["team_id"] == team_ids[1] else team_ids[1]
                )
                stat["lineup_id"] = lineups_ids[stat["team_id"]]
                stat["opponent_team_id"] = opponent_team_id
                stat["opponent_lineup_id"] = lineups_ids[opponent_team_id]
        return self.base_stats + stats
