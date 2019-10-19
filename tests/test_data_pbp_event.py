import pbpstats
from pbpstats.data_pbp_event import DataPbpEvent
from pbpstats.data_period import DataPeriod


class TestDataPbpEvent:
    GameId = '0021600270'
    Period = 1

    def test_made_fg_is_made_fg(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 28, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_made_fg() is True

    def test_missed_fg_is_made_fg(self):
        event = DataPbpEvent({'evt': 14, 'cl': '10:34', 'de': '[BKN] Bogdanovic Layup Shot: Missed', 'locX': 4, 'locY': 16, 'mtype': 5, 'etype': 2, 'opid': '', 'tid': 1610612751, 'pid': 202711, 'hs': 2, 'vs': 2, 'epid': '', 'oftid': 1610612751})
        assert event.is_made_fg() is False

    def test_missed_fg_is_missed_fg(self):
        event = DataPbpEvent({'evt': 14, 'cl': '10:34', 'de': '[BKN] Bogdanovic Layup Shot: Missed', 'locX': 4, 'locY': 16, 'mtype': 5, 'etype': 2, 'opid': '', 'tid': 1610612751, 'pid': 202711, 'hs': 2, 'vs': 2, 'epid': '', 'oftid': 1610612751})
        assert event.is_missed_fg() is True

    def test_made_fg_is_missed_fg(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 28, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_missed_fg() is False

    def test_assisted_shot_is_assisted_shot(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 28, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_assisted_shot() is True

    def test_unassisted_shot_is_assisted_shot(self):
        event = DataPbpEvent({'evt': 21, 'cl': '09:31', 'de': '[BKN 4-5] Bogdanovic Driving Layup Shot: Made (2 PTS)', 'locX': 9, 'locY': 13, 'mtype': 42, 'etype': 1, 'opid': '', 'tid': 1610612751, 'pid': 202711, 'hs': 5, 'vs': 4, 'epid': '', 'oftid': 1610612751})
        assert event.is_assisted_shot() is False

    def test_3pt_shot_is_3pt_shot(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 28, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_3pt_shot() is True

    def test_layup_is_3pt_shot(self):
        event = DataPbpEvent({'evt': 14, 'cl': '10:34', 'de': '[BKN] Bogdanovic Layup Shot: Missed', 'locX': 4, 'locY': 16, 'mtype': 5, 'etype': 2, 'opid': '', 'tid': 1610612751, 'pid': 202711, 'hs': 2, 'vs': 2, 'epid': '', 'oftid': 1610612751})
        assert event.is_3pt_shot() is False

    def test_corner3_is_corner_3(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 28, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_corner_3() is True

    def test_non_corner3_is_corner_3(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 100, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_corner_3() is False

    def test_non_shot_event_with_corner3_coordinates_is_corner_3(self):
        event = DataPbpEvent({'evt': 87, 'cl': '03:17', 'de': '[NYK] Thomas Rebound (Off:0 Def:1)', 'locX': -230, 'locY': 28, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612752, 'pid': 202498, 'hs': 14, 'vs': 22, 'epid': '', 'oftid': 1610612751})
        assert event.is_corner_3() is False

    def test_missing_coordinates_is_corner_3(self):
        event = DataPbpEvent({'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': None, 'locY': None, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752})
        assert event.is_corner_3() is False

    def test_10ft_shot_get_shot_distance(self):
        event = DataPbpEvent({'evt': 115, 'cl': '00:45.9', 'de': '[NYK] Anthony Jump Shot: Missed', 'locX': 0, 'locY': 100, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612752, 'pid': 2546, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.get_shot_distance() == 10

    def test_18ft_shot_get_shot_distance(self):
        event = DataPbpEvent({'evt': 115, 'cl': '00:45.9', 'de': '[NYK] Anthony Jump Shot: Missed', 'locX': 100, 'locY': 150, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612752, 'pid': 2546, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.get_shot_distance() == 18

    def test_18ft_shot_with_negative_x_coord_get_shot_distance(self):
        event = DataPbpEvent({'evt': 115, 'cl': '00:45.9', 'de': '[NYK] Anthony Jump Shot: Missed', 'locX': -100, 'locY': 150, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612752, 'pid': 2546, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.get_shot_distance() == 18

    def test_no_coords_get_shot_distance(self):
        event = DataPbpEvent({'evt': 115, 'cl': '00:45.9', 'de': "[NYK] Anthony 16' Jump Shot: Missed", 'locX': None, 'locY': None, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612752, 'pid': 2546, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.get_shot_distance() == 16

    def test_non_fg_get_shot_distance(self):
        event = DataPbpEvent({'evt': 110, 'cl': '01:09', 'de': "[NYK 17-27] O'Quinn Free Throw 2 of 2 (3 PTS)", 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.get_shot_distance() is None

    def test_no_coords_no_distance_in_description_get_shot_distance(self):
        event = DataPbpEvent({'evt': 115, 'cl': '00:45.9', 'de': '[NYK] Anthony Jump Shot: Missed', 'locX': None, 'locY': None, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612752, 'pid': 2546, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.get_shot_distance() is None

    def test_made_ft_is_made_ft(self):
        event = DataPbpEvent({'evt': 110, 'cl': '01:09', 'de': "[NYK 17-27] O'Quinn Free Throw 2 of 2 (3 PTS)", 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_made_ft() is True

    def test_missed_ft_is_made_ft(self):
        event = DataPbpEvent({'evt': 108, 'cl': '01:09', 'de': "[NYK] O'Quinn Free Throw 1 of 2 Missed", 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 16, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_made_ft() is False

    def test_made_ft_is_missed_ft(self):
        event = DataPbpEvent({'evt': 110, 'cl': '01:09', 'de': "[NYK 17-27] O'Quinn Free Throw 2 of 2 (3 PTS)", 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_missed_ft() is False

    def test_missed_ft_is_missed_ft(self):
        event = DataPbpEvent({'evt': 108, 'cl': '01:09', 'de': "[NYK] O'Quinn Free Throw 1 of 2 Missed", 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 16, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_missed_ft() is True

    def test_substitution_is_substitution(self):
        event = DataPbpEvent({'evt': 126, 'cl': '00:08.8', 'de': "[NYK] O'Quinn Substitution replaced by Porzingis", 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 19, 'vs': 29, 'epid': '204001', 'oftid': 1610612752})
        assert event.is_substitution() is True

    def test_ft_is_substitution(self):
        event = DataPbpEvent({'evt': 108, 'cl': '01:09', 'de': "[NYK] O'Quinn Free Throw 1 of 2 Missed", 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 16, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_substitution() is False

    def test_technical_foul_is_technical_foul(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 11})
        assert event.is_technical_foul() is True

    def test_non_technical_foul_is_technical_foul(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 16})
        assert event.is_technical_foul() is False

    def test_double_technical_is_double_technical_foul(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 11})
        assert event.is_double_technical_foul() is False

    def test_non_double_technical_is_double_technical_foul(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 16})
        assert event.is_double_technical_foul() is True

    def test_ejection_is_ejection(self):
        event = DataPbpEvent({'etype': 11, 'mtype': 11})
        assert event.is_ejection() is True

    def test_non_ejection_is_ejection(self):
        event = DataPbpEvent({'etype': 16, 'mtype': 16})
        assert event.is_ejection() is False

    def test_turnover_is_turnover(self):
        event = DataPbpEvent({'evt': 162, 'cl': '09:07', 'de': '[BKN] Ferrell Turnover : Bad Pass (2 TO) Steal:Ndour (1 ST)', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 5, 'opid': '1626254', 'tid': 1610612751, 'pid': 1627812, 'hs': 25, 'vs': 37, 'epid': '', 'oftid': 1610612751})
        assert event.is_turnover() is True

    def test_ft_is_turnover(self):
        event = DataPbpEvent({'evt': 108, 'cl': '01:09', 'de': "[NYK] O'Quinn Free Throw 1 of 2 Missed", 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 16, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_turnover() is False

    def test_no_turnover_is_turnover(self):
        event = DataPbpEvent({'evt': 325, 'cl': '08:06', 'de': '[WAS] Wall Turnover : No Turnover (3 TO) Steal:Smart (1 ST)', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 5, 'opid': '203935', 'tid': 1610612764, 'pid': 202322, 'hs': 67, 'vs': 47, 'epid': '', 'oftid': 1610612764})
        assert event.is_turnover() is False

    def test_steal_is_steal(self):
        event = DataPbpEvent({'evt': 162, 'cl': '09:07', 'de': '[BKN] Ferrell Turnover : Bad Pass (2 TO) Steal:Ndour (1 ST)', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 5, 'opid': '1626254', 'tid': 1610612751, 'pid': 1627812, 'hs': 25, 'vs': 37, 'epid': '', 'oftid': 1610612751})
        assert event.is_steal() is True

    def test_out_of_bounds_is_steal(self):
        event = DataPbpEvent({'evt': 166, 'cl': '08:31', 'de': '[NYK] Jennings Turnover : Out of Bounds - Bad Pass Turnover (2 TO)', 'locX': 0, 'locY': -80, 'mtype': 45, 'etype': 5, 'opid': '', 'tid': 1610612752, 'pid': 201943, 'hs': 27, 'vs': 37, 'epid': '', 'oftid': 1610612752})
        assert event.is_steal() is False

    def test_shot_clock_violation_is_shot_clock_violation(self):
        event = DataPbpEvent({'etype': 5, 'mtype': 11})
        assert event.is_shot_clock_violation() is True

    def test_steal_is_shot_clock_violation(self):
        event = DataPbpEvent({'evt': 162, 'cl': '09:07', 'de': '[BKN] Ferrell Turnover : Bad Pass (2 TO) Steal:Ndour (1 ST)', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 5, 'opid': '1626254', 'tid': 1610612751, 'pid': 1627812, 'hs': 25, 'vs': 37, 'epid': '', 'oftid': 1610612751})
        assert event.is_shot_clock_violation() is False

    def test_support_ruling_is_replay_challenge_support_ruling(self):
        event = DataPbpEvent({'etype': 18, 'mtype': 4})
        assert event.is_replay_challenge_support_ruling() is True

    def test_overturn_ruling_is_replay_challenge_support_ruling(self):
        event = DataPbpEvent({'etype': 18, 'mtype': 5})
        assert event.is_replay_challenge_support_ruling() is False

    def test_overturn_ruling_is_replay_challenge_overturn_ruling(self):
        event = DataPbpEvent({'etype': 18, 'mtype': 5})
        assert event.is_replay_challenge_overturn_ruling() is True

    def test_support_ruling_is_replay_challenge_overturn_ruling(self):
        event = DataPbpEvent({'etype': 18, 'mtype': 4})
        assert event.is_replay_challenge_overturn_ruling() is False

    def test_ruling_stands_is_replay_challenge_ruling_stands(self):
        event = DataPbpEvent({'etype': 18, 'mtype': 6})
        assert event.is_replay_challenge_ruling_stands() is True

    def test_overturn_ruling_is_replay_challenge_ruling_stands(self):
        event = DataPbpEvent({'etype': 18, 'mtype': 5})
        assert event.is_replay_challenge_ruling_stands() is False

    def test_rebound_is_rebound(self):
        event = DataPbpEvent({'evt': 172, 'cl': '08:18', 'de': '[NYK] Ndour Rebound (Off:0 Def:2)', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612752, 'pid': 1626254, 'hs': 27, 'vs': 38, 'epid': '', 'oftid': 1610612751})
        assert event.is_rebound() is True

    def test_rebound_with_mtype_1_is_rebound(self):
        event = DataPbpEvent({'evt': 116, 'cl': '00:45.5', 'de': '[BKN] Team Rebound', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 4, 'opid': '', 'tid': 1610612751, 'pid': 0, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_rebound() is False

    def test_rebound_with_mtype_1_and_pid_is_rebound(self):
        event = DataPbpEvent({'evt': 172, 'cl': '08:18', 'de': '[NYK] Ndour Rebound (Off:0 Def:2)', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 4, 'opid': '', 'tid': 1610612752, 'pid': 1626254, 'hs': 27, 'vs': 38, 'epid': '', 'oftid': 1610612751})
        assert event.is_rebound() is True

    def test_miss_rebound_make_is_putback(self):
        events = DataPeriod(
            [
                {'etype': 2, 'cl': '1:06', 'pid': 12, 'tid': 1, 'de': ''},
                {'etype': 4, 'mtype': 0, 'cl': '1:03', 'pid': 12, 'tid': 1},
                {'etype': 1, 'cl': '1:02', 'pid': 12, 'de': '', 'tid': 1}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is True

    def test_miss_rebound_make_outside_time_cutoff_is_putback(self):
        events = DataPeriod(
            [
                {'etype': 2, 'cl': '1:06', 'pid': 12, 'tid': 1, 'de': ''},
                {'etype': 4, 'mtype': 0, 'cl': '1:05', 'pid': 12, 'tid': 1},
                {'etype': 1, 'cl': '1:02', 'pid': 12, 'de': '', 'tid': 1}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_rebound_make_by_different_player_is_putback(self):
        events = DataPeriod(
            [
                {'etype': 2, 'cl': '1:06', 'pid': 12, 'tid': 1, 'de': ''},
                {'etype': 4, 'mtype': 0, 'cl': '1:03', 'pid': 12, 'tid': 1},
                {'etype': 1, 'cl': '1:02', 'pid': 11, 'de': '', 'tid': 1}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_rebound_assisted_make_is_putback(self):
        events = DataPeriod(
            [
                {'etype': 2, 'cl': '1:06', 'pid': 12, 'tid': 1, 'de': ''},
                {'etype': 4, 'mtype': 0, 'cl': '1:03', 'pid': 12, 'tid': 1},
                {'etype': 1, 'cl': '1:02', 'pid': 12, 'de': 'Assist: ', 'tid': 1}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_by_other_team_rebound_make_is_putback(self):
        events = DataPeriod(
            [
                {'etype': 2, 'cl': '1:06', 'pid': 121, 'tid': 2, 'de': ''},
                {'etype': 4, 'mtype': 0, 'cl': '1:03', 'pid': 12, 'tid': 1},
                {'etype': 1, 'cl': '1:02', 'pid': 12, 'de': '', 'tid': 1}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_rebound_and1_foul_make_is_putback(self):
        # shooting foul event between rebound and made shot - pbp out of order
        events = DataPeriod(
            [
                {'evt': 591, 'cl': '02:36', 'de': '[NOP] Davis Driving Layup Shot: Missed', 'locX': -41, 'locY': 21, 'mtype': 6, 'etype': 2, 'opid': '203991', 'tid': 1610612740, 'pid': 203076, 'hs': 94, 'vs': 101, 'epid': '', 'oftid': 1610612740, 'ord': 563000},
                {'evt': 593, 'cl': '02:36', 'de': '[NOP] Randle Rebound (Off:3 Def:7)', 'locX': -41, 'locY': 21, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612740, 'pid': 203944, 'hs': 94, 'vs': 101, 'epid': '', 'oftid': 1610612740, 'ord': 563500},
                {'evt': 592, 'cl': '02:36', 'de': '[HOU] Capela Foul: Shooting (4 PF) (1 FTA) (Z Zarba)', 'locX': -41, 'locY': 21, 'mtype': 2, 'etype': 6, 'opid': '203944', 'tid': 1610612745, 'pid': 203991, 'hs': 96, 'vs': 101, 'epid': '', 'oftid': 1610612740, 'ord': 564000},
                {'evt': 609, 'cl': '02:36', 'de': '[NOP 96-101] Randle Putback Layup Shot: Made (23 PTS)', 'locX': -11, 'locY': 62, 'mtype': 72, 'etype': 1, 'opid': '', 'tid': 1610612740, 'pid': 203944, 'hs': 96, 'vs': 101, 'epid': '', 'oftid': 1610612740, 'ord': 563750},
                {'evt': 595, 'cl': '02:36', 'de': '[NOP] Randle Free Throw 1 of 1 Missed', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612740, 'pid': 203944, 'hs': 96, 'vs': 101, 'epid': '', 'oftid': 1610612740, 'ord': 566000}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].is_putback() is True

    def test_miss_rebound_goaltend_make_is_putback(self):
        events = DataPeriod(
            [
                {'evt': 781, 'cl': '01:14', 'de': '[PHI] Shamet Driving Floating Jump Shot: Missed', 'locX': 72, 'locY': 20, 'mtype': 101, 'etype': 2, 'opid': '', 'tid': 1610612755, 'pid': 1629013, 'hs': 120, 'vs': 106, 'epid': '', 'oftid': 1610612755, 'ord': 746500},
                {'evt': 783, 'cl': '01:13', 'de': '[PHI] Muscala Rebound (Off:1 Def:3)', 'locX': 72, 'locY': 20, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612755, 'pid': 203488, 'hs': 120, 'vs': 106, 'epid': '', 'oftid': 1610612755, 'ord': 746750},
                {'evt': 785, 'cl': '01:12', 'de': '[MIL] DiVincenzo Violation:Defensive Goaltending (N Buchert)', 'locX': 0, 'locY': -80, 'mtype': 2, 'etype': 7, 'opid': '', 'tid': 1610612749, 'pid': 1628978, 'hs': 120, 'vs': 108, 'epid': '', 'oftid': 1610612755, 'ord': 747976},
                {'evt': 784, 'cl': '01:12', 'de': '[PHI 108-120] Muscala Tip Layup Shot: Made (8 PTS)', 'locX': -8, 'locY': 3, 'mtype': 97, 'etype': 1, 'opid': '', 'tid': 1610612755, 'pid': 203488, 'hs': 120, 'vs': 108, 'epid': '', 'oftid': 1610612755, 'ord': 747953},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].is_putback() is True

    def test_foul_is_foul(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 0})
        assert event.is_foul() is True

    def test_rebound_is_foul(self):
        event = DataPbpEvent({'etype': 4, 'mtype': 1})
        assert event.is_foul() is False

    def test_personal_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 1})
        assert event.get_foul_type() == pbpstats.PERSONAL_FOUL_TYPE_STRING

    def test_shooting_foul_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 2})
        assert event.get_foul_type() == pbpstats.SHOOTING_FOUL_TYPE_STRING

    def test_loose_ball_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 3})
        assert event.get_foul_type() == pbpstats.LOOSE_BALL_FOUL_TYPE_STRING

    def test_offensive_foul_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 4})
        assert event.get_foul_type() == pbpstats.OFFENSIVE_FOUL_TYPE_STRING

    def test_inbound_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 5})
        assert event.get_foul_type() == pbpstats.INBOUND_FOUL_TYPE_STRING

    def test_away_from_play_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 6})
        assert event.get_foul_type() == pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING

    def test_clear_path_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 9})
        assert event.get_foul_type() == pbpstats.CLEAR_PATH_FOUL_TYPE_STRING

    def test_double_foul_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 10})
        assert event.get_foul_type() == pbpstats.DOUBLE_FOUL_TYPE_STRING

    def test_flagrant1_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 14})
        assert event.get_foul_type() == pbpstats.FLAGRANT_1_FOUL_TYPE_STRING

    def test_flagrant2_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 15})
        assert event.get_foul_type() == pbpstats.FLAGRANT_2_FOUL_TYPE_STRING

    def test_def_3_seconds_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 17})
        assert event.get_foul_type() == pbpstats.DEFENSIVE_3_SECONDS_FOUL_TYPE_STRING

    def test_charge_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 26})
        assert event.get_foul_type() == pbpstats.CHARGE_FOUL_TYPE_STRING

    def test_block_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 27})
        assert event.get_foul_type() == pbpstats.PERSONAL_BLOCK_TYPE_STRING

    def test_take_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 28})
        assert event.get_foul_type() == pbpstats.PERSONAL_TAKE_TYPE_STRING

    def test_shooting_block_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 29})
        assert event.get_foul_type() == pbpstats.SHOOTING_BLOCK_TYPE_STRING

    def test_unknown_mtype_get_foul_type(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 909})
        assert event.get_foul_type() is None

    def test_non_foul_get_foul_type(self):
        event = DataPbpEvent({'etype': 5, 'mtype': 1})
        assert event.get_foul_type() is None

    def test_personal_is_foul_that_counts_toward_penalty(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 1})
        assert event.is_foul_that_counts_toward_penalty() is True

    def test_offensive_foul_is_foul_that_counts_toward_penalty(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 4})
        assert event.is_foul_that_counts_toward_penalty() is False

    def test_1_of_2_is_first_ft(self):
        event = DataPbpEvent({'evt': 110, 'cl': '01:09', 'de': "[NYK 17-27] O'Quinn Free Throw 1 of 2 (3 PTS)", 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_first_ft() is True

    def test_2_of_2_is_first_ft(self):
        event = DataPbpEvent({'evt': 110, 'cl': '01:09', 'de': "[NYK 17-27] O'Quinn Free Throw 2 of 2 (3 PTS)", 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_first_ft() is False

    def test_tech_is_technical_ft(self):
        event = DataPbpEvent({'evt': 91, 'cl': '03:21', 'de': '[BOS] Bradley Free Throw Technical Missed', 'locX': 0, 'locY': -80, 'mtype': 16, 'etype': 3, 'opid': '', 'tid': 1610612738, 'pid': 202340, 'hs': 28, 'vs': 6, 'epid': '', 'oftid': 1610612738})
        assert event.is_technical_ft() is True

    def test_2_of_2_is_technical_ft(self):
        event = DataPbpEvent({'evt': 110, 'cl': '01:09', 'de': "[NYK 17-27] O'Quinn Free Throw 2 of 2 (3 PTS)", 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612752, 'pid': 203124, 'hs': 17, 'vs': 27, 'epid': '', 'oftid': 1610612752})
        assert event.is_technical_ft() is False

    def test_blocked_shot_is_blocked_shot(self):
        event = DataPbpEvent({'evt': 59, 'cl': '05:27', 'de': '[NYK] Porzingis Layup Shot: Missed Block: Lopez (1 BLK)', 'locX': 12, 'locY': 26, 'mtype': 5, 'etype': 2, 'opid': '201572', 'tid': 1610612752, 'pid': 204001, 'hs': 12, 'vs': 14, 'epid': '', 'oftid': 1610612752})
        assert event.is_blocked_shot() is True

    def test_missed_shot_is_blocked_shot(self):
        event = DataPbpEvent({'evt': 61, 'cl': '05:21', 'de': '[BKN] Hollis-Jefferson Layup Shot: Missed', 'locX': -9, 'locY': 7, 'mtype': 5, 'etype': 2, 'opid': '', 'tid': 1610612751, 'pid': 1626178, 'hs': 12, 'vs': 14, 'epid': '', 'oftid': 1610612751})
        assert event.is_blocked_shot() is False

    def test_get_and1_shot(self):
        events = DataPeriod(
            [
                {'etype': 1, 'cl': '3:20'},
                {'etype': 6, 'cl': '3:20'},
                {'etype': 8, 'cl': '3:20'},
                {'etype': 39, 'cl': '3:20'},
                {'etype': 39, 'cl': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[1].get_and1_shot() == events.Events[0]

    def test_1_fta_get_number_of_fta_for_foul(self):
        events = DataPeriod([{'etype': 6, 'de': 'asdgsg (1 FTA)'}], self.GameId, self.Period)
        assert events.Events[0].get_number_of_fta_for_foul() == 1

    def test_2_fta_get_number_of_fta_for_foul(self):
        events = DataPeriod([{'etype': 6, 'de': 'asdgsg (2 FTA)'}], self.GameId, self.Period)
        assert events.Events[0].get_number_of_fta_for_foul() == 2

    def test_3_fta_get_number_of_fta_for_foul(self):
        events = DataPeriod([{'etype': 6, 'de': 'asdgsg (3 FTA)'}], self.GameId, self.Period)
        assert events.Events[0].get_number_of_fta_for_foul() == 3

    def test_1_fta_on_away_from_play_on_made_ft_get_number_of_fta_for_foul(self):
        events = DataPeriod(
            [
                {'evt': 607, 'cl': '00:24.9', 'de': '[DET 121-111] Jackson Free Throw 2 of 2 (16 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612765, 'pid': 202704, 'hs': 121, 'vs': 111, 'epid': '', 'oftid': 1610612765, 'ord': 6050000},
                {'evt': 608, 'cl': '00:24.9', 'de': '[WAS] Team Timeout : Regular', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 9, 'opid': '', 'tid': 1610612764, 'pid': 1610612764, 'hs': 121, 'vs': 111, 'epid': '', 'oftid': 1610612764, 'ord': 6060000},
                {'evt': 609, 'cl': '00:24.9', 'de': '[DET] Griffin Foul: Away From Play (5 PF) (1 FTA) (M Davis)', 'locX': -109, 'locY': 100, 'mtype': 6, 'etype': 6, 'opid': '201145', 'tid': 1610612765, 'pid': 201933, 'hs': 121, 'vs': 111, 'epid': '', 'oftid': 1610612764, 'ord': 6070000},
                {'evt': 611, 'cl': '00:24.9', 'de': '[WAS 112-121] Beal Free Throw 1 of 1 (32 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612764, 'pid': 203078, 'hs': 121, 'vs': 112, 'epid': '', 'oftid': 1610612764, 'ord': 6090000},
                {'evt': 612, 'cl': '00:23.5', 'de': '[WAS] Green 3pt Shot: Missed', 'locX': -221, 'locY': 157, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612764, 'pid': 201145, 'hs': 121, 'vs': 112, 'epid': '', 'oftid': 1610612764, 'ord': 6100000}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_number_of_fta_for_foul() == 1

        events = DataPeriod(
            [
                {'evt': 168, 'cl': '00:38.8', 'de': '[POR 27-30] Lillard Free Throw 1 of 2 (7 PTS)', 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612757, 'pid': 203081, 'hs': 27, 'vs': 30, 'epid': '', 'oftid': 1610612757, 'ord': 1680000},
                {'evt': 169, 'cl': '00:38.8', 'de': '[POR] Layman Substitution replaced by Aminu', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612757, 'pid': 1627774, 'hs': 27, 'vs': 30, 'epid': '202329', 'oftid': 1610612757, 'ord': 1690000},
                {'evt': 171, 'cl': '00:38.8', 'de': '[POR 28-30] Lillard Free Throw 2 of 2 (8 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612757, 'pid': 203081, 'hs': 28, 'vs': 30, 'epid': '', 'oftid': 1610612757, 'ord': 1710000},
                {'evt': 172, 'cl': '00:38.8', 'de': '[OKC] Noel Foul: Away From Play (2 PF) (1 FTA) (M Ervin)', 'locX': -11, 'locY': 27, 'mtype': 6, 'etype': 6, 'opid': '202683', 'tid': 1610612760, 'pid': 203457, 'hs': 28, 'vs': 30, 'epid': '', 'oftid': 1610612757, 'ord': 1720000},
                {'evt': 174, 'cl': '00:38.8', 'de': '[POR 29-30] Kanter Free Throw 1 of 1 (1 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612757, 'pid': 202683, 'hs': 29, 'vs': 30, 'epid': '', 'oftid': 1610612757, 'ord': 1740000}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].get_number_of_fta_for_foul() == 1

    def test_get_foul_that_resulted_in_ft_excluding_techs(self):
        events = DataPeriod(
            [
                {'etype': 6, 'mtype': 2, 'cl': '3:20'},
                {'etype': 6, 'mtype': 2, 'cl': '3:20'},
                {'etype': 3, 'cl': '3:20'},
                {'etype': 11, 'mtype': 2, 'cl': '3:20'},
                {'etype': 8, 'mtype': 2, 'cl': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_foul_that_resulted_in_ft_excluding_techs() == events.Events[1]

    def test_ignore_tech_get_foul_that_resulted_in_ft_excluding_techs(self):
        # technical which should be ignored at index 1 which should be ignored
        events = DataPeriod(
            [
                {'etype': 6, 'mtype': 2, 'cl': '3:20'},
                {'etype': 6, 'mtype': 11, 'cl': '3:20'},
                {'etype': 3, 'cl': '3:20'},
                {'etype': 11, 'mtype': 2, 'cl': '3:20'},
                {'etype': 8, 'mtype': 2, 'cl': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_foul_that_resulted_in_ft_excluding_techs() == events.Events[0]

    def testset_next_and_previous_event_for_all_events(self):
        events = DataPeriod(
            [
                {'etype': 1, 'cl': '3:20'},
                {'etype': 6, 'cl': '3:20'},
                {'etype': 8, 'cl': '3:20'},
                {'etype': 39, 'cl': '3:20'},
                {'etype': 39, 'cl': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[0].previous_event is None
        assert events.Events[0].next_event.order == 1
        assert events.Events[4].previous_event.order == 3
        assert events.Events[4].next_event is None

    def test_player_def_reb_get_rebound_data(self):
        '''
        test for checking rebound type is correct
        '''
        player_def_2pt_reb_shot = {
            'cl': '10:26',
            'etype': 2,
            'mtype': 0,
            'tid': 111,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2
        }
        player_def_2pt_reb = {
            'cl': '10:24',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        player_def_3pt_reb_shot = {
            'cl': '10:18',
            'etype': 2,
            'mtype': 0,
            'tid': 1111,
            'pid': 123,
            'de': 'miss 3pt Shot',
            'locX': 200,
            'locY': 110
        }
        player_def_3pt_reb = {
            'cl': '10:16',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }
        player_def_ft_reb_shot = {
            'cl': '10:15',
            'etype': 3,
            'mtype': 12,
            'tid': 111,
            'pid': 123,
            'de': 'Missed Free Throw 2 of 2',
            'locX': 0,
            'locY': 0
        }
        player_def_ft_reb = {
            'cl': '10:14',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        pbp = DataPeriod(
            [
                player_def_2pt_reb_shot,
                player_def_2pt_reb,
                player_def_3pt_reb_shot,
                player_def_3pt_reb,
                player_def_ft_reb_shot,
                player_def_ft_reb
            ],
            self.GameId,
            self.Period
        )

        player_def_2pt_reb_data = pbp.Events[1].get_rebound_data()
        assert player_def_2pt_reb_data['def_reb'] is True
        assert player_def_2pt_reb_data['player_reb'] is True
        assert player_def_2pt_reb_data['three'] is False
        assert player_def_2pt_reb_data['ft'] is False
        assert player_def_2pt_reb_data['player_id'] == '12345'
        assert player_def_2pt_reb_data['team_id'] == '909'

        player_def_3pt_reb_data = pbp.Events[3].get_rebound_data()
        assert player_def_3pt_reb_data['def_reb'] is True
        assert player_def_3pt_reb_data['player_reb'] is True
        assert player_def_3pt_reb_data['three'] is True
        assert player_def_3pt_reb_data['ft'] is False
        assert player_def_3pt_reb_data['player_id'] == '12345'
        assert player_def_3pt_reb_data['team_id'] == '909'

        player_def_ft_reb_data = pbp.Events[5].get_rebound_data()
        assert player_def_ft_reb_data['def_reb'] is True
        assert player_def_ft_reb_data['player_reb'] is True
        assert player_def_ft_reb_data['three'] is False
        assert player_def_ft_reb_data['ft'] is True
        assert player_def_ft_reb_data['player_id'] == '12345'
        assert player_def_ft_reb_data['team_id'] == '909'

    def test_player_off_reb_get_rebound_data(self):
        player_off_2pt_reb_shot = {
            'cl': '10:26',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2,
        }
        player_off_2pt_reb = {
            'cl': '10:24',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        player_off_3pt_reb_shot = {
            'cl': '10:18',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': 'miss 3pt Shot',
            'locX': 200,
            'locY': 110,
        }
        player_off_3pt_reb = {
            'cl': '10:16',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }
        player_off_ft_reb_shot = {
            'cl': '10:15',
            'etype': 3,
            'mtype': 12,
            'tid': 909,
            'pid': 123,
            'de': 'Free Throw Missed 2 of 2',
            'locX': 0,
            'locY': 0,
        }
        player_off_ft_reb = {
            'cl': '10:14',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        pbp = DataPeriod(
            [
                player_off_2pt_reb_shot,
                player_off_2pt_reb,
                player_off_3pt_reb_shot,
                player_off_3pt_reb,
                player_off_ft_reb_shot,
                player_off_ft_reb
            ],
            self.GameId,
            self.Period
        )

        player_off_2pt_reb_data = pbp.Events[1].get_rebound_data()
        assert player_off_2pt_reb_data['def_reb'] is False
        assert player_off_2pt_reb_data['player_reb'] is True
        assert player_off_2pt_reb_data['three'] is False
        assert player_off_2pt_reb_data['ft'] is False
        assert player_off_2pt_reb_data['player_id'] == '12345'
        assert player_off_2pt_reb_data['team_id'] == '909'

        player_off_3pt_reb_data = pbp.Events[3].get_rebound_data()
        assert player_off_3pt_reb_data['def_reb'] is False
        assert player_off_3pt_reb_data['player_reb'] is True
        assert player_off_3pt_reb_data['three'] is True
        assert player_off_3pt_reb_data['ft'] is False
        assert player_off_3pt_reb_data['player_id'] == '12345'
        assert player_off_3pt_reb_data['team_id'] == '909'

        player_off_ft_reb_data = pbp.Events[5].get_rebound_data()
        assert player_off_ft_reb_data['def_reb'] is False
        assert player_off_ft_reb_data['player_reb'] is True
        assert player_off_ft_reb_data['three'] is False
        assert player_off_ft_reb_data['ft'] is True
        assert player_off_ft_reb_data['player_id'] == '12345'
        assert player_off_ft_reb_data['team_id'] == '909'

    def test_team_def_reb_get_rebound_data(self):
        team_def_2pt_reb_shot = {
            'cl': '10:26',
            'etype': 2,
            'mtype': 0,
            'tid': 111,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2,
        }
        team_def_2pt_reb = {
            'cl': '10:24',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        team_def_3pt_reb_shot = {
            'cl': '10:18',
            'etype': 2,
            'mtype': 0,
            'tid': 1111,
            'pid': 123,
            'de': 'miss 3pt Shot',
            'locX': 200,
            'locY': 110,
        }
        team_def_3pt_reb = {
            'cl': '10:16',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }
        team_def_ft_reb_shot = {
            'cl': '10:15',
            'etype': 3,
            'mtype': 12,
            'tid': 111,
            'pid': 123,
            'de': 'Free Throw Missed',
            'locX': 0,
            'locY': 0,
        }
        team_def_ft_reb = {
            'cl': '10:14',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        pbp = DataPeriod(
            [
                team_def_2pt_reb_shot,
                team_def_2pt_reb,
                team_def_3pt_reb_shot,
                team_def_3pt_reb,
                team_def_ft_reb_shot,
                team_def_ft_reb
            ],
            self.GameId,
            self.Period
        )

        team_def_2pt_reb_data = pbp.Events[1].get_rebound_data()
        assert team_def_2pt_reb_data['def_reb'] is True
        assert team_def_2pt_reb_data['player_reb'] is False
        assert team_def_2pt_reb_data['three'] is False
        assert team_def_2pt_reb_data['ft'] is False
        assert team_def_2pt_reb_data['player_id'] is None
        assert team_def_2pt_reb_data['team_id'] == '909'

        team_def_3pt_reb_data = pbp.Events[3].get_rebound_data()
        assert team_def_3pt_reb_data['def_reb'] is True
        assert team_def_3pt_reb_data['player_reb'] is False
        assert team_def_3pt_reb_data['three'] is True
        assert team_def_3pt_reb_data['ft'] is False
        assert team_def_3pt_reb_data['player_id'] is None
        assert team_def_3pt_reb_data['team_id'] == '909'

        team_def_ft_reb_data = pbp.Events[5].get_rebound_data()
        assert team_def_ft_reb_data['def_reb'] is True
        assert team_def_ft_reb_data['player_reb'] is False
        assert team_def_ft_reb_data['three'] is False
        assert team_def_ft_reb_data['ft'] is True
        assert team_def_ft_reb_data['player_id'] is None
        assert team_def_ft_reb_data['team_id'] == '909'

    def test_team_off_reb_get_rebound_data(self):
        team_off_2pt_reb_shot = {
            'cl': '10:26',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2,
        }
        team_off_2pt_reb = {
            'cl': '10:24',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        team_off_3pt_reb_shot = {
            'cl': '10:18',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': 'miss 3pt Shot',
            'locX': 200,
            'locY': 110,
        }
        team_off_3pt_reb = {
            'cl': '10:16',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }
        team_off_ft_reb_shot = {
            'cl': '10:15',
            'etype': 3,
            'mtype': 12,
            'tid': 909,
            'pid': 123,
            'de': 'Free Throw Missed',
            'locX': 0,
            'locY': 0,
        }
        team_off_ft_reb = {
            'cl': '10:14',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        pbp = DataPeriod(
            [
                team_off_2pt_reb_shot,
                team_off_2pt_reb,
                team_off_3pt_reb_shot,
                team_off_3pt_reb,
                team_off_ft_reb_shot,
                team_off_ft_reb
            ],
            self.GameId,
            self.Period
        )

        team_off_2pt_reb_data = pbp.Events[1].get_rebound_data()
        assert team_off_2pt_reb_data['def_reb'] is False
        assert team_off_2pt_reb_data['player_reb'] is False
        assert team_off_2pt_reb_data['three'] is False
        assert team_off_2pt_reb_data['ft'] is False
        assert team_off_2pt_reb_data['player_id'] is None
        assert team_off_2pt_reb_data['team_id'] == '909'

        team_off_3pt_reb_data = pbp.Events[3].get_rebound_data()
        assert team_off_3pt_reb_data['def_reb'] is False
        assert team_off_3pt_reb_data['player_reb'] is False
        assert team_off_3pt_reb_data['three'] is True
        assert team_off_3pt_reb_data['ft'] is False
        assert team_off_3pt_reb_data['player_id'] is None
        assert team_off_3pt_reb_data['team_id'] == '909'

        team_off_ft_reb_data = pbp.Events[5].get_rebound_data()
        assert team_off_ft_reb_data['def_reb'] is False
        assert team_off_ft_reb_data['player_reb'] is False
        assert team_off_ft_reb_data['three'] is False
        assert team_off_ft_reb_data['ft'] is True
        assert team_off_ft_reb_data['player_id'] is None
        assert team_off_ft_reb_data['team_id'] == '909'

    def test_non_rebs_get_rebound_data(self):
        airball_shot_clock_violation_shot = {
            'cl': '10:15',
            'etype': 2,
            'mtype': 0,
            'tid': 111,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2
        }
        shot_clock_violation = {
            'cl': '10:14',
            'etype': 5,
            'mtype': 11,
            'tid': 111,
            'pid': 0,
            'de': 'shot clock violation',
        }
        team_reb = {
            'cl': '10:14',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }
        end_of_period_shot = {
            'cl': '0:01',
            'etype': 2,
            'mtype': 0,
            'tid': 111,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2
        }
        end_of_period_reb = {
            'cl': '00:00.0',
            'pid': 0,
            'tid': 909,
            'etype': 4,
            'current_players': []
        }

        pbp = DataPeriod(
            [
                airball_shot_clock_violation_shot,
                shot_clock_violation,
                team_reb,
                end_of_period_shot,
                end_of_period_reb
            ],
            self.GameId,
            self.Period
        )
        shot_clock_team_reb = pbp.Events[2].get_rebound_data()
        assert shot_clock_team_reb is None

        end_of_period_team_reb = pbp.Events[4].get_rebound_data()
        assert end_of_period_team_reb is None

    def test_player_reb_at_time_of_shot_clock_violation_get_rebound_data(self):
        events = DataPeriod(
            [
                {'evt': 679, 'cl': '06:42', 'de': '[ATL] Len Driving Layup Shot: Missed', 'locX': 9, 'locY': 24, 'mtype': 6, 'etype': 2, 'opid': '', 'tid': 1610612737, 'pid': 203458, 'hs': 104, 'vs': 100, 'epid': '', 'oftid': 1610612737, 'ord': 669000},
                {'evt': 680, 'cl': '06:39', 'de': '[ATL] Prince Rebound (Off:2 Def:2)', 'locX': 9, 'locY': 24, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612737, 'pid': 1627752, 'hs': 104, 'vs': 100, 'epid': '', 'oftid': 1610612737, 'ord': 670000},
                {'evt': 681, 'cl': '06:39', 'de': '[ATL] Team Turnover : Shot Clock Turnover', 'locX': -220, 'locY': 72, 'mtype': 11, 'etype': 5, 'opid': '', 'tid': 1610612737, 'pid': 0, 'hs': 104, 'vs': 100, 'epid': '', 'oftid': 1610612737, 'ord': 671000}
            ],
            self.GameId,
            self.Period
        )
        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is not None
        assert reb_data['def_reb'] is False

    def test_team_reb_from_lb_foul_at_end_of_period_get_rebound_data(self):
        events = DataPeriod(
            [
                {'evt': 541, 'cl': '00:01.2', 'de': '[WAS] Brown Jr. Driving Floating Jump Shot: Missed', 'locX': -58, 'locY': 25, 'mtype': 101, 'etype': 2, 'opid': '', 'tid': 1610612764, 'pid': 1628972, 'hs': 77, 'vs': 101, 'epid': '', 'oftid': 1610612764, 'ord': 5342500},
                {'evt': 545, 'cl': '0:00', 'de': '[BKN] Team Rebound', 'locX': -58, 'locY': 25, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612751, 'pid': 0, 'hs': 77, 'vs': 101, 'epid': '', 'oftid': 1610612764, 'ord': 5343750},
                {'evt': 543, 'cl': '0:00', 'de': '[WAS] Bryant Foul: Loose Ball (2 PF) (2 FTA) (M Lindsay)', 'locX': 43, 'locY': 828, 'mtype': 3, 'etype': 6, 'opid': '1626178', 'tid': 1610612764, 'pid': 1628418, 'hs': 77, 'vs': 101, 'epid': '', 'oftid': 1610612751, 'ord': 5345000},
                {'evt': 546, 'cl': '0:00', 'de': '[BKN 78-101] Hollis-Jefferson Free Throw 1 of 2 (2 PTS)', 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612751, 'pid': 1626178, 'hs': 78, 'vs': 101, 'epid': '', 'oftid': 1610612751, 'ord': 5390000},
                {'evt': 548, 'cl': '0:00', 'de': '[BKN 79-101] Hollis-Jefferson Free Throw 2 of 2 (3 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612751, 'pid': 1626178, 'hs': 79, 'vs': 101, 'epid': '', 'oftid': 1610612751, 'ord': 5400000}
            ],
            self.GameId,
            self.Period
        )

        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is not None

    def test_team_reb_at_end_of_period_with_event_between_get_rebound_data(self):
        events = DataPeriod(
            [
                {'evt': 369, 'cl': '00:00.0', 'de': '[ATL] Bazemore 3pt Shot: Missed', 'locX': 9, 'locY': 575, 'mtype': 103, 'etype': 2, 'opid': '', 'tid': 1610612737, 'pid': 203145, 'hs': 65, 'vs': 69, 'epid': '', 'oftid': 1610612737},
                {'evt': 370, 'cl': '00:00.0', 'de': '[ATL] Team Rebound', 'locX': 9, 'locY': 575, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612737, 'pid': 0, 'hs': 65, 'vs': 69, 'epid': '', 'oftid': 1610612737},
                {'evt': 372, 'cl': '00:00.0', 'de': 'Instant Replay - Support Ruling', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 18, 'opid': '', 'tid': 0, 'pid': 0, 'hs': 65, 'vs': 69, 'epid': '', 'oftid': 1610612737},
                {'evt': 371, 'cl': '00:00.0', 'de': 'End Period', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 13, 'opid': '', 'tid': 0, 'pid': 0, 'hs': 65, 'vs': 69, 'epid': '', 'oftid': 1610612737}
            ],
            self.GameId,
            self.Period
        )

        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is None

    def test_rebound_at_same_time_as_buzzer_beater_get_rebound_data(self):
        events = DataPeriod(
            [
                {'evt': 749, 'cl': '00:01.0', 'de': '[WAS] Porter Jr. 3pt Shot: Missed', 'locX': 139, 'locY': 245, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612764, 'pid': 203490, 'hs': 113, 'vs': 117, 'epid': '', 'oftid': 1610612764},
                {'evt': 750, 'cl': '00:01.0', 'de': '[WAS] Team Rebound', 'locX': 139, 'locY': 245, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612764, 'pid': 0, 'hs': 113, 'vs': 117, 'epid': '', 'oftid': 1610612764},
                {'evt': 751, 'cl': '00:00.0', 'de': 'End Period', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 13, 'opid': '', 'tid': 0, 'pid': 0, 'hs': 113, 'vs': 117, 'epid': '', 'oftid': 1610612764}
            ],
            self.GameId,
            self.Period
        )

        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is None

    def test_rebound_on_missed_ft_1_of_2_get_rebound_data(self):
        events = DataPeriod(
            [
                {'evt': 155, 'cl': '02:38', 'de': '[TOR] Miles Free Throw 1 of 2 Missed', 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612761, 'pid': 101139, 'hs': 18, 'vs': 21, 'epid': '', 'oftid': 1610612761},
                {'evt': 156, 'cl': '02:38', 'de': '[TOR] Team Rebound', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 4, 'opid': '', 'tid': 1610612761, 'pid': 0, 'hs': 18, 'vs': 21, 'epid': '', 'oftid': 1610612761},
                {'evt': 157, 'cl': '02:38', 'de': '[TOR 22-18] Miles Free Throw 2 of 2 (1 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612761, 'pid': 101139, 'hs': 18, 'vs': 22, 'epid': '', 'oftid': 1610612761}
            ],
            self.GameId,
            self.Period
        )

        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is None

    def test_start_of_period_is_start_of_period(self):
        event = DataPbpEvent({'etype': 12, 'mtype': 0})
        assert event.is_start_of_period() is True

    def test_end_of_period_is_start_of_period(self):
        event = DataPbpEvent({'etype': 13, 'mtype': 0})
        assert event.is_start_of_period() is False

    def test_end_of_period_is_end_of_period(self):
        event = DataPbpEvent({'etype': 13, 'mtype': 0})
        assert event.is_end_of_period() is True

    def test_start_of_period_is_end_of_period(self):
        event = DataPbpEvent({'etype': 12, 'mtype': 0})
        assert event.is_end_of_period() is False

    def test_delay_of_game_is_delay_of_game(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 18})
        assert event.is_delay_of_game() is True

    def test_non_delay_of_game_is_delay_of_game(self):
        event = DataPbpEvent({'etype': 6, 'mtype': 8})
        assert event.is_delay_of_game() is False

    def test_1_of_1_is_ft_1_of_1(self):
        event = DataPbpEvent({'etype': 3, 'mtype': 10})
        assert event.is_ft_1_of_1() is True

    def test_1_of_2_is_ft_1_of_1(self):
        event = DataPbpEvent({'etype': 3, 'mtype': 11})
        assert event.is_ft_1_of_1() is False

    def test_2_of_2_is_ft_2_of_2(self):
        event = DataPbpEvent({'etype': 3, 'mtype': 12})
        assert event.is_ft_2_of_2() is True

    def test_1_of_2_is_ft_2_of_2(self):
        event = DataPbpEvent({'etype': 3, 'mtype': 11})
        assert event.is_ft_2_of_2() is False

    def test_3_of_3_is_ft_3_of_3(self):
        event = DataPbpEvent({'etype': 3, 'mtype': 15})
        assert event.is_ft_3_of_3() is True

    def test_1_of_3_is_ft_3_of_3(self):
        event = DataPbpEvent({'etype': 3, 'mtype': 13})
        assert event.is_ft_3_of_3() is False

    def test_jump_ball_is_jump_ball(self):
        event = DataPbpEvent({'etype': 10, 'mtype': 15})
        assert event.is_jump_ball() is True

    def test_non_jump_ball_is_jump_ball(self):
        event = DataPbpEvent({'etype': 13, 'mtype': 11})
        assert event.is_jump_ball() is False

    def test_away_from_play_is_away_from_play_ft(self):
        events = DataPeriod(
            [
                {'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1, 'pid': 1},
                {'etype': 6, 'mtype': 6, 'de': 'Away From Play Foul', 'cl': '0:45', 'tid': 2, 'pid': 2},
                {'etype': 1, 'mtype': 10, 'de': 'Made Shot by team that got fouled', 'cl': '0:35', 'tid': 2, 'pid': 2},
            ],
            self.GameId,
            self.Period
        )

        assert events.Events[0].is_away_from_play_ft() is True

    def test_foul_on_made_shot_by_team_that_got_fouled_is_away_from_play_ft(self):
        events = DataPeriod(
            [
                DataPbpEvent({'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1, 'pid': 1}),
                DataPbpEvent({'etype': 6, 'mtype': 6, 'de': 'Away From Play Foul', 'cl': '0:45', 'tid': 2, 'pid': 3}),
                DataPbpEvent({'etype': 1, 'mtype': 10, 'de': 'Made Shot by team that got fouled', 'cl': '0:45', 'tid': 1, 'pid': 2}),
            ],
            self.GameId,
            self.Period
        )

        assert events.Events[0].is_away_from_play_ft() is False

    def test_foul_on_made_shot_by_team_that_didnt_get_fouled_is_away_from_play_ft(self):
        events = DataPeriod(
            [
                DataPbpEvent({'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1, 'pid': 1}),
                DataPbpEvent({'etype': 6, 'mtype': 6, 'de': 'Away From Play Foul', 'cl': '0:45', 'tid': 2, 'pid': 2}),
                DataPbpEvent({'etype': 1, 'mtype': 10, 'de': 'Made Shot by team that got didnt get fouled', 'cl': '0:45', 'tid': 2, 'pid': 3}),
            ],
            self.GameId,
            self.Period
        )

        assert events.Events[0].is_away_from_play_ft() is True

    def test_foul_on_made_ft_by_team_that_got_fouled_is_away_from_play_ft(self):
        events = DataPeriod(
            [
                {'evt': 499, 'cl': '04:51', 'de': '[TOR 94-68] Lowry 3pt Shot: Made (15 PTS)', 'locX': 159, 'locY': 224, 'mtype': 79, 'etype': 1, 'opid': '', 'tid': 1610612761, 'pid': 200768, 'hs': 94, 'vs': 68, 'epid': '', 'oftid': 1610612761, 'ord': 490000},
                {'evt': 500, 'cl': '04:32', 'de': '[TOR] Leonard Foul: Shooting (3 PF) (2 FTA) (S Foster)', 'locX': -39, 'locY': 59, 'mtype': 2, 'etype': 6, 'opid': '203954', 'tid': 1610612761, 'pid': 202695, 'hs': 94, 'vs': 68, 'epid': '', 'oftid': 1610612755, 'ord': 491000},
                {'evt': 502, 'cl': '04:32', 'de': '[PHI 69-94] Embiid Free Throw 1 of 2 (19 PTS)', 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612755, 'pid': 203954, 'hs': 94, 'vs': 69, 'epid': '', 'oftid': 1610612755, 'ord': 493000},
                {'evt': 503, 'cl': '04:32', 'de': '[PHI] Simmons Substitution replaced by Fultz', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612755, 'pid': 1627732, 'hs': 94, 'vs': 69, 'epid': '1628365', 'oftid': 1610612755, 'ord': 494000},
                {'evt': 505, 'cl': '04:32', 'de': '[PHI 70-94] Embiid Free Throw 2 of 2 (20 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612755, 'pid': 203954, 'hs': 94, 'vs': 70, 'epid': '', 'oftid': 1610612755, 'ord': 496000},
                {'evt': 506, 'cl': '04:32', 'de': '[TOR] Siakam Foul: Away From Play (2 PF) (1 FTA) (T Ford)', 'locX': 51, 'locY': 26, 'mtype': 6, 'etype': 6, 'opid': '203488', 'tid': 1610612761, 'pid': 1627783, 'hs': 94, 'vs': 70, 'epid': '', 'oftid': 1610612755, 'ord': 497000},
                {'evt': 511, 'cl': '04:32', 'de': '[PHI 71-94] Muscala Free Throw 1 of 1 (10 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612755, 'pid': 203488, 'hs': 94, 'vs': 71, 'epid': '', 'oftid': 1610612755, 'ord': 499000},
                {'evt': 509, 'cl': '04:32', 'de': '[PHI] Embiid Substitution replaced by Johnson', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612755, 'pid': 203954, 'hs': 94, 'vs': 71, 'epid': '101161', 'oftid': 1610612761, 'ord': 500000},
                {'evt': 512, 'cl': '04:17', 'de': '[TOR] Siakam Turnaround Fadeaway shot: Missed', 'locX': -18, 'locY': 20, 'mtype': 86, 'etype': 2, 'opid': '', 'tid': 1610612761, 'pid': 1627783, 'hs': 94, 'vs': 71, 'epid': '', 'oftid': 1610612761, 'ord': 503000},
                {'evt': 513, 'cl': '04:15', 'de': '[PHI] Muscala Rebound (Off:2 Def:3)', 'locX': -18, 'locY': 20, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612755, 'pid': 203488, 'hs': 94, 'vs': 71, 'epid': '', 'oftid': 1610612761, 'ord': 504000},
                {'evt': 514, 'cl': '04:04', 'de': '[PHI 73-94] Fultz Pullup Jump shot: Made (5 PTS)', 'locX': 8, 'locY': 155, 'mtype': 79, 'etype': 1, 'opid': '', 'tid': 1610612755, 'pid': 1628365, 'hs': 94, 'vs': 73, 'epid': '', 'oftid': 1610612755, 'ord': 505000}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_away_from_play_ft() is False
        assert events.Events[4].is_away_from_play_ft() is False
        assert events.Events[6].is_away_from_play_ft() is False

    def test_foul_on_made_ft_by_team_that_didnt_get_fouled_is_away_from_play_ft(self):
        events = DataPeriod(
            [
                {'evt': 607, 'cl': '00:24.9', 'de': '[DET 121-111] Jackson Free Throw 2 of 2 (16 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612765, 'pid': 202704, 'hs': 121, 'vs': 111, 'epid': '', 'oftid': 1610612765, 'ord': 6050000},
                {'evt': 608, 'cl': '00:24.9', 'de': '[WAS] Team Timeout : Regular', 'locX': 0, 'locY': -80, 'mtype': 1, 'etype': 9, 'opid': '', 'tid': 1610612764, 'pid': 1610612764, 'hs': 121, 'vs': 111, 'epid': '', 'oftid': 1610612764, 'ord': 6060000},
                {'evt': 609, 'cl': '00:24.9', 'de': '[DET] Griffin Foul: Away From Play (5 PF) (1 FTA) (M Davis)', 'locX': -109, 'locY': 100, 'mtype': 6, 'etype': 6, 'opid': '201145', 'tid': 1610612765, 'pid': 201933, 'hs': 121, 'vs': 111, 'epid': '', 'oftid': 1610612764, 'ord': 6070000},
                {'evt': 611, 'cl': '00:24.9', 'de': '[WAS 112-121] Beal Free Throw 1 of 1 (32 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612764, 'pid': 203078, 'hs': 121, 'vs': 112, 'epid': '', 'oftid': 1610612764, 'ord': 6090000},
                {'evt': 612, 'cl': '00:23.5', 'de': '[WAS] Green 3pt Shot: Missed', 'locX': -221, 'locY': 157, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612764, 'pid': 201145, 'hs': 121, 'vs': 112, 'epid': '', 'oftid': 1610612764, 'ord': 6100000}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].is_away_from_play_ft() is True

    def test_away_from_play_is_inbound_foul_ft(self):
        events = DataPeriod([
            DataPbpEvent({'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1}),
            DataPbpEvent({'etype': 6, 'mtype': 6, 'de': 'Away From Play Foul', 'cl': '0:45', 'tid': 2}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_inbound_foul_ft() is False

    def test_inbound_foul_is_inbound_foul_ft(self):
        events = DataPeriod([
            DataPbpEvent({'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1}),
            DataPbpEvent({'etype': 6, 'mtype': 5, 'de': 'Inbound Foul', 'cl': '0:45', 'tid': 2}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_inbound_foul_ft() is True

    def test_lane_violation_turnover_is_lane_violation_turnover(self):
        event = DataPbpEvent({'etype': 5, 'mtype': 17})
        assert event.is_lane_violation_turnover() is True

    def test_lane_violation_is_lane_violation_turnover(self):
        event = DataPbpEvent({'etype': 7, 'mtype': 3})
        assert event.is_lane_violation_turnover() is False

    def test_lane_violation_turnover_is_lane_violation(self):
        event = DataPbpEvent({'etype': 5, 'mtype': 17})
        assert event.is_lane_violation() is False

    def test_lane_violation_is_lane_violation(self):
        event = DataPbpEvent({'etype': 7, 'mtype': 3})
        assert event.is_lane_violation() is True

    def test_double_lane_violation_is_double_lane_violation(self):
        event = DataPbpEvent({'etype': 7, 'mtype': 6})
        assert event.is_double_lane_violation() is True

    def test_lane_violation_is_double_lane_violation(self):
        event = DataPbpEvent({'etype': 7, 'mtype': 3})
        assert event.is_double_lane_violation() is False

    def test_jump_ball_violation_is_jumpball_violation(self):
        event = DataPbpEvent({'etype': 7, 'mtype': 4})
        assert event.is_jumpball_violation() is True

    def test_lane_violation_is_jumpball_violation(self):
        event = DataPbpEvent({'etype': 7, 'mtype': 3})
        assert event.is_jumpball_violation() is False

    def test_tech_at_time_of_make_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'etype': 1, 'mtype': 10, 'de': 'Made Shot', 'cl': '0:45', 'tid': 1}),
            DataPbpEvent({'etype': 6, 'mtype': 11, 'de': 'Technical Foul', 'cl': '0:45', 'tid': 1}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is False

    def test_and1_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'etype': 1, 'mtype': 10, 'tid': 1, 'de': 'Made Shot', 'cl': '0:45'}),
            DataPbpEvent({'etype': 6, 'mtype': 2, 'de': 'Shooting Foul', 'cl': '0:45', 'tid': 2}),
            DataPbpEvent({'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is True

    def test_and1_with_foul_out_of_order_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'etype': 1, 'mtype': 10, 'tid': 1, 'de': 'Made Shot', 'cl': '0:45'}),
            DataPbpEvent({'etype': 3, 'mtype': 10, 'de': 'Free Throw 1 of 1', 'cl': '0:45', 'tid': 1}),
            DataPbpEvent({'etype': 6, 'mtype': 2, 'de': 'Shooting Foul', 'cl': '0:45', 'tid': 2}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is True

    def test_flagrant_and1_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'evt': 68, 'cl': '06:51', 'de': '[LAL] James Violation:Defensive Goaltending (J Tiven)', 'locX': 0, 'locY': -80, 'mtype': 2, 'etype': 7, 'opid': '', 'tid': 1610612747, 'pid': 2544, 'hs': 11, 'vs': 10, 'epid': '', 'oftid': 1610612759}),
            DataPbpEvent({'evt': 69, 'cl': '06:34', 'de': '[LAL 13-10] Ingram Turnaround Jump Shot: Made (4 PTS)', 'locX': 97, 'locY': 82, 'mtype': 47, 'etype': 1, 'opid': '', 'tid': 1610612747, 'pid': 1627742, 'hs': 13, 'vs': 10, 'epid': '', 'oftid': 1610612747}),
            DataPbpEvent({'evt': 70, 'cl': '06:34', 'de': '[SAS] Aldridge Foul: Flagrant Type 1 (2 PF) (1 FTA) (J Tiven)', 'locX': 87, 'locY': 72, 'mtype': 14, 'etype': 6, 'opid': '1627742', 'tid': 1610612759, 'pid': 200746, 'hs': 13, 'vs': 10, 'epid': '', 'oftid': 1610612747}),
            DataPbpEvent({'evt': 72, 'cl': '06:34', 'de': 'Instant Replay - Support Ruling', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 18, 'opid': '', 'tid': 0, 'pid': 0, 'hs': 13, 'vs': 10, 'epid': '', 'oftid': 1610612747}),
            DataPbpEvent({'evt': 73, 'cl': '06:34', 'de': '[LAL 14-10] Ingram Free Throw Flagrant 1 of 1 (5 PTS)', 'locX': 0, 'locY': -80, 'mtype': 20, 'etype': 3, 'opid': '', 'tid': 1610612747, 'pid': 1627742, 'hs': 14, 'vs': 10, 'epid': '', 'oftid': 1610612747}),
            DataPbpEvent({'evt': 74, 'cl': '06:34', 'de': '[LAL] Ingram Substitution replaced by Hart', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612747, 'pid': 1627742, 'hs': 14, 'vs': 10, 'epid': '1628404', 'oftid': 1610612759}),
            DataPbpEvent({'evt': 75, 'cl': '06:34', 'de': '[SAS] Aldridge Substitution replaced by Poeltl', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612759, 'pid': 200746, 'hs': 14, 'vs': 10, 'epid': '1627751', 'oftid': 1610612759}),
            DataPbpEvent({'evt': 78, 'cl': '06:24', 'de': '[LAL] Kuzma Jump Shot: Missed', 'locX': -19, 'locY': 51, 'mtype': 1, 'etype': 2, 'opid': '', 'tid': 1610612747, 'pid': 1628398, 'hs': 14, 'vs': 10, 'epid': '', 'oftid': 1610612747})
        ], self.GameId, self.Period)

        assert events.Events[1].is_and1_shot() is True

    def test_and1_on_missed_ft_tip_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'evt': 512, 'cl': '01:20', 'de': '[UTA] Favors Foul: Shooting (4 PF) (2 FTA) (M Ervin)', 'locX': -20, 'locY': 9, 'mtype': 2, 'etype': 6, 'opid': '203524', 'tid': 1610612762, 'pid': 202324, 'hs': 74, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 514, 'cl': '01:20', 'de': '[NOP 75-99] S Hill Free Throw 1 of 2 (6 PTS)', 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612740, 'pid': 203524, 'hs': 75, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 515, 'cl': '01:20', 'de': '[NOP] Mirotic Substitution replaced by Frazier', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612740, 'pid': 202703, 'hs': 75, 'vs': 99, 'epid': '204025', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 517, 'cl': '01:20', 'de': '[NOP] S Hill Free Throw 2 of 2 Missed', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612740, 'pid': 203524, 'hs': 75, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 518, 'cl': '01:20', 'de': '[NOP] Okafor Rebound (Off:1 Def:3)', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612740, 'pid': 1626143, 'hs': 75, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 519, 'cl': '01:20', 'de': '[NOP 77-99] Okafor Tip Layup Shot: Made (8 PTS)', 'locX': 0, 'locY': -5, 'mtype': 97, 'etype': 1, 'opid': '', 'tid': 1610612740, 'pid': 1626143, 'hs': 77, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 520, 'cl': '01:20', 'de': '[UTA] Crowder Foul: Shooting (3 PF) (1 FTA) (K Fitzgerald)', 'locX': 0, 'locY': -5, 'mtype': 2, 'etype': 6, 'opid': '1626143', 'tid': 1610612762, 'pid': 203109, 'hs': 77, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 522, 'cl': '01:20', 'de': '[NOP 78-99] Okafor Free Throw 1 of 1 (9 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612740, 'pid': 1626143, 'hs': 78, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 523, 'cl': '01:11', 'de': '[UTA 101-78] Burks Cutting Layup Shot: Made (5 PTS) Assist: Exum (1 AST)', 'locX': 7, 'locY': -1, 'mtype': 98, 'etype': 1, 'opid': '', 'tid': 1610612762, 'pid': 202692, 'hs': 78, 'vs': 101, 'epid': '203957', 'oftid': 1610612762})
        ], self.GameId, self.Period)

        assert events.Events[5].is_and1_shot() is True

    def test_and1_on_missed_and1_ft_tip_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'evt': 602, 'cl': '07:25', 'de': '[LAC 92-97] Williams Driving Layup Shot: Made (16 PTS)', 'locX': -5, 'locY': 9, 'mtype': 6, 'etype': 1, 'opid': '', 'tid': 1610612746, 'pid': 101150, 'hs': 92, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 603, 'cl': '07:25', 'de': '[LAL] McGee Foul: Shooting (3 PF) (1 FTA) (J Goble)', 'locX': -11, 'locY': 6, 'mtype': 2, 'etype': 6, 'opid': '101150', 'tid': 1610612747, 'pid': 201580, 'hs': 92, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 605, 'cl': '07:25', 'de': '[LAC] Williams Free Throw 1 of 1 Missed', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612746, 'pid': 101150, 'hs': 92, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 606, 'cl': '07:25', 'de': '[LAC] Marjanovic Rebound (Off:1 Def:0)', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612746, 'pid': 1626246, 'hs': 92, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 607, 'cl': '07:25', 'de': '[LAC 94-97] Marjanovic Putback Layup Shot: Made (2 PTS)', 'locX': 6, 'locY': 3, 'mtype': 72, 'etype': 1, 'opid': '', 'tid': 1610612746, 'pid': 1626246, 'hs': 94, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 613, 'cl': '07:25', 'de': '[LAL] McGee Violation:Defensive Goaltending', 'locX': 0, 'locY': -80, 'mtype': 2, 'etype': 7, 'opid': '', 'tid': 1610612747, 'pid': 201580, 'hs': 94, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 608, 'cl': '07:25', 'de': '[LAL] Ingram Foul: Shooting (4 PF) (1 FTA) (B Barnaky)', 'locX': 0, 'locY': 0, 'mtype': 2, 'etype': 6, 'opid': '1626246', 'tid': 1610612747, 'pid': 1627742, 'hs': 94, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 610, 'cl': '07:25', 'de': '[LAL] McGee Substitution replaced by Chandler', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612747, 'pid': 201580, 'hs': 94, 'vs': 97, 'epid': '2199', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 612, 'cl': '07:25', 'de': '[LAC 95-97] Marjanovic Free Throw 1 of 1 (3 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612746, 'pid': 1626246, 'hs': 95, 'vs': 97, 'epid': '', 'oftid': 1610612746}),
            DataPbpEvent({'evt': 614, 'cl': '07:05', 'de': '[LAL] Kuzma Fadeaway Jump Shot: Missed', 'locX': -40, 'locY': 57, 'mtype': 63, 'etype': 2, 'opid': '', 'tid': 1610612747, 'pid': 1628398, 'hs': 95, 'vs': 97, 'epid': '', 'oftid': 1610612747})
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is True
        assert events.Events[4].is_and1_shot() is True

    def test_and1_where_team_commits_foul_on_missed_ft_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'evt': 383, 'cl': '07:37', 'de': '[MIL 77-47] Bledsoe Driving Layup Shot: Made (4 PTS) Assist: Antetokounmpo (6 AST)', 'locX': -7, 'locY': 20, 'mtype': 6, 'etype': 1, 'opid': '', 'tid': 1610612749, 'pid': 202339, 'hs': 47, 'vs': 77, 'epid': '203507', 'oftid': 1610612749}),
            DataPbpEvent({'evt': 385, 'cl': '07:37', 'de': '[MIN] Teague Foul: Shooting (1 PF) (1 FTA) (B Adair)', 'locX': -7, 'locY': 20, 'mtype': 2, 'etype': 6, 'opid': '202339', 'tid': 1610612750, 'pid': 201952, 'hs': 47, 'vs': 77, 'epid': '', 'oftid': 1610612749}),
            DataPbpEvent({'evt': 387, 'cl': '07:37', 'de': '[MIL] Brogdon Substitution replaced by Ilyasova', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612749, 'pid': 1627763, 'hs': 47, 'vs': 77, 'epid': '101141', 'oftid': 1610612749}),
            DataPbpEvent({'evt': 389, 'cl': '07:37', 'de': '[MIL] Bledsoe Free Throw 1 of 1 Missed', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612749, 'pid': 202339, 'hs': 47, 'vs': 77, 'epid': '', 'oftid': 1610612749}),
            DataPbpEvent({'evt': 390, 'cl': '07:37', 'de': '[MIN] Team Rebound', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612750, 'pid': 0, 'hs': 47, 'vs': 77, 'epid': '', 'oftid': 1610612749}),
            DataPbpEvent({'evt': 391, 'cl': '07:37', 'de': '[MIL] Bledsoe Foul: Loose Ball (2 PF) (1 FTA) (E Lewis)', 'locX': -111, 'locY': 823, 'mtype': 3, 'etype': 6, 'opid': '201959', 'tid': 1610612749, 'pid': 202339, 'hs': 47, 'vs': 77, 'epid': '', 'oftid': 1610612750}),
            DataPbpEvent({'evt': 393, 'cl': '07:24', 'de': '[MIN 50-77] Towns 3pt Shot: Made (14 PTS) Assist: Teague (4 AST)', 'locX': 3, 'locY': 257, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612750, 'pid': 1626157, 'hs': 50, 'vs': 77, 'epid': '201952', 'oftid': 1610612750})
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is True

    def test_and1_with_lane_violation_is_and1_shot(self):
        events = DataPeriod([
            DataPbpEvent({'evt': 518, 'cl': '01:20', 'de': '[NOP] Okafor Rebound (Off:1 Def:3)', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612740, 'pid': 1626143, 'hs': 75, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 519, 'cl': '01:20', 'de': '[NOP 77-99] Okafor Tip Layup Shot: Made (8 PTS)', 'locX': 0, 'locY': -5, 'mtype': 97, 'etype': 1, 'opid': '', 'tid': 1610612740, 'pid': 1626143, 'hs': 77, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 520, 'cl': '01:20', 'de': '[UTA] Crowder Foul: Shooting (3 PF) (1 FTA) (K Fitzgerald)', 'locX': 0, 'locY': -5, 'mtype': 2, 'etype': 6, 'opid': '1626143', 'tid': 1610612762, 'pid': 203109, 'hs': 77, 'vs': 99, 'epid': '', 'oftid': 1610612740}),
            DataPbpEvent({'evt': 522, 'cl': '01:20', 'de': '[NOP] Okafor Turnover : Lane Violation (1 TO)', 'locX': 0, 'locY': -80, 'mtype': 17, 'etype': 5, 'opid': '', 'tid': 1610612740, 'pid': 1626143, 'hs': 23, 'vs': 21, 'epid': '', 'oftid': 1610612755}),
            DataPbpEvent({'evt': 523, 'cl': '01:11', 'de': '[UTA 101-78] Burks Cutting Layup Shot: Made (5 PTS) Assist: Exum (1 AST)', 'locX': 7, 'locY': -1, 'mtype': 98, 'etype': 1, 'opid': '', 'tid': 1610612762, 'pid': 202692, 'hs': 78, 'vs': 101, 'epid': '203957', 'oftid': 1610612762})
        ], self.GameId, self.Period)

        assert events.Events[1].is_and1_shot() is True

    def test_oreb_is_second_chance_event(self):
        first_shot = {
            'evt': 1,
            'cl': '10:26',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2,
            'current_players': [],
        }
        first_oreb = {
            'evt': 2,
            'cl': '10:25',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'mtype': 0,
            'current_players': [],
        }
        second_shot = {
            'evt': 3,
            'cl': '10:16',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': '',
            'locX': -17,
            'locY': 12,
            'current_players': [],
        }
        second_oreb = {
            'evt': 4,
            'cl': '10:15',
            'pid': 12345,
            'tid': 909,
            'etype': 4,
            'mtype': 0,
            'current_players': [],
        }
        third_shot = {
            'evt': 5,
            'cl': '10:14',
            'etype': 2,
            'mtype': 1,
            'tid': 909,
            'pid': 123,
            'de': '',
            'locX': -17,
            'locY': 12,
            'current_players': [],
        }

        pbp = DataPeriod(
            [
                first_shot,
                first_oreb,
                second_shot,
                second_oreb,
                third_shot
            ],
            self.GameId,
            self.Period
        )

        assert pbp.Events[4].is_second_chance_event(pbp.Events) is True
        assert pbp.Events[2].is_second_chance_event(pbp.Events) is True
        assert pbp.Events[0].is_second_chance_event(pbp.Events) is False

    def test_dreb_is_second_chance_event(self):
        shot = {
            'evt': 1,
            'cl': '10:26',
            'etype': 2,
            'mtype': 0,
            'tid': 909,
            'pid': 123,
            'de': '',
            'locX': -7,
            'locY': 2,
            'current_players': [],
        }
        dreb = {
            'evt': 2,
            'cl': '10:25',
            'pid': 12345,
            'tid': 908,
            'etype': 4,
            'mtype': 0,
            'current_players': [],
        }
        pbp = DataPeriod([shot, dreb], self.GameId, self.Period)

        assert pbp.Events[0].is_second_chance_event(pbp.Events) is False

    def test_get_all_events_at_event_time(self):
        events = DataPeriod(
            [
                {'evt': 499, 'cl': '04:51', 'de': '[TOR 94-68] Lowry 3pt Shot: Made (15 PTS)', 'locX': 159, 'locY': 224, 'mtype': 79, 'etype': 1, 'opid': '', 'tid': 1610612761, 'pid': 200768, 'hs': 94, 'vs': 68, 'epid': '', 'oftid': 1610612761},
                {'evt': 500, 'cl': '04:32', 'de': '[TOR] Leonard Foul: Shooting (3 PF) (2 FTA) (S Foster)', 'locX': -39, 'locY': 59, 'mtype': 2, 'etype': 6, 'opid': '203954', 'tid': 1610612761, 'pid': 202695, 'hs': 94, 'vs': 68, 'epid': '', 'oftid': 1610612755},
                {'evt': 502, 'cl': '04:32', 'de': '[PHI 69-94] Embiid Free Throw 1 of 2 (19 PTS)', 'locX': 0, 'locY': -80, 'mtype': 11, 'etype': 3, 'opid': '', 'tid': 1610612755, 'pid': 203954, 'hs': 94, 'vs': 69, 'epid': '', 'oftid': 1610612755},
                {'evt': 503, 'cl': '04:32', 'de': '[PHI] Simmons Substitution replaced by Fultz', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612755, 'pid': 1627732, 'hs': 94, 'vs': 69, 'epid': '1628365', 'oftid': 1610612755},
                {'evt': 505, 'cl': '04:32', 'de': '[PHI 70-94] Embiid Free Throw 2 of 2 (20 PTS)', 'locX': 0, 'locY': -80, 'mtype': 12, 'etype': 3, 'opid': '', 'tid': 1610612755, 'pid': 203954, 'hs': 94, 'vs': 70, 'epid': '', 'oftid': 1610612755},
                {'evt': 506, 'cl': '04:32', 'de': '[TOR] Siakam Foul: Away From Play (2 PF) (1 FTA) (T Ford)', 'locX': 51, 'locY': 26, 'mtype': 6, 'etype': 6, 'opid': '203488', 'tid': 1610612761, 'pid': 1627783, 'hs': 94, 'vs': 70, 'epid': '', 'oftid': 1610612755},
                {'evt': 511, 'cl': '04:32', 'de': '[PHI 71-94] Muscala Free Throw 1 of 1 (10 PTS)', 'locX': 0, 'locY': -80, 'mtype': 10, 'etype': 3, 'opid': '', 'tid': 1610612755, 'pid': 203488, 'hs': 94, 'vs': 71, 'epid': '', 'oftid': 1610612755},
                {'evt': 509, 'cl': '04:32', 'de': '[PHI] Embiid Substitution replaced by Johnson', 'locX': 0, 'locY': -80, 'mtype': 0, 'etype': 8, 'opid': '', 'tid': 1610612755, 'pid': 203954, 'hs': 94, 'vs': 71, 'epid': '101161', 'oftid': 1610612761},
                {'evt': 512, 'cl': '04:17', 'de': '[TOR] Siakam Turnaround Fadeaway shot: Missed', 'locX': -18, 'locY': 20, 'mtype': 86, 'etype': 2, 'opid': '', 'tid': 1610612761, 'pid': 1627783, 'hs': 94, 'vs': 71, 'epid': '', 'oftid': 1610612761},
                {'evt': 513, 'cl': '04:15', 'de': '[PHI] Muscala Rebound (Off:2 Def:3)', 'locX': -18, 'locY': 20, 'mtype': 0, 'etype': 4, 'opid': '', 'tid': 1610612755, 'pid': 203488, 'hs': 94, 'vs': 71, 'epid': '', 'oftid': 1610612761},
                {'evt': 514, 'cl': '04:04', 'de': '[PHI 73-94] Fultz Pullup Jump shot: Made (5 PTS)', 'locX': 8, 'locY': 155, 'mtype': 79, 'etype': 1, 'opid': '', 'tid': 1610612755, 'pid': 1628365, 'hs': 94, 'vs': 73, 'epid': '', 'oftid': 1610612755}
            ],
            self.GameId,
            self.Period
        )
        filtered_events = events.Events[4].get_all_events_at_event_time()
        assert len(filtered_events) == 7
        assert filtered_events[0].number == 500
        assert filtered_events[-1].number == 509

        assert len(events.Events[0].get_all_events_at_event_time()) == 1
