import abc

import pbpstats


class Foul(object):
    """
    Class for foul events
    """

    @abc.abstractproperty
    def number_of_fta_for_foul(self):
        """
        returns the number of free throws resulting from the foul
        """
        pass

    @abc.abstractproperty
    def is_personal_foul(self):
        pass

    @abc.abstractproperty
    def is_shooting_foul(self):
        pass

    @abc.abstractproperty
    def is_loose_ball_foul(self):
        pass

    @abc.abstractproperty
    def is_offensive_foul(self):
        pass

    @abc.abstractproperty
    def is_inbound_foul(self):
        pass

    @abc.abstractproperty
    def is_away_from_play_foul(self):
        pass

    @abc.abstractproperty
    def is_clear_path_foul(self):
        pass

    @abc.abstractproperty
    def is_double_foul(self):
        pass

    @abc.abstractproperty
    def is_technical(self):
        pass

    @property
    def is_flagrant(self):
        return self.is_flagrant1 or self.is_flagrant2

    @abc.abstractproperty
    def is_flagrant1(self):
        pass

    @abc.abstractproperty
    def is_flagrant2(self):
        pass

    @abc.abstractproperty
    def is_double_technical(self):
        pass

    @abc.abstractproperty
    def is_defensive_3_seconds(self):
        pass

    @abc.abstractproperty
    def is_delay_of_game(self):
        pass

    @abc.abstractproperty
    def is_charge(self):
        pass

    @abc.abstractproperty
    def is_personal_block_foul(self):
        pass

    @abc.abstractproperty
    def is_personal_take_foul(self):
        pass

    @abc.abstractproperty
    def is_shooting_block_foul(self):
        pass

    @property
    def counts_towards_penalty(self):
        """
        returns True if foul is a foul type that counts towards the penalty, False otherwise
        """
        if self.is_personal_foul:
            return True
        if self.is_shooting_foul:
            return True
        if self.is_loose_ball_foul:
            return True
        if self.is_inbound_foul:
            return True
        if self.is_away_from_play_foul:
            return True
        if self.is_clear_path_foul:
            return True
        if self.is_flagrant:
            return True
        if self.is_personal_block_foul:
            return True
        if self.is_personal_take_foul:
            return True
        if self.is_shooting_block_foul:
            return True
        return False

    @property
    def counts_as_personal_foul(self):
        """
        returns True if fouls is a foul type that counts as a personal foul, False otherwise
        """
        if self.is_personal_foul:
            return True
        if self.is_shooting_foul:
            return True
        if self.is_loose_ball_foul:
            return True
        if self.is_offensive_foul:
            return True
        if self.is_inbound_foul:
            return True
        if self.is_away_from_play_foul:
            return True
        if self.is_clear_path_foul:
            return True
        if self.is_double_foul:
            return True
        if self.is_flagrant:
            return True
        if self.is_charge:
            return True
        if self.is_personal_block_foul:
            return True
        if self.is_personal_take_foul:
            return True
        if self.is_shooting_block_foul:
            return True

        return False

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
        if self.is_flagrant1:
            return pbpstats.FLAGRANT_1_FOUL_TYPE_STRING
        if self.is_flagrant2:
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
