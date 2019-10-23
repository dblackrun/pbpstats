import pbpstats
from pbpstats.stats_pbp_event import StatsPbpEvent
from pbpstats.stats_period import StatsPeriod


class TestStatsPbpEvent:
    GameId = '0021600270'
    Period = 1

    def test_made_fg_is_made_fg(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_made_fg() is True

    def test_missed_fg_is_made_fg(self):
        event = StatsPbpEvent({'EVENTNUM': 14, 'PCTIMESTRING': '10:34', 'VISITORDESCRIPTION': "MISS Bogdanovic 2' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_made_fg() is False

    def test_missed_fg_is_missed_fg(self):
        event = StatsPbpEvent({'EVENTNUM': 14, 'PCTIMESTRING': '10:34', 'VISITORDESCRIPTION': "MISS Bogdanovic 2' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_missed_fg() is True

    def test_made_fg_is_missed_fg(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_missed_fg() is False

    def test_assisted_shot_is_assisted_shot(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_assisted_shot() is True

    def test_unassisted_shot_is_assisted_shot(self):
        event = StatsPbpEvent({'EVENTNUM': 21, 'PCTIMESTRING': '09:31', 'VISITORDESCRIPTION': "Bogdanovic 2' Driving Layup (2 PTS)", 'EVENTMSGACTIONTYPE': 42, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_assisted_shot() is False

    def test_3pt_shot_is_3pt_shot(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_3pt_shot() is True

    def test_layup_is_3pt_shot(self):
        event = StatsPbpEvent({'EVENTNUM': 14, 'PCTIMESTRING': '10:34', 'VISITORDESCRIPTION': "MISS Bogdanovic 2' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_3pt_shot() is False

    def test_corner3_is_corner_3(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = -230
        event.loc_y = 28
        assert event.is_corner_3() is True

    def test_non_corner3_is_corner_3(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = -230
        event.loc_y = 100
        assert event.is_corner_3() is False

    def test_non_shot_event_with_corner3_coordinates_is_corner_3(self):
        event = StatsPbpEvent({'EVENTNUM': 87, 'PCTIMESTRING': '03:17', 'HOMEDESCRIPTION': 'Thomas Rebound (Off:0 Def:1)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 202498, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = -230
        event.loc_y = 28
        assert event.is_corner_3() is False

    def test_missing_coordinates_is_corner_3(self):
        event = StatsPbpEvent({'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = None
        event.loc_y = None
        assert event.is_corner_3() is False

    def test_10ft_shot_get_shot_distance(self):
        event = StatsPbpEvent({'EVENTNUM': 115, 'PCTIMESTRING': '0:45.9', 'HOMEDESCRIPTION': "MISS Anthony Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = 0
        event.loc_y = 100
        assert event.get_shot_distance() == 10

    def test_18ft_shot_get_shot_distance(self):
        event = StatsPbpEvent({'EVENTNUM': 115, 'PCTIMESTRING': '0:45.9', 'HOMEDESCRIPTION': "MISS Anthony Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = 100
        event.loc_y = 150
        assert event.get_shot_distance() == 18

    def test_18ft_shot_with_negative_x_coord_get_shot_distance(self):
        event = StatsPbpEvent({'EVENTNUM': 115, 'PCTIMESTRING': '0:45.9', 'HOMEDESCRIPTION': "MISS Anthony Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = -100
        event.loc_y = 150
        assert event.get_shot_distance() == 18

    def test_no_coords_get_shot_distance(self):
        event = StatsPbpEvent({'EVENTNUM': 115, 'PCTIMESTRING': '0:45.9', 'HOMEDESCRIPTION': "MISS Anthony 16' Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = None
        event.loc_y = None
        assert event.get_shot_distance() == 16

    def test_non_fg_get_shot_distance(self):
        event = StatsPbpEvent({'EVENTNUM': 110, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "O'Quinn Free Throw 2 of 2 (3 PTS)", 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.get_shot_distance() is None

    def test_no_coords_no_distance_in_description_get_shot_distance(self):
        event = StatsPbpEvent({'EVENTNUM': 115, 'PCTIMESTRING': '0:45.9', 'HOMEDESCRIPTION': "MISS Anthony Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        event.loc_x = None
        event.loc_y = None
        assert event.get_shot_distance() is None

    def test_made_ft_is_made_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 110, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "O'Quinn Free Throw 2 of 2 (3 PTS)", 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_made_ft() is True

    def test_missed_ft_is_made_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 108, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "MISS O'Quinn Free Throw 1 of 2", 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_made_ft() is False

    def test_made_ft_is_missed_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 110, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "O'Quinn Free Throw 2 of 2 (3 PTS)", 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_missed_ft() is False

    def test_missed_ft_is_missed_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 108, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "MISS O'Quinn Free Throw 1 of 2", 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_missed_ft() is True

    def test_substitution_is_substitution(self):
        event = StatsPbpEvent({'EVENTNUM': 126, 'PCTIMESTRING': '0:08.8', 'HOMEDESCRIPTION': "SUB: Porzingis FOR O'Quinn", 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': 204001, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_substitution() is True

    def test_ft_is_substitution(self):
        event = StatsPbpEvent({'EVENTNUM': 108, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "MISS O'Quinn Free Throw 1 of 2", 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_substitution() is False

    def test_technical_foul_is_technical_foul(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_technical_foul() is True

    def test_non_technical_foul_is_technical_foul(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 16})
        assert event.is_technical_foul() is False

    def test_double_technical_is_double_technical_foul(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_double_technical_foul() is False

    def test_non_double_technical_is_double_technical_foul(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 16})
        assert event.is_double_technical_foul() is True

    def test_ejection_is_ejection(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 11, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_ejection() is True

    def test_non_ejection_is_ejection(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 16, 'EVENTMSGACTIONTYPE': 16})
        assert event.is_ejection() is False

    def test_turnover_is_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 162, 'PCTIMESTRING': '09:07', 'HOMEDESCRIPTION': 'Ndour STEAL (1 STL)', 'VISITORDESCRIPTION': 'Ferrell Bad Pass Turnover (P2.T7)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1627812, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': 1626254, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_turnover() is True

    def test_ft_is_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 108, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "MISS O'Quinn Free Throw 1 of 2", 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_turnover() is False

    def test_no_turnover_is_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 325, 'PCTIMESTRING': '08:06', 'HOMEDESCRIPTION': 'Wall No Turnover (P3.T7)', 'VISITORDESCRIPTION': 'Smart STEAL (1 STL)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 202322, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': 203935, 'PLAYER2_TEAM_ID': 1610612738, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_turnover() is False

    def test_steal_is_steal(self):
        event = StatsPbpEvent({'EVENTNUM': 162, 'PCTIMESTRING': '09:07', 'HOMEDESCRIPTION': 'Ndour STEAL (1 STL)', 'VISITORDESCRIPTION': 'Ferrell Bad Pass Turnover (P2.T7)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1627812, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': 1626254, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_steal() is True

    def test_out_of_bounds_is_steal(self):
        event = StatsPbpEvent({'EVENTNUM': 166, 'PCTIMESTRING': '08:31', 'HOMEDESCRIPTION': 'Jennings Out of Bounds - Bad Pass Turnover Turnover (P2.T4)', 'EVENTMSGACTIONTYPE': 45, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 201943, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_steal() is False

    def test_out_of_bounds_is_lost_ball_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 166, 'PCTIMESTRING': '08:31', 'HOMEDESCRIPTION': 'Jennings Out of Bounds - Bad Pass Turnover Turnover (P2.T4)', 'EVENTMSGACTIONTYPE': 45, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 201943, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_lost_ball_turnover() is False

    def test_lost_ball_is_lost_ball_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 523, 'PCTIMESTRING': '08:09', 'HOMEDESCRIPTION': 'Washburn STEAL (2 STL)', 'VISITORDESCRIPTION': 'McKinnie Lost Ball Turnover (P1.T11)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1628035, 'PLAYER1_TEAM_ID': 1610612744, 'PLAYER2_ID': 1627395, 'PLAYER2_TEAM_ID': 1610612763, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_lost_ball_turnover() is True

    def test_lost_ball_out_of_bounds_is_lost_ball_out_of_bounds_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 67, 'PCTIMESTRING': '06:53', 'HOMEDESCRIPTION': 'Holiday Out of Bounds Lost Ball Turnover (P2.T2)', 'EVENTMSGACTIONTYPE': 40, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 203200, 'PLAYER1_TEAM_ID': 1610612763, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_lost_ball_out_of_bounds_turnover() is True

    def test_lost_ball_steal_is_lost_ball_out_of_bounds_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 523, 'PCTIMESTRING': '08:09', 'HOMEDESCRIPTION': 'Washburn STEAL (2 STL)', 'VISITORDESCRIPTION': 'McKinnie Lost Ball Turnover (P1.T11)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1628035, 'PLAYER1_TEAM_ID': 1610612744, 'PLAYER2_ID': 1627395, 'PLAYER2_TEAM_ID': 1610612763, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_lost_ball_out_of_bounds_turnover() is False

    def test_steal_is_bad_pass_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 162, 'PCTIMESTRING': '09:07', 'HOMEDESCRIPTION': 'Ndour STEAL (1 STL)', 'VISITORDESCRIPTION': 'Ferrell Bad Pass Turnover (P2.T7)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1627812, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': 1626254, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_bad_pass_turnover() is True

    def test_out_of_bounds_is_bad_pass_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 166, 'PCTIMESTRING': '08:31', 'HOMEDESCRIPTION': 'Jennings Out of Bounds - Bad Pass Turnover Turnover (P2.T4)', 'EVENTMSGACTIONTYPE': 45, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 201943, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_bad_pass_turnover() is False

    def test_out_of_bounds_is_bad_pass_out_of_bounds_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 166, 'PCTIMESTRING': '08:31', 'HOMEDESCRIPTION': 'Jennings Out of Bounds - Bad Pass Turnover Turnover (P2.T4)', 'EVENTMSGACTIONTYPE': 45, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 201943, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_bad_pass_out_of_bounds_turnover() is True

    def test_steal_is_bad_pass_out_of_bounds_turnover(self):
        event = StatsPbpEvent({'EVENTNUM': 162, 'PCTIMESTRING': '09:07', 'HOMEDESCRIPTION': 'Ndour STEAL (1 STL)', 'VISITORDESCRIPTION': 'Ferrell Bad Pass Turnover (P2.T7)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1627812, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': 1626254, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_bad_pass_out_of_bounds_turnover() is False

    def test_shot_clock_violation_is_shot_clock_violation(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 5, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_shot_clock_violation() is True

    def test_steal_is_shot_clock_violation(self):
        event = StatsPbpEvent({'EVENTNUM': 162, 'PCTIMESTRING': '09:07', 'HOMEDESCRIPTION': 'Ndour STEAL (1 STL)', 'VISITORDESCRIPTION': 'Ferrell Bad Pass Turnover (P2.T7)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1627812, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': 1626254, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_shot_clock_violation() is False

    def test_rebound_is_rebound(self):
        event = StatsPbpEvent({'EVENTNUM': 172, 'PCTIMESTRING': '08:18', 'HOMEDESCRIPTION': 'Ndour REBOUND (Off:0 Def:2)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1626254, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_rebound() is True

    def test_rebound_with_mtype_1_is_rebound(self):
        event = StatsPbpEvent({'EVENTNUM': 116, 'PCTIMESTRING': '0:45.5', 'VISITORDESCRIPTION': 'Nets Rebound', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1610612751, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_rebound() is False

    def test_rebound_with_mtype_1_and_pid_is_rebound(self):
        event = StatsPbpEvent({'EVENTNUM': 172, 'PCTIMESTRING': '08:18', 'HOMEDESCRIPTION': 'Ndour REBOUND (Off:0 Def:2)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1626254, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_rebound() is True

    def test_miss_rebound_make_is_putback(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:03', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is True

    def test_miss_rebound_make_outside_time_cutoff_is_putback(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:05', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_rebound_make_by_different_player_is_putback(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:03', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 11, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_rebound_assisted_make_is_putback(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:03', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'HOMEDESCRIPTION': "Green 25' 3PT Jump Shot (3 PTS) (Beal 1 AST)", 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_by_other_team_rebound_make_is_putback(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 121, 'PLAYER1_TEAM_ID': 2, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:03', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_putback() is False

    def test_miss_rebound_and1_foul_make_is_putback(self):
        # shooting foul event between rebound and made shot - pbp out of order
        events = StatsPeriod(
            [
                {'EVENTNUM': 591, 'PCTIMESTRING': '02:36', 'HOMEDESCRIPTION': "MISS Davis 5' Driving Layup", 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 203076, 'PLAYER1_TEAM_ID': 1610612740, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 593, 'PCTIMESTRING': '02:36', 'HOMEDESCRIPTION': 'Randle REBOUND (Off:3 Def:7)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 203944, 'PLAYER1_TEAM_ID': 1610612740, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 592, 'PCTIMESTRING': '02:36', 'VISITORDESCRIPTION': 'Capela S.FOUL (P4.PN) (Z.Zarba)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 203991, 'PLAYER1_TEAM_ID': 1610612745, 'PLAYER2_ID': 203944, 'PLAYER2_TEAM_ID': 1610612740, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 609, 'PCTIMESTRING': '02:36', 'HOMEDESCRIPTION': "Randle 6' Putback Layup (23 PTS)", 'EVENTMSGACTIONTYPE': 72, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 203944, 'PLAYER1_TEAM_ID': 1610612740, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 595, 'PCTIMESTRING': '02:36', 'HOMEDESCRIPTION': 'MISS Randle Free Throw 1 of 1', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203944, 'PLAYER1_TEAM_ID': 1610612740, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].is_putback() is True

    def test_miss_rebound_goaltend_make_is_putback(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 781, 'PCTIMESTRING': '01:14', 'VISITORDESCRIPTION': "MISS Shamet 7' Driving Floating Jump Shot", 'EVENTMSGACTIONTYPE': 101, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1629013, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 783, 'PCTIMESTRING': '01:13', 'VISITORDESCRIPTION': 'Muscala REBOUND (Off:1 Def:3)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 785, 'PCTIMESTRING': '01:12', 'HOMEDESCRIPTION': 'DiVincenzo Violation:Defensive Goaltending (N.Buchert)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 7, 'PLAYER1_ID': 1628978, 'PLAYER1_TEAM_ID': 1610612749, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 784, 'PCTIMESTRING': '01:12', 'VISITORDESCRIPTION': "Muscala 1' Tip Layup Shot (8 PTS)", 'EVENTMSGACTIONTYPE': 97, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].is_putback() is True

    def test_foul_is_foul(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 0})
        assert event.is_foul() is True

    def test_rebound_is_foul(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 1})
        assert event.is_foul() is False

    def test_personal_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 1})
        assert event.get_foul_type() == pbpstats.PERSONAL_FOUL_TYPE_STRING

    def test_shooting_foul_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2})
        assert event.get_foul_type() == pbpstats.SHOOTING_FOUL_TYPE_STRING

    def test_loose_ball_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 3})
        assert event.get_foul_type() == pbpstats.LOOSE_BALL_FOUL_TYPE_STRING

    def test_offensive_foul_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 4})
        assert event.get_foul_type() == pbpstats.OFFENSIVE_FOUL_TYPE_STRING

    def test_inbound_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 5})
        assert event.get_foul_type() == pbpstats.INBOUND_FOUL_TYPE_STRING

    def test_away_from_play_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 6})
        assert event.get_foul_type() == pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING

    def test_clear_path_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 9})
        assert event.get_foul_type() == pbpstats.CLEAR_PATH_FOUL_TYPE_STRING

    def test_double_foul_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 10})
        assert event.get_foul_type() == pbpstats.DOUBLE_FOUL_TYPE_STRING

    def test_flagrant1_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 14})
        assert event.get_foul_type() == pbpstats.FLAGRANT_1_FOUL_TYPE_STRING

    def test_flagrant2_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 15})
        assert event.get_foul_type() == pbpstats.FLAGRANT_2_FOUL_TYPE_STRING

    def test_def_3_seconds_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 17})
        assert event.get_foul_type() == pbpstats.DEFENSIVE_3_SECONDS_FOUL_TYPE_STRING

    def test_charge_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 26})
        assert event.get_foul_type() == pbpstats.CHARGE_FOUL_TYPE_STRING

    def test_block_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 27})
        assert event.get_foul_type() == pbpstats.PERSONAL_BLOCK_TYPE_STRING

    def test_take_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 28})
        assert event.get_foul_type() == pbpstats.PERSONAL_TAKE_TYPE_STRING

    def test_shooting_block_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 29})
        assert event.get_foul_type() == pbpstats.SHOOTING_BLOCK_TYPE_STRING

    def test_unknown_mtype_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 909})
        assert event.get_foul_type() is None

    def test_non_foul_get_foul_type(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 5, 'EVENTMSGACTIONTYPE': 1})
        assert event.get_foul_type() is None

    def test_personal_is_foul_that_counts_toward_penalty(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 1})
        assert event.is_foul_that_counts_toward_penalty() is True

    def test_offensive_foul_is_foul_that_counts_toward_penalty(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 4})
        assert event.is_foul_that_counts_toward_penalty() is False

    def test_1_of_2_is_first_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 110, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "O'Quinn Free Throw 1 of 2 (3 PTS)", 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_first_ft() is True

    def test_2_of_2_is_first_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 110, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "O'Quinn Free Throw 2 of 2 (3 PTS)", 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_first_ft() is False

    def test_tech_is_technical_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 91, 'PCTIMESTRING': '03:21', 'VISITORDESCRIPTION': 'MISS Bradley Free Throw Technical', 'EVENTMSGACTIONTYPE': 16, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 202340, 'PLAYER1_TEAM_ID': 1610612738, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_technical_ft() is True

    def test_2_of_2_is_technical_ft(self):
        event = StatsPbpEvent({'EVENTNUM': 110, 'PCTIMESTRING': '01:09', 'HOMEDESCRIPTION': "O'Quinn Free Throw 2 of 2 (3 PTS)", 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203124, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_technical_ft() is False

    def test_blocked_shot_is_blocked_shot(self):
        event = StatsPbpEvent({'EVENTNUM': 59, 'PCTIMESTRING': '05:27', 'HOMEDESCRIPTION': "MISS Porzingis 3' Layup", 'VISITORDESCRIPTION': "Lopez BLOCK (1 BLK)", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 204001, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': 201572, 'PLAYER2_TEAM_ID': 1610612751, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_blocked_shot() is True

    def test_missed_shot_is_blocked_shot(self):
        event = StatsPbpEvent({'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 1' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None})
        assert event.is_blocked_shot() is False

    def test_get_and1_shot(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 6, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 8, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 39, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 39, 'PCTIMESTRING': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[1].get_and1_shot() == events.Events[0]

    def test_get_number_of_fta_for_foul(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 6, 'VISITORDESCRIPTION': 'foul', 'PCTIMESTRING': '3:20', 'PLAYER1_ID': 10, 'PLAYER1_TEAM_ID': 2, 'PLAYER2_ID': 1, 'PLAYER2_TEAM_ID': 1},
                {'EVENTMSGTYPE': 3, 'HOMEDESCRIPTION': 'Free Throw 1 of 2', 'PCTIMESTRING': '3:20', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1},
                {'EVENTMSGTYPE': 3, 'HOMEDESCRIPTION': 'Free Throw 2 of 2', 'PCTIMESTRING': '3:20', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[0].get_number_of_fta_for_foul() == 2

        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 6, 'VISITORDESCRIPTION': 'foul', 'PCTIMESTRING': '3:20', 'PLAYER1_ID': 10, 'PLAYER1_TEAM_ID': 2, 'PLAYER2_ID': 1, 'PLAYER2_TEAM_ID': 1},
                {'EVENTMSGTYPE': 3, 'HOMEDESCRIPTION': 'Free Throw 1 of 3', 'PCTIMESTRING': '3:20', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1, 'EVENTMSGACTIONTYPE': 13, 'EVENTMSGTYPE': 3},
                {'EVENTMSGTYPE': 3, 'HOMEDESCRIPTION': 'Free Throw 2 of 3', 'PCTIMESTRING': '3:20', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1, 'EVENTMSGACTIONTYPE': 14, 'EVENTMSGTYPE': 3},
                {'EVENTMSGTYPE': 3, 'HOMEDESCRIPTION': 'Free Throw 3 of 3', 'PCTIMESTRING': '3:20', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1, 'EVENTMSGACTIONTYPE': 15, 'EVENTMSGTYPE': 3},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[0].get_number_of_fta_for_foul() == 3

        events = StatsPeriod(
            [
                {'EVENTNUM': 607, 'PCTIMESTRING': '0:25', 'VISITORDESCRIPTION': 'Jackson Free Throw 2 of 2 (16 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 202704, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 608, 'PCTIMESTRING': '0:25', 'HOMEDESCRIPTION': 'Wizards Timeout: Regular (Reg.5 Short 0)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 9, 'PLAYER1_ID': 1610612764, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 609, 'PCTIMESTRING': '0:25', 'VISITORDESCRIPTION': 'Griffin AWAY.FROM.PLAY.FOUL (P5.PN) (M.Davis)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 201933, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': 201145, 'PLAYER2_TEAM_ID': 1610612764, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 611, 'PCTIMESTRING': '0:25', 'HOMEDESCRIPTION': 'Beal Free Throw 1 of 1 (32 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203078, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 612, 'PCTIMESTRING': '0:24', 'VISITORDESCRIPTION': "MISS Green 27' 3PT Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 201145, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_number_of_fta_for_foul() == 1

        events = StatsPeriod(
            [
                {'EVENTNUM': 168, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'Lillard Free Throw 1 of 2 (7 PTS)', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203081, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 169, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'SUB: Aminu FOR Layman', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 1627774, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': 202329, 'PLAYER2_TEAM_ID': 1610612757, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 171, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'Lillard Free Throw 2 of 2 (8 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203081, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 172, 'PCTIMESTRING': '0:39', 'VISITORDESCRIPTION': 'Noel AWAY.FROM.PLAY.FOUL (P2.PN) (M.Ervin)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 203457, 'PLAYER1_TEAM_ID': 1610612760, 'PLAYER2_ID': 202683, 'PLAYER2_TEAM_ID': 1610612757, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 174, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'Kanter Free Throw 1 of 1 (1 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 202683, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].get_number_of_fta_for_foul() == 1

    def test_1_fta_on_away_from_play_on_made_ft_get_number_of_fta_for_foul(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 607, 'PCTIMESTRING': '0:25', 'VISITORDESCRIPTION': 'Jackson Free Throw 2 of 2 (16 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 202704, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 608, 'PCTIMESTRING': '0:25', 'HOMEDESCRIPTION': 'Wizards Timeout: Regular (Reg.5 Short 0)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 9, 'PLAYER1_ID': 1610612764, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 609, 'PCTIMESTRING': '0:25', 'VISITORDESCRIPTION': 'Griffin AWAY.FROM.PLAY.FOUL (P5.PN) (M.Davis)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 201933, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': 201145, 'PLAYER2_TEAM_ID': 1610612764, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 611, 'PCTIMESTRING': '0:25', 'HOMEDESCRIPTION': 'Beal Free Throw 1 of 1 (32 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203078, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 612, 'PCTIMESTRING': '0:24', 'VISITORDESCRIPTION': "MISS Green 27' 3PT Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 201145, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_number_of_fta_for_foul() == 1

        events = StatsPeriod(
            [
                {'EVENTNUM': 168, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'Lillard Free Throw 1 of 2 (7 PTS)', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203081, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 169, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'SUB: Aminu FOR Layman', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 1627774, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': 202329, 'PLAYER2_TEAM_ID': 1610612757, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 171, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'Lillard Free Throw 2 of 2 (8 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203081, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 172, 'PCTIMESTRING': '0:39', 'VISITORDESCRIPTION': 'Noel AWAY.FROM.PLAY.FOUL (P2.PN) (M.Ervin)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 203457, 'PLAYER1_TEAM_ID': 1610612760, 'PLAYER2_ID': 202683, 'PLAYER2_TEAM_ID': 1610612757, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 174, 'PCTIMESTRING': '0:39', 'HOMEDESCRIPTION': 'Kanter Free Throw 1 of 1 (1 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 202683, 'PLAYER1_TEAM_ID': 1610612757, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].get_number_of_fta_for_foul() == 1

    def test_get_foul_that_resulted_in_ft_excluding_techs(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 3, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 11, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 8, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_foul_that_resulted_in_ft_excluding_techs() == events.Events[1]

    def test_ignore_tech_get_foul_that_resulted_in_ft_excluding_techs(self):
        # technical which should be ignored at index 1 which should be ignored
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 11, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 3, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 11, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 8, 'EVENTMSGACTIONTYPE': 2, 'PCTIMESTRING': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_foul_that_resulted_in_ft_excluding_techs() == events.Events[0]

    def test_foul_out_of_order_get_foul_that_resulted_in_ft(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 474, 'PCTIMESTRING': '0:42', 'VISITORDESCRIPTION': 'Lamb REBOUND (Off:2 Def:8)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 203087, 'PLAYER1_TEAM_ID': 1610612766, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 470, 'PCTIMESTRING': '0:37', 'HOMEDESCRIPTION': 'Wiggins P.FOUL (P1.T2) (D.Collins)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 203952, 'PLAYER1_TEAM_ID': 1610612750, 'PLAYER2_ID': 203087, 'PLAYER2_TEAM_ID': 1610612766, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 477, 'PCTIMESTRING': '0:30', 'VISITORDESCRIPTION': 'Lamb Free Throw 1 of 2 (15 PTS)', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203087, 'PLAYER1_TEAM_ID': 1610612766, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 478, 'PCTIMESTRING': '0:30', 'HOMEDESCRIPTION': 'Wiggins S.FOUL (P1.T2) (D.Collins)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 203952, 'PLAYER1_TEAM_ID': 1610612750, 'PLAYER2_ID': 203087, 'PLAYER2_TEAM_ID': 1610612766, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 479, 'PCTIMESTRING': '0:30', 'VISITORDESCRIPTION': 'Lamb Free Throw 2 of 2 (16 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203087, 'PLAYER1_TEAM_ID': 1610612766, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].get_foul_that_resulted_in_ft() == events.Events[3]

    def testset_next_and_previous_event_for_all_events(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 6, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 8, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 39, 'PCTIMESTRING': '3:20'},
                {'EVENTMSGTYPE': 39, 'PCTIMESTRING': '3:20'},
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[0].previous_event is None
        assert events.Events[0].next_event.order == 1
        assert events.Events[4].previous_event.order == 3
        assert events.Events[4].next_event is None

    def test_player_def_reb_get_rebound_data(self):
        """
        test for checking rebound type is correct
        """
        player_def_2pt_reb_shot = {
            'PCTIMESTRING': '10:26',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 123,
        }
        player_def_2pt_reb = {
            'PCTIMESTRING': '10:24',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        player_def_3pt_reb_shot = {
            'PCTIMESTRING': '10:18',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 1111,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'miss 3PT Shot',
        }
        player_def_3pt_reb = {
            'PCTIMESTRING': '10:16',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }
        player_def_ft_reb_shot = {
            'PCTIMESTRING': '10:15',
            'EVENTMSGTYPE': 3,
            'EVENTMSGACTIONTYPE': 12,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'MISS Free Throw 2 of 2',
        }
        player_def_ft_reb = {
            'PCTIMESTRING': '10:14',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        pbp = StatsPeriod(
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
            'PCTIMESTRING': '10:26',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
        }
        player_off_2pt_reb = {
            'PCTIMESTRING': '10:24',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        player_off_3pt_reb_shot = {
            'PCTIMESTRING': '10:18',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'miss 3PT Shot',
        }
        player_off_3pt_reb = {
            'PCTIMESTRING': '10:16',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }
        player_off_ft_reb_shot = {
            'PCTIMESTRING': '10:15',
            'EVENTMSGTYPE': 3,
            'EVENTMSGACTIONTYPE': 12,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'MISS Free Throw 2 of 2',
        }
        player_off_ft_reb = {
            'PCTIMESTRING': '10:14',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        pbp = StatsPeriod(
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
            'PCTIMESTRING': '10:26',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 123,
        }
        team_def_2pt_reb = {
            'PCTIMESTRING': '10:24',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        team_def_3pt_reb_shot = {
            'PCTIMESTRING': '10:18',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 1111,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'miss 3PT Shot',
        }
        team_def_3pt_reb = {
            'PCTIMESTRING': '10:16',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }
        team_def_ft_reb_shot = {
            'PCTIMESTRING': '10:15',
            'EVENTMSGTYPE': 3,
            'EVENTMSGACTIONTYPE': 12,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'MISS Free Throw',
        }
        team_def_ft_reb = {
            'PCTIMESTRING': '10:14',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        pbp = StatsPeriod(
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
            'PCTIMESTRING': '10:26',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
        }
        team_off_2pt_reb = {
            'PCTIMESTRING': '10:24',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        team_off_3pt_reb_shot = {
            'PCTIMESTRING': '10:18',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'miss 3PT Shot',
        }
        team_off_3pt_reb = {
            'PCTIMESTRING': '10:16',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }
        team_off_ft_reb_shot = {
            'PCTIMESTRING': '10:15',
            'EVENTMSGTYPE': 3,
            'EVENTMSGACTIONTYPE': 12,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
            'HOMEDESCRIPTION': 'MISS Free Throw',
        }
        team_off_ft_reb = {
            'PCTIMESTRING': '10:14',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }

        pbp = StatsPeriod(
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
            'PCTIMESTRING': '10:15',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 123,
        }
        shot_clock_violation = {
            'PCTIMESTRING': '10:14',
            'EVENTMSGTYPE': 5,
            'EVENTMSGACTIONTYPE': 11,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 0,
            'HOMEDESCRIPTION': 'shot clock violation',
        }
        team_reb = {
            'PCTIMESTRING': '10:14',
            'PLAYER1_ID': 0,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
        }
        end_of_period_shot = {
            'PCTIMESTRING': '0:01',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 111,
            'PLAYER1_ID': 123,
        }
        end_of_period_reb = {
            'PCTIMESTRING': '0:00',
            'PLAYER1_ID': 909,
            'PLAYER1_TEAM_ID': None,
            'EVENTMSGTYPE': 4,
        }

        pbp = StatsPeriod(
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
        events = StatsPeriod(
            [
                {'EVENTNUM': 679, 'PCTIMESTRING': '06:42', 'HOMEDESCRIPTION': 'MISS Len Driving Layup Shot', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 2, 'PLAYER1_TEAM_ID': 1610612737, 'PLAYER1_ID': 203458, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 680, 'PCTIMESTRING': '06:39', 'HOMEDESCRIPTION': 'Prince Rebound (Off:2 Def:2)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_TEAM_ID': 1610612737, 'PLAYER1_ID': 1627752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 681, 'PCTIMESTRING': '06:39', 'HOMEDESCRIPTION': 'Hawks Shot Clock Turnover', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 5, 'PLAYER1_TEAM_ID': None, 'PLAYER1_ID': 1610612737, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is not None
        assert reb_data['def_reb'] is False

    def test_team_reb_from_lb_foul_at_end_of_period_get_rebound_data(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 541, 'PCTIMESTRING': '0:01', 'VISITORDESCRIPTION': "MISS Brown Jr. 6' Driving Floating Jump Shot", 'EVENTMSGACTIONTYPE': 101, 'EVENTMSGTYPE': 2, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER1_ID': 1628972, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 545, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'NETS Rebound', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_TEAM_ID': None, 'PLAYER1_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 543, 'PCTIMESTRING': '0:00', 'VISITORDESCRIPTION': 'Bryant L.B.FOUL (P2.PN) (M.Lindsay)', 'EVENTMSGACTIONTYPE': 3, 'EVENTMSGTYPE': 6, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER1_ID': 1628418, 'PLAYER2_ID': 1626178, 'PLAYER2_TEAM_ID': 1610612751, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 546, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'Hollis-Jefferson Free Throw 1 of 2 (2 PTS)', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER1_ID': 1626178, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 548, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'Hollis-Jefferson Free Throw 2 of 2 (3 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER1_ID': 1626178, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )

        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is not None

    def test_team_reb_at_end_of_period_with_event_between_get_rebound_data(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 369, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'Missed Bazemore 3pt Shot', 'EVENTMSGACTIONTYPE': 103, 'EVENTMSGTYPE': 2, 'PLAYER1_TEAM_ID': 1610612737, 'PLAYER1_ID': 203145, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 370, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'Hawks Rebound', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1610612737, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 372, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'Instant Replay - Support Ruling', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 18, 'PLAYER1_ID': None, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 371, 'PCTIMESTRING': '0:00', 'HOMEDESCRIPTION': 'End Period', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 13, 'PLAYER1_ID': None, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )

        reb_data = events.Events[1].get_rebound_data()
        assert reb_data is None

    def test_start_of_period_is_start_of_period(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 12, 'EVENTMSGACTIONTYPE': 0})
        assert event.is_start_of_period() is True

    def test_end_of_period_is_start_of_period(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 13, 'EVENTMSGACTIONTYPE': 0})
        assert event.is_start_of_period() is False

    def test_end_of_period_is_end_of_period(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 13, 'EVENTMSGACTIONTYPE': 0})
        assert event.is_end_of_period() is True

    def test_start_of_period_is_end_of_period(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 12, 'EVENTMSGACTIONTYPE': 0})
        assert event.is_end_of_period() is False

    def test_delay_of_game_is_delay_of_game(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 18})
        assert event.is_delay_of_game() is True

    def test_non_delay_of_game_is_delay_of_game(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 8})
        assert event.is_delay_of_game() is False

    def test_1_of_1_is_ft_1_of_1(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10})
        assert event.is_ft_1_of_1() is True

    def test_1_of_2_is_ft_1_of_1(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_ft_1_of_1() is False

    def test_2_of_2_is_ft_2_of_2(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 12})
        assert event.is_ft_2_of_2() is True

    def test_1_of_2_is_ft_2_of_2(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_ft_2_of_2() is False

    def test_3_of_3_is_ft_3_of_3(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 15})
        assert event.is_ft_3_of_3() is True

    def test_1_of_3_is_ft_3_of_3(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 13})
        assert event.is_ft_3_of_3() is False

    def test_jump_ball_is_jump_ball(self):
        event = StatsPbpEvent({'EVENTNUM': 4, 'PCTIMESTRING': '12:00', 'HOMEDESCRIPTION': "Jump Ball Drummond vs. Bryant: Tip to Griffin", 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 10, 'PLAYER1_ID': 203083, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': 1628418, 'PLAYER2_TEAM_ID': 1610612764, 'PLAYER3_ID': 201933, 'PLAYER3_TEAM_ID': 1610612765})
        assert event.is_jump_ball() is True

    def test_non_jump_ball_is_jump_ball(self):
        event = StatsPbpEvent({'EVENTMSGTYPE': 13, 'EVENTMSGACTIONTYPE': 11})
        assert event.is_jump_ball() is False

    def test_away_from_play_is_away_from_play_ft(self):
        events = StatsPeriod(
            [
                {'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1},
                {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 6, 'VISITORDESCRIPTION': 'Away From Play Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 2},
                {'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'VISITORDESCRIPTION': 'Made Shot by team that got fouled', 'PCTIMESTRING': '0:35', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 2},
            ],
            self.GameId,
            self.Period
        )

        assert events.Events[0].is_away_from_play_ft() is True

    def test_foul_on_made_shot_by_team_that_got_fouled_is_away_from_play_ft(self):
        events = StatsPeriod(
            [
                StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1}),
                StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 6, 'VISITORDESCRIPTION': 'Away From Play Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 3}),
                StatsPbpEvent({'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Made Shot by team that got fouled', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 2}),
            ],
            self.GameId,
            self.Period
        )

        assert events.Events[0].is_away_from_play_ft() is False

    def test_foul_on_made_shot_by_team_that_didnt_get_fouled_is_away_from_play_ft(self):
        events = StatsPeriod(
            [
                StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 1}),
                StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 6, 'VISITORDESCRIPTION': 'Away From Play Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 2}),
                StatsPbpEvent({'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'VISITORDESCRIPTION': 'Made Shot by team that got didnt get fouled', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 3}),
            ],
            self.GameId,
            self.Period
        )

        assert events.Events[0].is_away_from_play_ft() is True

    def test_foul_on_made_ft_by_team_that_got_fouled_is_away_from_play_ft(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 499, 'PCTIMESTRING': '04:51', 'HOMEDESCRIPTION': "Lowry 27' 3PT Pullup Jump Shot (15 PTS)", 'EVENTMSGACTIONTYPE': 79, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 200768, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 500, 'PCTIMESTRING': '04:32', 'HOMEDESCRIPTION': 'Leonard S.FOUL (P3.T2) (S.Foster)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 202695, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': 203954, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 502, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'Embiid Free Throw 1 of 2 (19 PTS)', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203954, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 503, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'SUB: Fultz FOR Simmons', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 1627732, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': 1628365, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 505, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'Embiid Free Throw 2 of 2 (20 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203954, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 506, 'PCTIMESTRING': '04:32', 'HOMEDESCRIPTION': 'Siakam AWAY.FROM.PLAY.FOUL (P2.T3) (T.Ford)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 1627783, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': 203488, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 509, 'PCTIMESTRING': '04:32', 'HOMEDESCRIPTION': 'SUB: Johnson FOR Embiid', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 203954, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': 101161, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 511, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'Muscala Free Throw 1 of 1 (10 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 512, 'PCTIMESTRING': '04:17', 'HOMEDESCRIPTION': "MISS Siakam 3' Turnaround Fadeaway Shot", 'EVENTMSGACTIONTYPE': 86, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1627783, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 513, 'PCTIMESTRING': '04:15', 'VISITORDESCRIPTION': 'Muscala REBOUND (Off:2 Def:3)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 514, 'PCTIMESTRING': '04:04', 'VISITORDESCRIPTION': "Fultz 15' Pullup Jump Shot (5 PTS)", 'EVENTMSGACTIONTYPE': 79, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 1628365, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[2].is_away_from_play_ft() is False
        assert events.Events[4].is_away_from_play_ft() is False
        assert events.Events[6].is_away_from_play_ft() is False

    def test_foul_on_made_ft_by_team_that_didnt_get_fouled_is_away_from_play_ft(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 607, 'PCTIMESTRING': '0:25', 'VISITORDESCRIPTION': 'Jackson Free Throw 2 of 2 (16 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 202704, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 608, 'PCTIMESTRING': '0:25', 'HOMEDESCRIPTION': 'Wizards Timeout: Regular (Reg.5 Short 0)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 9, 'PLAYER1_ID': 1610612764, 'PLAYER1_TEAM_ID': None, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 609, 'PCTIMESTRING': '0:25', 'VISITORDESCRIPTION': 'Griffin AWAY.FROM.PLAY.FOUL (P5.PN) (M.Davis)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 201933, 'PLAYER1_TEAM_ID': 1610612765, 'PLAYER2_ID': 201145, 'PLAYER2_TEAM_ID': 1610612764, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 611, 'PCTIMESTRING': '0:25', 'HOMEDESCRIPTION': 'Beal Free Throw 1 of 1 (32 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203078, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 612, 'PCTIMESTRING': '0:24', 'VISITORDESCRIPTION': "MISS Green 27' 3PT Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 201145, 'PLAYER1_TEAM_ID': 1610612764, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        assert events.Events[3].is_away_from_play_ft() is True

    def test_away_from_play_is_inbound_foul_ft(self):
        events = StatsPeriod([
            StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1}),
            StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 6, 'VISITORDESCRIPTION': 'Away From Play Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_inbound_foul_ft() is False

    def test_inbound_foul_is_inbound_foul_ft(self):
        events = StatsPeriod([
            StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1}),
            StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 5, 'VISITORDESCRIPTION': 'Inbound Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_inbound_foul_ft() is True

    def test_tech_at_time_of_make_is_and1_shot(self):
        events = StatsPeriod([
            StatsPbpEvent({'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1}),
            StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 11, 'VISITORDESCRIPTION': 'Technical Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is False

    def test_and1_is_and1_shot(self):
        events = StatsPeriod([
            StatsPbpEvent({'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45'}),
            StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'VISITORDESCRIPTION': 'Shooting Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2}),
            StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is True

    def test_and1_with_foul_out_of_order_is_and1_shot(self):
        events = StatsPeriod([
            StatsPbpEvent({'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45'}),
            StatsPbpEvent({'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1}),
            StatsPbpEvent({'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'VISITORDESCRIPTION': 'Shooting Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2}),
        ], self.GameId, self.Period)

        assert events.Events[0].is_and1_shot() is True

    def test_oreb_is_second_chance_event(self):
        first_shot = {
            'EVENTNUM': 1,
            'PCTIMESTRING': '10:26',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
        }
        first_oreb = {
            'EVENTNUM': 2,
            'PCTIMESTRING': '10:25',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
            'EVENTMSGACTIONTYPE': 0,
        }
        second_shot = {
            'EVENTNUM': 3,
            'PCTIMESTRING': '10:16',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 0,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
        }
        second_oreb = {
            'EVENTNUM': 4,
            'PCTIMESTRING': '10:15',
            'PLAYER1_ID': 12345,
            'PLAYER1_TEAM_ID': 909,
            'EVENTMSGTYPE': 4,
            'EVENTMSGACTIONTYPE': 0,
        }
        third_shot = {
            'EVENTNUM': 5,
            'PCTIMESTRING': '10:14',
            'EVENTMSGTYPE': 2,
            'EVENTMSGACTIONTYPE': 1,
            'PLAYER1_TEAM_ID': 909,
            'PLAYER1_ID': 123,
        }

        pbp = StatsPeriod(
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
        shot = StatsPbpEvent(
            {
                'EVENTNUM': 1,
                'PCTIMESTRING': '10:26',
                'EVENTMSGTYPE': 2,
                'EVENTMSGACTIONTYPE': 0,
                'PLAYER1_TEAM_ID': 909,
                'PLAYER1_ID': 123,
            }
        )
        dreb = StatsPbpEvent(
            {
                'EVENTNUM': 2,
                'PCTIMESTRING': '10:25',
                'PLAYER1_ID': 12345,
                'PLAYER1_TEAM_ID': 908,
                'EVENTMSGTYPE': 4,
                'EVENTMSGACTIONTYPE': 0,
            }
        )
        pbp = StatsPeriod([shot, dreb], self.GameId, self.Period)

        assert pbp.Events[0].is_second_chance_event(pbp.Events) is False

    def test_get_all_events_at_event_time(self):
        events = StatsPeriod(
            [
                {'EVENTNUM': 499, 'PCTIMESTRING': '04:51', 'HOMEDESCRIPTION': "Lowry 27' 3PT Pullup Jump Shot (15 PTS)", 'EVENTMSGACTIONTYPE': 79, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 200768, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 500, 'PCTIMESTRING': '04:32', 'HOMEDESCRIPTION': 'Leonard S.FOUL (P3.T2) (S.Foster)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 202695, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': 203954, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 502, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'Embiid Free Throw 1 of 2 (19 PTS)', 'EVENTMSGACTIONTYPE': 11, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203954, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 503, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'SUB: Fultz FOR Simmons', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 1627732, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': 1628365, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 505, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'Embiid Free Throw 2 of 2 (20 PTS)', 'EVENTMSGACTIONTYPE': 12, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203954, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 506, 'PCTIMESTRING': '04:32', 'HOMEDESCRIPTION': 'Siakam AWAY.FROM.PLAY.FOUL (P2.T3) (T.Ford)', 'EVENTMSGACTIONTYPE': 6, 'EVENTMSGTYPE': 6, 'PLAYER1_ID': 1627783, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': 203488, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 509, 'PCTIMESTRING': '04:32', 'HOMEDESCRIPTION': 'SUB: Johnson FOR Embiid', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 8, 'PLAYER1_ID': 203954, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': 101161, 'PLAYER2_TEAM_ID': 1610612755, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 511, 'PCTIMESTRING': '04:32', 'VISITORDESCRIPTION': 'Muscala Free Throw 1 of 1 (10 PTS)', 'EVENTMSGACTIONTYPE': 10, 'EVENTMSGTYPE': 3, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 512, 'PCTIMESTRING': '04:17', 'HOMEDESCRIPTION': "MISS Siakam 3' Turnaround Fadeaway Shot", 'EVENTMSGACTIONTYPE': 86, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1627783, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 513, 'PCTIMESTRING': '04:15', 'VISITORDESCRIPTION': 'Muscala REBOUND (Off:2 Def:3)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None},
                {'EVENTNUM': 514, 'PCTIMESTRING': '04:04', 'VISITORDESCRIPTION': "Fultz 15' Pullup Jump Shot (5 PTS)", 'EVENTMSGACTIONTYPE': 79, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 1628365, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
            ],
            self.GameId,
            self.Period
        )
        filtered_events = events.Events[4].get_all_events_at_event_time()
        assert len(filtered_events) == 7
        assert filtered_events[0].number == 500
        assert filtered_events[-1].number == 511

        assert len(events.Events[0].get_all_events_at_event_time()) == 1
