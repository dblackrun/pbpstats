import pbpstats
from pbpstats.resources.enhanced_pbp.data_nba.field_goal import DataFieldGoal
from pbpstats.resources.enhanced_pbp.stats_nba.field_goal import StatsFieldGoal
from pbpstats.resources.enhanced_pbp.stats_nba.foul import StatsFoul
from pbpstats.resources.enhanced_pbp.stats_nba.free_throw import StatsFreeThrow
from pbpstats.resources.enhanced_pbp.stats_nba.rebound import StatsRebound
from pbpstats.resources.enhanced_pbp.stats_nba.turnover import StatsTurnover
from pbpstats.resources.enhanced_pbp.stats_nba.violation import StatsViolation


def test_data_field_goal_3_shot_value_is_3():
    item = {'evt': 20, 'cl': '09:57', 'de': '[NYK 5-2] Rose 3pt Shot: Made (5 PTS) Assist: Anthony (1 AST)', 'locX': -230, 'locY': 28, 'mtype': 1, 'etype': 1, 'opid': '', 'tid': 1610612752, 'pid': 201565, 'hs': 5, 'vs': 2, 'epid': '2546', 'oftid': 1610612752}
    period = 1
    game_id = '0021900001'
    fg = DataFieldGoal(item, period, game_id)
    assert fg.shot_value == 3


def test_data_field_goal_2_shot_value_is_2():
    item = {'evt': 14, 'cl': '10:34', 'de': '[BKN] Bogdanovic Layup Shot: Missed', 'locX': 4, 'locY': 16, 'mtype': 5, 'etype': 2, 'opid': '', 'tid': 1610612751, 'pid': 202711, 'hs': 2, 'vs': 2, 'epid': '', 'oftid': 1610612751}
    period = 1
    game_id = '0021900001'
    fg = DataFieldGoal(item, period, game_id)
    assert fg.shot_value == 2


def test_stats_field_goal_3_shot_value_is_3():
    item = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg = StatsFieldGoal(item, order)
    assert fg.shot_value == 3


def test_stats_field_goal_2_shot_value_is_2():
    item = {'EVENTNUM': 14, 'PCTIMESTRING': '10:34', 'VISITORDESCRIPTION': "MISS Bogdanovic 2' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg = StatsFieldGoal(item, order)
    assert fg.shot_value == 2


def test_made_true():
    event = {'EVENTNUM': 21, 'PCTIMESTRING': '09:31', 'VISITORDESCRIPTION': "Bogdanovic 2' Driving Layup (2 PTS)", 'EVENTMSGACTIONTYPE': 42, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.made is True


def test_made_false():
    event = {'EVENTNUM': 14, 'PCTIMESTRING': '10:34', 'VISITORDESCRIPTION': "MISS Bogdanovic 2' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.made is False


def test_blocked_true():
    event = {'EVENTNUM': 59, 'PCTIMESTRING': '05:27', 'HOMEDESCRIPTION': "MISS Porzingis 3' Layup", 'VISITORDESCRIPTION': "Lopez BLOCK (1 BLK)", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 204001, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': 201572, 'PLAYER3_TEAM_ID': 1610612751}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.blocked is True


def test_blocked_false():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 1' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.blocked is False


def test_assisted_true():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': 2546, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.assisted is True


def test_assisted_false():
    event = {'EVENTNUM': 21, 'PCTIMESTRING': '09:31', 'VISITORDESCRIPTION': "Bogdanovic 2' Driving Layup (2 PTS)", 'EVENTMSGACTIONTYPE': 42, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.assisted is False


def test_rebound_event_on_miss():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 1' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)

    rebound = {'EVENTNUM': 62, 'PCTIMESTRING': '05:20', 'HOMEDESCRIPTION': 'Thomas Rebound (Off:0 Def:1)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 202498, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 2
    rebound_event = StatsRebound(rebound, order)

    fg_event.next_event = rebound_event
    rebound_event.previous_event = fg_event
    rebound_event.next_event = None
    assert fg_event.rebound == rebound_event


def test_placeholder_rebound_event_on_miss_returns_none():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 1' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)

    rebound = {'EVENTNUM': 62, 'PCTIMESTRING': '05:20', 'HOMEDESCRIPTION': 'Knicks Rebound', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 0, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 2
    rebound_event = StatsRebound(rebound, order)

    fg_event.next_event = rebound_event
    rebound_event.previous_event = fg_event
    rebound_event.next_event = None
    assert fg_event.rebound is None


def test_heave_true():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '00:01', 'HOMEDESCRIPTION': "Rose 45' 3PT Jump Shot (5 PTS) (Anthony 1 AST)", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': 2546, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.is_heave is True


def test_heave_false():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': "Rose 25' 3PT Jump Shot (5 PTS) (Anthony 1 AST)", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': 2546, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.is_heave is False


def test_corner3_true():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    fg_event.locX = -230
    fg_event.locY = 28
    assert fg_event.is_corner_3 is True


def test_corner3_false():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    fg_event.locX = -230
    fg_event.locY = 100
    assert fg_event.is_corner_3 is False


def test_corner3_no_coords_is_false():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.is_corner_3 is False


def test_corner3_2pt_is_false():
    event = {'EVENTNUM': 21, 'PCTIMESTRING': '09:31', 'VISITORDESCRIPTION': "Bogdanovic 2' Driving Layup (2 PTS)", 'EVENTMSGACTIONTYPE': 42, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.is_corner_3 is False


def test_distance_with_coords():
    event = {'EVENTNUM': 115, 'PCTIMESTRING': '00:46', 'HOMEDESCRIPTION': "MISS Anthony Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    fg_event.locX = -100
    fg_event.locY = 150
    assert fg_event.distance == 18


def test_distance_without_coords_from_description():
    event = {'EVENTNUM': 115, 'PCTIMESTRING': '00:46', 'HOMEDESCRIPTION': "MISS Anthony 16' Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.distance == 16


def test_distance_no_coords_or_description_returns_none():
    event = {'EVENTNUM': 115, 'PCTIMESTRING': '00:46', 'HOMEDESCRIPTION': "MISS Anthony Jump Shot", 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 2546, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.distance is None


def test_shot_type_corner3():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    fg_event.locX = -230
    fg_event.locY = 28
    assert fg_event.shot_type == pbpstats.CORNER_3_STRING


def test_shot_type_arc3():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': '2546', 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    fg_event.locX = -230
    fg_event.locY = 100
    assert fg_event.shot_type == pbpstats.ARC_3_STRING


def test_shot_type_at_rim():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 1' Layup", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.shot_type == pbpstats.AT_RIM_STRING


def test_shot_type_short_mid_range():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 12' Jump Shot", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.shot_type == pbpstats.SHORT_MID_RANGE_STRING


def test_shot_type_long_mid_range():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson 19' Jump Shot", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.shot_type == pbpstats.LONG_MID_RANGE_STRING


def test_shot_type_unknown():
    event = {'EVENTNUM': 61, 'PCTIMESTRING': '05:21', 'VISITORDESCRIPTION': "MISS Hollis-Jefferson Jump Shot", 'EVENTMSGACTIONTYPE': 5, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.shot_type == pbpstats.UNKNOWN_SHOT_DISTANCE_STRING


def test_putback_true():
    miss = {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    miss_event = StatsFieldGoal(miss, order)
    rebound = {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:03', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    make = {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    make_event = StatsFieldGoal(make, order)
    miss_event.previous_event = None
    miss_event.next_event = rebound_event
    rebound_event.previous_event = miss_event
    rebound_event.next_event = make_event
    make_event.previous_event = rebound_event
    make_event.next_event = None
    assert make_event.putback is True


def test_putback_outside_time_cutoff_false():
    miss = {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    miss_event = StatsFieldGoal(miss, order)
    rebound = {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:05', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    make = {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    make_event = StatsFieldGoal(make, order)
    miss_event.previous_event = None
    miss_event.next_event = rebound_event
    rebound_event.previous_event = miss_event
    rebound_event.next_event = make_event
    make_event.previous_event = rebound_event
    make_event.next_event = None
    assert make_event.putback is False


def test_putback_reb_by_different_player_false():
    miss = {'EVENTMSGTYPE': 2, 'PCTIMESTRING': '1:06', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    miss_event = StatsFieldGoal(miss, order)
    rebound = {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PCTIMESTRING': '1:03', 'PLAYER1_ID': 13, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    make = {'EVENTMSGTYPE': 1, 'PCTIMESTRING': '1:02', 'PLAYER1_ID': 12, 'PLAYER1_TEAM_ID': 1, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    make_event = StatsFieldGoal(make, order)
    miss_event.previous_event = None
    miss_event.next_event = rebound_event
    rebound_event.previous_event = miss_event
    rebound_event.next_event = make_event
    make_event.previous_event = rebound_event
    make_event.next_event = None
    assert make_event.putback is False


def test_putback_goaltend_true():
    miss = {'EVENTNUM': 781, 'PCTIMESTRING': '01:14', 'VISITORDESCRIPTION': "MISS Shamet 7' Driving Floating Jump Shot", 'EVENTMSGACTIONTYPE': 101, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1629013, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    miss_event = StatsFieldGoal(miss, order)
    rebound = {'EVENTNUM': 783, 'PCTIMESTRING': '01:13', 'VISITORDESCRIPTION': 'Muscala REBOUND (Off:1 Def:3)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    goaltend = {'EVENTNUM': 785, 'PCTIMESTRING': '01:12', 'HOMEDESCRIPTION': 'DiVincenzo Violation:Defensive Goaltending (N.Buchert)', 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 7, 'PLAYER1_ID': 1628978, 'PLAYER1_TEAM_ID': 1610612749, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    goaltend_event = StatsViolation(goaltend, order)
    make = {'EVENTNUM': 784, 'PCTIMESTRING': '01:12', 'VISITORDESCRIPTION': "Muscala 1' Tip Layup Shot (8 PTS)", 'EVENTMSGACTIONTYPE': 97, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 203488, 'PLAYER1_TEAM_ID': 1610612755, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    make_event = StatsFieldGoal(make, order)
    miss_event.previous_event = None
    miss_event.next_event = rebound_event
    rebound_event.previous_event = miss_event
    rebound_event.next_event = goaltend_event
    goaltend_event.previous_event = rebound_event
    goaltend_event.next_event = make_event
    make_event.previous_event = goaltend_event
    make_event.next_event = None
    assert make_event.putback is True


def test_putback_3pt_false():
    event = {'EVENTNUM': 20, 'PCTIMESTRING': '09:57', 'HOMEDESCRIPTION': 'Rose  3PT Jump Shot (5 PTS) (Anthony 1 AST)', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 201565, 'PLAYER1_TEAM_ID': 1610612752, 'PLAYER2_ID': 2546, 'PLAYER2_TEAM_ID': 1610612752, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    assert fg_event.putback is False


def test_putback_no_prev_event_false():
    event = {'EVENTNUM': 21, 'PCTIMESTRING': '09:31', 'VISITORDESCRIPTION': "Bogdanovic 2' Driving Layup (2 PTS)", 'EVENTMSGACTIONTYPE': 42, 'EVENTMSGTYPE': 1, 'PLAYER1_ID': 202711, 'PLAYER1_TEAM_ID': 1610612751, 'PLAYER2_ID': None, 'PLAYER2_TEAM_ID': None, 'PLAYER3_ID': None, 'PLAYER3_TEAM_ID': None}
    order = 1
    fg_event = StatsFieldGoal(event, order)
    fg_event.previous_event = None
    assert fg_event.putback is False


def test_and1_shot_at_time_of_and1_ft_is_false():
    make = {'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'PLAYER1_ID': 15, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45', 'EVENTNUM': 1}
    order = 1
    make_event = StatsFieldGoal(make, order)
    foul = {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'VISITORDESCRIPTION': 'Shooting Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 12, 'PLAYER2_ID': 15, 'EVENTNUM': 2}
    order = 1
    foul_event = StatsFoul(foul, order)
    ft = {'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 15, 'EVENTNUM': 3}
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    rebound = {'EVENTMSGTYPE': 4, 'EVENTMSGACTIONTYPE': 0, 'PLAYER1_ID': 17, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Rebound', 'PCTIMESTRING': '0:45', 'EVENTNUM': 4}
    order = 2
    rebound_event = StatsRebound(rebound, order)
    tip = {'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'PLAYER1_ID': 17, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45', 'EVENTNUM': 5}
    order = 1
    tip_event = StatsFieldGoal(tip, order)
    make_event.previous_event = None
    make_event.next_event = foul_event
    foul_event.previous_event = make_event
    foul_event.next_event = ft_event
    ft_event.previous_event = foul_event
    ft_event.next_event = rebound_event
    rebound_event.previous_event = ft_event
    rebound_event.next_event = tip_event
    tip_event.previous_event = rebound_event
    tip_event.next_event = None
    assert make_event.and1 is True
    assert tip_event.and1 is False


def test_and1_with_foul_out_of_order_true():
    make = {'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'PLAYER1_ID': 15, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45', 'EVENTNUM': 1}
    order = 1
    make_event = StatsFieldGoal(make, order)
    ft = {'EVENTMSGTYPE': 3, 'EVENTMSGACTIONTYPE': 10, 'HOMEDESCRIPTION': 'Free Throw 1 of 1', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 15, 'EVENTNUM': 2}
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    foul = {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'VISITORDESCRIPTION': 'Shooting Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 12, 'PLAYER2_ID': 15, 'EVENTNUM': 3}
    order = 1
    foul_event = StatsFoul(foul, order)
    make_event.previous_event = None
    make_event.next_event = ft_event
    ft_event.previous_event = make_event
    ft_event.next_event = foul_event
    foul_event.previous_event = ft_event
    foul_event.next_event = None
    assert make_event.and1 is True


def test_and1_with_lane_violation_true():
    make = {'EVENTMSGTYPE': 1, 'EVENTMSGACTIONTYPE': 10, 'PLAYER1_ID': 15, 'PLAYER1_TEAM_ID': 1, 'HOMEDESCRIPTION': 'Made Shot', 'PCTIMESTRING': '0:45', 'EVENTNUM': 1}
    order = 1
    make_event = StatsFieldGoal(make, order)
    foul = {'EVENTMSGTYPE': 6, 'EVENTMSGACTIONTYPE': 2, 'VISITORDESCRIPTION': 'Shooting Foul', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 2, 'PLAYER1_ID': 12, 'PLAYER2_ID': 15, 'EVENTNUM': 2}
    order = 1
    foul_event = StatsFoul(foul, order)
    lane_violation = {'EVENTMSGTYPE': 5, 'EVENTMSGACTIONTYPE': 17, 'HOMEDESCRIPTION': 'Lane Violation Turnover', 'PCTIMESTRING': '0:45', 'PLAYER1_TEAM_ID': 1, 'PLAYER1_ID': 15, 'PLAYER2_ID': None, 'EVENTNUM': 3}
    order = 1
    lane_violation_event = StatsTurnover(lane_violation, order)
    make_event.previous_event = None
    make_event.next_event = foul_event
    foul_event.previous_event = make_event
    foul_event.next_event = lane_violation_event
    lane_violation_event.previous_event = foul_event
    lane_violation_event.next_event = None
    assert make_event.and1 is True
