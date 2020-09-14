import pbpstats


class Foul(object):
    """
    Class for foul events
    """

    event_type = 6

    @property
    def is_personal_foul(self):
        return self.event_action_type == 1

    @property
    def is_shooting_foul(self):
        return self.event_action_type == 2

    @property
    def is_loose_ball_foul(self):
        return self.event_action_type == 3

    @property
    def is_offensive_foul(self):
        return self.event_action_type == 4

    @property
    def is_inbound_foul(self):
        return self.event_action_type == 5

    @property
    def is_away_from_play_foul(self):
        return self.event_action_type == 6

    @property
    def is_clear_path_foul(self):
        return self.event_action_type == 9

    @property
    def is_double_foul(self):
        return self.event_action_type == 10

    @property
    def is_technical(self):
        return self.event_action_type in [11, 12, 13, 18, 19, 25, 30]

    @property
    def is_flagrant(self):
        return self.event_action_type in [14, 15]

    @property
    def is_double_technical(self):
        return self.event_action_type == 16

    @property
    def is_defensive_3_seconds(self):
        return self.event_action_type == 17

    @property
    def is_delay_of_game(self):
        return self.event_action_type == 18

    @property
    def is_charge(self):
        return self.event_action_type == 26

    @property
    def is_personal_block_foul(self):
        return self.event_action_type == 27

    @property
    def is_personal_take_foul(self):
        return self.event_action_type == 28

    @property
    def is_shooting_block_foul(self):
        return self.event_action_type == 29

    @property
    def counts_towards_penalty(self):
        """
        returns True if foul is a foul type that counts towards the penalty, False otherwise
        """
        return self.event_action_type in [1, 2, 3, 5, 6, 9, 14, 15, 27, 28, 29]

    @property
    def counts_as_personal_foul(self):
        """
        returns True if fouls is a foul type that counts as a personal foul, False otherwise
        """
        return self.event_action_type in [
            1,
            2,
            3,
            4,
            5,
            6,
            9,
            10,
            14,
            15,
            26,
            27,
            28,
            29,
        ]

    @property
    def foul_type_string(self):
        """
        returns string description of foul type
        """
        if self.is_personal_foul:
            return pbpstats.PERSONAL_FOUL_TYPE_STRING
        if self.is_shooting_foul:
            return pbpstats.SHOOTING_FOUL_TYPE_STRING
        if self.is_loose_ball_foul:
            return pbpstats.LOOSE_BALL_FOUL_TYPE_STRING
        if self.is_offensive_foul:
            return pbpstats.OFFENSIVE_FOUL_TYPE_STRING
        if self.is_inbound_foul:
            return pbpstats.INBOUND_FOUL_TYPE_STRING
        if self.is_away_from_play_foul:
            return pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING
        if self.is_clear_path_foul:
            return pbpstats.CLEAR_PATH_FOUL_TYPE_STRING
        if self.is_double_foul:
            return pbpstats.DOUBLE_FOUL_TYPE_STRING
        if self.event_action_type == 14:
            return pbpstats.FLAGRANT_1_FOUL_TYPE_STRING
        if self.event_action_type == 15:
            return pbpstats.FLAGRANT_2_FOUL_TYPE_STRING
        if self.is_defensive_3_seconds:
            return pbpstats.DEFENSIVE_3_SECONDS_FOUL_TYPE_STRING
        if self.is_charge:
            return pbpstats.CHARGE_FOUL_TYPE_STRING
        if self.is_personal_block_foul:
            return pbpstats.PERSONAL_BLOCK_TYPE_STRING
        if self.is_personal_take_foul:
            return pbpstats.PERSONAL_TAKE_TYPE_STRING
        if self.is_shooting_block_foul:
            return pbpstats.SHOOTING_BLOCK_TYPE_STRING

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        stats = []
        foul_type = self.foul_type_string
        is_penalty_event = self.is_penalty_event()
        if foul_type is not None:
            stats.append(
                {
                    "player_id": self.player1_id,
                    "team_id": self.team_id,
                    "stat_key": foul_type,
                    "stat_value": 1,
                }
            )
            if is_penalty_event:
                stats.append(
                    {
                        "player_id": self.player1_id,
                        "team_id": self.team_id,
                        "stat_key": f"{pbpstats.PENALTY_STRING}{foul_type}",
                        "stat_value": 1,
                    }
                )
            team_ids = list(self.current_players.keys())
            if hasattr(self, "player3_id"):
                p3_stat_key = (
                    foul_type
                    if self.is_double_foul
                    else foul_type + pbpstats.FOULS_DRAWN_TYPE_STRING
                )
                opponent_team_id = (
                    team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
                )
                if self.player3_id in self.current_players[self.team_id]:
                    stats.append(
                        {
                            "player_id": self.player3_id,
                            "team_id": self.team_id,
                            "stat_key": p3_stat_key,
                            "stat_value": 1,
                        }
                    )
                    if is_penalty_event:
                        stats.append(
                            {
                                "player_id": self.player3_id,
                                "team_id": self.team_id,
                                "stat_key": f"{pbpstats.PENALTY_STRING}{p3_stat_key}",
                                "stat_value": 1,
                            }
                        )
                elif self.player3_id in self.current_players[opponent_team_id]:
                    stats.append(
                        {
                            "player_id": self.player3_id,
                            "team_id": opponent_team_id,
                            "stat_key": p3_stat_key,
                            "stat_value": 1,
                        }
                    )
                    if is_penalty_event:
                        stats.append(
                            {
                                "player_id": self.player3_id,
                                "team_id": opponent_team_id,
                                "stat_key": f"{pbpstats.PENALTY_STRING}{p3_stat_key}",
                                "stat_value": 1,
                            }
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
