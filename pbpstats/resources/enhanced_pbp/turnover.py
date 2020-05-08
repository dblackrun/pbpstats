import pbpstats
from pbpstats.resources.enhanced_pbp import Substitution


class Turnover(object):
    """
    Class for Turnover events
    """

    event_type = 5

    @property
    def is_steal(self):
        return hasattr(self, "player3_id")

    @property
    def is_no_turnover(self):
        return self.event_action_type == 0

    @property
    def is_bad_pass(self):
        return self.event_action_type == 1 and self.is_steal

    @property
    def is_lost_ball(self):
        return self.event_action_type == 2 and self.is_steal

    @property
    def is_travel(self):
        return self.event_action_type == 4

    @property
    def is_3_second_violation(self):
        return self.event_action_type == 8

    @property
    def is_shot_clock_violation(self):
        return self.event_action_type == 11

    @property
    def is_offensive_goaltending(self):
        return self.event_action_type == 15

    @property
    def is_lane_violation(self):
        return self.event_action_type == 17

    @property
    def is_kicked_ball(self):
        return self.event_action_type == 19

    @property
    def is_step_out_of_bounds(self):
        return self.event_action_type == 39

    @property
    def is_lost_ball_out_of_bounds(self):
        # some labelled as lost ball but should be lost ball out of bounds (missing player3 id)
        return self.event_action_type == 40 or (
            self.event_action_type == 2 and not self.is_steal
        )

    @property
    def is_bad_pass_out_of_bounds(self):
        # some labelled as bad pass but should be bad pass out of bounds (missing player3 id)
        return self.event_action_type == 45 or (
            self.event_action_type == 1 and not self.is_steal
        )

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        stats = []
        second_chance_stats = []
        if not self.is_no_turnover:
            team_ids = list(self.current_players.keys())
            opponent_team_id = (
                team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
            )
            lineup_ids = self.lineup_ids
            if self.is_steal:
                turnover_key = (
                    pbpstats.LOST_BALL_TURNOVER_STRING
                    if self.is_lost_ball
                    else pbpstats.BAD_PASS_TURNOVER_STRING
                )
                stats.append(
                    {
                        "player_id": self.player1_id,
                        "team_id": self.team_id,
                        "stat_key": turnover_key,
                        "stat_value": 1,
                    }
                )
                steal_key = (
                    pbpstats.LOST_BALL_STEAL_STRING
                    if self.is_lost_ball
                    else pbpstats.BAD_PASS_STEAL_STRING
                )
                stats.append(
                    {
                        "player_id": self.player3_id,
                        "team_id": opponent_team_id,
                        "stat_key": steal_key,
                        "stat_value": 1,
                    }
                )
            else:
                stats.append(
                    {
                        "player_id": self.player1_id,
                        "team_id": self.team_id,
                        "stat_key": pbpstats.DEADBALL_TURNOVERS_STRING,
                        "stat_value": 1,
                    }
                )
                if self.is_travel:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.TRAVELS_STRING,
                            "stat_value": 1,
                        }
                    )
                elif self.is_3_second_violation:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.THREE_SECOND_VIOLATION_TURNOVER_STRING,
                            "stat_value": 1,
                        }
                    )
                elif self.is_step_out_of_bounds:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.STEP_OUT_OF_BOUNDS_TURNOVER_STRING,
                            "stat_value": 1,
                        }
                    )
                elif self.is_offensive_goaltending:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.OFFENSIVE_GOALTENDING_STRING,
                            "stat_value": 1,
                        }
                    )
                elif self.is_lost_ball_out_of_bounds:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.LOST_BALL_OUT_OF_BOUNDS_TURNOVER_STRING,
                            "stat_value": 1,
                        }
                    )
                elif self.is_bad_pass_out_of_bounds:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.BAD_PASS_OUT_OF_BOUNDS_TURNOVER_STRING,
                            "stat_value": 1,
                        }
                    )
                elif self.is_shot_clock_violation:
                    stats.append(
                        {
                            "player_id": self.player1_id,
                            "team_id": self.team_id,
                            "stat_key": pbpstats.SHOT_CLOCK_VIOLATION_TURNOVER_STRING,
                            "stat_value": 1,
                        }
                    )

                # sometimes events are out of order and turnover happens after sub
                # if player who turned ball over is subbed out before turnover event, fix lineup id
                events_to_check = self.get_all_events_at_current_time()
                if self.player1_id != 0 and str(self.player1_id) not in lineup_ids[
                    self.team_id
                ].split("-"):
                    # sub in wrong order - fix lineup
                    for event in events_to_check:
                        if isinstance(event, Substitution):
                            if event.outgoing_player_id == self.player1_id:
                                fixed_lineup_id = lineup_ids[self.team_id].replace(
                                    str(event.incoming_player_id),
                                    str(event.outgoing_player_id),
                                )
                                lineup_ids[self.team_id] = fixed_lineup_id

            for stat in stats:
                opponent_team_id = (
                    team_ids[0] if stat["team_id"] == team_ids[1] else team_ids[1]
                )
                stat["lineup_id"] = lineup_ids[stat["team_id"]]
                stat["opponent_team_id"] = opponent_team_id
                stat["opponent_lineup_id"] = lineup_ids[opponent_team_id]
                if self.is_second_chance_event():
                    second_chance_stats.append(
                        {
                            key: value
                            if key != "stat_key"
                            else f"{pbpstats.SECOND_CHANCE_STRING}{value}"
                            for key, value in stat.items()
                        }
                    )
                if self.is_penalty_event():
                    second_chance_stats.append(
                        {
                            key: value
                            if key != "stat_key"
                            else f"{pbpstats.PENALTY_STRING}{value}"
                            for key, value in stat.items()
                        }
                    )

        return self.base_stats + stats + second_chance_stats
