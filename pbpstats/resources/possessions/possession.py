"""
The ``Possession`` class has some basic properties for handling possession data
"""
from itertools import groupby
from operator import itemgetter

import pbpstats
from pbpstats.resources.enhanced_pbp import (
    FieldGoal,
    FreeThrow,
    JumpBall,
    Rebound,
    Substitution,
    Timeout,
    Turnover,
)


class Possession(object):
    """
    Class for possession

    :param list events: list of
        :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` items for possession,
        typically from a possession data loader
    """

    def __init__(self, events):
        self.game_id = events[0].game_id
        self.period = events[0].period
        self.events = events

    def __repr__(self):
        return (
            f"<{type(self).__name__} GameId: {self.game_id}, Period: {self.period}, "
            f"Number: {self.number}, StartTime: {self.start_time}, EndTime: {self.end_time}, "
            f"OffenseTeamId: {self.offense_team_id}>"
        )

    @property
    def data(self):
        """
        returns dict possession data
        """
        return self.__dict__

    @property
    def start_time(self):
        """
        returns the time remaining (MM:SS) in the period when the possession started
        """
        if not hasattr(self, "previous_possession") or self.previous_possession is None:
            return self.events[0].clock
        return self.previous_possession.events[-1].clock

    @property
    def end_time(self):
        """
        returns the time remaining (MM:SS) in the period when the possession ended
        """
        return self.events[-1].clock

    @property
    def start_score_margin(self):
        """
        returns the score margin from the perspective of the team on offense when the possession started
        """
        if not hasattr(self, "previous_possession") or self.previous_possession is None:
            score = self.events[0].score
        else:
            score = self.previous_possession.events[-1].score
        offense_team_id = self.offense_team_id
        offense_points = score[offense_team_id]
        defense_points = 0
        for team_id, points in score.items():
            if team_id != offense_team_id:
                defense_points = points
        return offense_points - defense_points

    def get_team_ids(self):
        """
        returns a list with the team ids of both teams playing
        """
        team_ids = list(
            set([event.team_id for event in self.events if event.team_id != 0])
        )
        prev_poss = self.previous_possession
        while len(team_ids) != 2 and prev_poss is not None:
            team_ids += [
                event.team_id for event in prev_poss.events if event.team_id != 0
            ]
            team_ids = list(set(team_ids))
            prev_poss = prev_poss.previous_possession
        next_poss = self.next_possession
        while len(team_ids) != 2 and next_poss is not None:
            team_ids += [
                event.team_id for event in next_poss.events if event.team_id != 0
            ]
            team_ids = list(set(team_ids))
            next_poss = next_poss.next_possession
        return team_ids

    @property
    def offense_team_id(self):
        """
        returns team id for team on offense on possession
        """
        if len(self.events) == 1 and isinstance(self.events[0], JumpBall):
            # if possession only has one event and it is a jump ball, need to check
            # how previous possession ended to see which team actually started with the ball
            # because team id on jump ball is team that won the jump ball
            prev_event = self.previous_possession_ending_event
            if isinstance(prev_event, Turnover) and not prev_event.is_no_turnover:
                team_ids = self.get_team_ids()
                return (
                    team_ids[0]
                    if team_ids[1] == prev_event.get_offense_team_id()
                    else team_ids[1]
                )
            if isinstance(prev_event, Rebound) and prev_event.is_real_rebound:
                if not prev_event.oreb:
                    team_ids = self.get_team_ids()
                    return (
                        team_ids[0]
                        if team_ids[1] == prev_event.get_offense_team_id()
                        else team_ids[1]
                    )
                return prev_event.get_offense_team_id()
            if isinstance(prev_event, (FieldGoal, FreeThrow)):
                if prev_event.is_made:
                    team_ids = self.get_team_ids()
                    return (
                        team_ids[0]
                        if team_ids[1] == prev_event.get_offense_team_id()
                        else team_ids[1]
                    )
                return prev_event.get_offense_team_id()
        return self.events[0].get_offense_team_id()

    @property
    def possession_has_timeout(self):
        """
        returns True if there was a timeout called on the current possession, False otherwise
        """
        for i, event in enumerate(self.events):
            if isinstance(event, Timeout) and event.clock != self.end_time:
                # timeout is not at possession end time
                if not (
                    event.next_event is not None
                    and (
                        isinstance(event.next_event, FreeThrow)
                        and not event.next_event.is_technical_ft
                    )
                    and event.clock == event.next_event.clock
                ):
                    # check to make sure timeout is not between/before FTs
                    return True
            elif isinstance(event, Timeout) and event.clock == self.end_time:
                timeout_time = event.clock
                after_timeout_index = i + 1
                # call time out and turn ball over at same time as timeout following time out
                for possession_event in self.events[after_timeout_index:]:
                    if (
                        isinstance(possession_event, Turnover)
                        and not possession_event.is_no_turnover
                        and possession_event.clock == timeout_time
                    ):
                        return True
        return False

    @property
    def previous_possession_has_timeout(self):
        """
        returns True if there was a timeout called at same time as possession ended, False otherwise
        """
        if self.previous_possession is not None:
            for event in self.previous_possession.events:
                if isinstance(event, Timeout) and event.clock == self.start_time:
                    if not (
                        event.next_event is not None
                        and isinstance(event.next_event, FreeThrow)
                        and event.clock == event.next_event.clock
                    ):
                        # check to make sure timeout is not beween FTs
                        return True
        return False

    @property
    def previous_possession_ending_event(self):
        """
        returns previous possession ending event - ignoring subs
        """
        previous_event_index = -1
        while isinstance(
            self.previous_possession.events[previous_event_index], Substitution
        ) and len(self.previous_possession.events) > abs(previous_event_index):
            previous_event_index -= 1
        return self.previous_possession.events[previous_event_index]

    @property
    def possession_start_type(self):
        """
        returns possession start type string
        """
        if self.number == 1:
            return pbpstats.OFF_DEADBALL_STRING
        if self.possession_has_timeout or self.previous_possession_has_timeout:
            return pbpstats.OFF_TIMEOUT_STRING
        previous_possession_ending_event = self.previous_possession_ending_event
        if (
            isinstance(previous_possession_ending_event, (FieldGoal, FreeThrow))
            and previous_possession_ending_event.is_made
        ):
            shot_type = previous_possession_ending_event.shot_type
            return f"Off{shot_type}{pbpstats.MAKE_STRING}"
        if isinstance(previous_possession_ending_event, Turnover):
            if previous_possession_ending_event.is_steal:
                return pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
            return pbpstats.OFF_DEADBALL_STRING
        if isinstance(previous_possession_ending_event, Rebound):
            if previous_possession_ending_event.player1_id == 0:
                # team rebound
                return pbpstats.OFF_DEADBALL_STRING
            missed_shot = previous_possession_ending_event.missed_shot
            shot_type = missed_shot.shot_type
            if hasattr(missed_shot, "is_blocked") and missed_shot.is_blocked:
                return f"Off{shot_type}{pbpstats.BLOCK_STRING}"
            return f"Off{shot_type}{pbpstats.MISS_STRING}"

        if isinstance(previous_possession_ending_event, JumpBall):
            # jump balls tipped out of bounds have no player2_id and should be off deadball
            if not hasattr(previous_possession_ending_event, "player2_id"):
                return pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
            else:
                return pbpstats.OFF_DEADBALL_STRING
        return pbpstats.OFF_DEADBALL_STRING

    @property
    def previous_possession_end_shooter_player_id(self):
        """
        returns player id of player who took shot (make or miss) that ended previous possession.
        returns 0 if previous possession did not end with made field goal or live ball rebound
        """
        if self.previous_possession is not None and not (
            self.possession_has_timeout or self.previous_possession_has_timeout
        ):
            previous_possession_ending_event = self.previous_possession_ending_event
            if (
                isinstance(previous_possession_ending_event, FieldGoal)
                and previous_possession_ending_event.is_made
            ):
                return previous_possession_ending_event.player1_id
            if isinstance(previous_possession_ending_event, Rebound):
                if previous_possession_ending_event.player1_id != 0:
                    missed_shot = previous_possession_ending_event.missed_shot
                    return missed_shot.player1_id
        return 0

    @property
    def previous_possession_end_rebound_player_id(self):
        """
        returns player id of player who got rebound that ended previous possession.
        returns 0 if previous possession did not end with a live ball rebound
        """
        if self.previous_possession is not None and not (
            self.possession_has_timeout or self.previous_possession_has_timeout
        ):
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, Rebound):
                if previous_possession_ending_event.player1_id != 0:
                    return previous_possession_ending_event.player1_id
        return 0

    @property
    def previous_possession_end_turnover_player_id(self):
        """
        returns player id of player who turned ball over that ended previous possession.
        returns 0 if previous possession did not end with a live ball turnover
        """
        if self.previous_possession is not None and not (
            self.possession_has_timeout or self.previous_possession_has_timeout
        ):
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, Turnover):
                if previous_possession_ending_event.is_steal:
                    return previous_possession_ending_event.player1_id
        return 0

    @property
    def previous_possession_end_steal_player_id(self):
        """
        returns player id of player who got steal that ended previous possession.
        returns 0 if previous possession did not end with a live ball turnover
        """
        if self.previous_possession is not None and not (
            self.possession_has_timeout or self.previous_possession_has_timeout
        ):
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, Turnover):
                if previous_possession_ending_event.is_steal:
                    return previous_possession_ending_event.player3_id
        return 0

    @property
    def possession_stats(self):
        """
        returns list of dicts with aggregate stats for possession
        """
        grouper = itemgetter(
            "player_id",
            "team_id",
            "opponent_team_id",
            "lineup_id",
            "opponent_lineup_id",
            "stat_key",
        )
        results = []
        event_stats = [
            event_stat for event in self.events for event_stat in event.event_stats
        ]
        for key, group in groupby(sorted(event_stats, key=grouper), grouper):
            temp_dict = dict(
                zip(
                    [
                        "player_id",
                        "team_id",
                        "opponent_team_id",
                        "lineup_id",
                        "opponent_lineup_id",
                        "stat_key",
                    ],
                    key,
                )
            )
            temp_dict["stat_value"] = sum(item["stat_value"] for item in group)
            results.append(temp_dict)

        return results
