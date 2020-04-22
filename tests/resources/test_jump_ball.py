from pbpstats.resources.enhanced_pbp.stats_nba.jump_ball import StatsJumpBall
from pbpstats.resources.enhanced_pbp.stats_nba.field_goal import StatsFieldGoal
from pbpstats.resources.enhanced_pbp.stats_nba.rebound import StatsRebound
from pbpstats.resources.enhanced_pbp.stats_nba.turnover import StatsTurnover


def test_dangling_jump_ball_changes_possession():
    shot = {'GAME_ID': '0021900510', 'EVENTNUM': 225, 'PCTIMESTRING': '6:40', 'VISITORDESCRIPTION': 'MISS Lowry  3PT Jump Shot', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 200768, 'PLAYER1_TEAM_ID': 1610612761}
    order = 1
    shot_event = StatsFieldGoal(shot, order)
    rebound = {'GAME_ID': '0021900510', 'EVENTNUM': 226, 'PCTIMESTRING': '6:38', 'HOMEDESCRIPTION': 'Silva REBOUND (Off:0 Def:1)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    jump_ball = {'GAME_ID': '0021900510', 'EVENTNUM': 228, 'PCTIMESTRING': '6:29', 'HOMEDESCRIPTION': 'Jump Ball Silva vs. Boucher: Tip to Johnson', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 10, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748, 'PLAYER2_ID': 1628449, 'PLAYER2_TEAM_ID': 1610612761, 'PLAYER3_ID': 1626169, 'PLAYER3_TEAM_ID': 1610612761}
    order = 1
    jump_ball_event = StatsJumpBall(jump_ball, order)
    turnover = {'GAME_ID': '0021900510', 'EVENTNUM': 233, 'PCTIMESTRING': '6:11', 'HOMEDESCRIPTION': "Herro STEAL (1 STL)", 'VISITORDESCRIPTION': "Hollis-Jefferson Lost Ball Turnover (P1.T5)", 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1626178, 'PLAYER1_TEAM_ID': 1610612761, 'PLAYER2_ID': 1629639, 'PLAYER2_TEAM_ID': 1610612748}
    order = 1
    turnover_event = StatsTurnover(turnover, order)

    shot_event.previous_event = None
    shot_event.next_event = rebound_event
    rebound_event.previous_event = shot_event
    rebound_event.next_event = jump_ball_event
    jump_ball_event.previous_event = rebound_event
    jump_ball_event.next_event = turnover_event
    turnover_event.previous_event = jump_ball_event
    turnover_event.next_event = None

    assert jump_ball_event.is_possession_ending_event is True


def test_jump_ball_turnover_next_event_not_possession_change():
    shot = {'GAME_ID': '0021900510', 'EVENTNUM': 225, 'PCTIMESTRING': '6:40', 'VISITORDESCRIPTION': 'MISS Lowry  3PT Jump Shot', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 200768, 'PLAYER1_TEAM_ID': 1610612761}
    order = 1
    shot_event = StatsFieldGoal(shot, order)
    rebound = {'GAME_ID': '0021900510', 'EVENTNUM': 226, 'PCTIMESTRING': '6:38', 'HOMEDESCRIPTION': 'Silva REBOUND (Off:0 Def:1)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    jump_ball = {'GAME_ID': '0021900510', 'EVENTNUM': 228, 'PCTIMESTRING': '6:29', 'HOMEDESCRIPTION': 'Jump Ball Silva vs. Boucher: Tip to Johnson', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 10, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748, 'PLAYER2_ID': 1628449, 'PLAYER2_TEAM_ID': 1610612761, 'PLAYER3_ID': 1626169, 'PLAYER3_TEAM_ID': 1610612761}
    order = 1
    jump_ball_event = StatsJumpBall(jump_ball, order)
    turnover = {'GAME_ID': '0021900510', 'EVENTNUM': 233, 'PCTIMESTRING': '6:29', 'VISITORDESCRIPTION': "Boucher STEAL (1 STL)", 'HOMEDESCRIPTION': "Silva Lost Ball Turnover (P1.T5)", 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748, 'PLAYER2_ID': 1628449, 'PLAYER2_TEAM_ID': 1610612761}
    order = 1
    turnover_event = StatsTurnover(turnover, order)

    shot_event.previous_event = None
    shot_event.next_event = rebound_event
    rebound_event.previous_event = shot_event
    rebound_event.next_event = jump_ball_event
    jump_ball_event.previous_event = rebound_event
    jump_ball_event.next_event = turnover_event
    turnover_event.previous_event = jump_ball_event
    turnover_event.next_event = None

    assert jump_ball_event.is_possession_ending_event is False


def test_jump_ball_turnover_previous_event_not_possession_change():
    shot = {'GAME_ID': '0021900510', 'EVENTNUM': 225, 'PCTIMESTRING': '6:40', 'VISITORDESCRIPTION': 'MISS Lowry  3PT Jump Shot', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 200768, 'PLAYER1_TEAM_ID': 1610612761}
    order = 1
    shot_event = StatsFieldGoal(shot, order)
    rebound = {'GAME_ID': '0021900510', 'EVENTNUM': 226, 'PCTIMESTRING': '6:38', 'HOMEDESCRIPTION': 'Silva REBOUND (Off:0 Def:1)', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 4, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748}
    order = 1
    rebound_event = StatsRebound(rebound, order)
    turnover = {'GAME_ID': '0021900510', 'EVENTNUM': 233, 'PCTIMESTRING': '6:29', 'VISITORDESCRIPTION': "Boucher STEAL (1 STL)", 'HOMEDESCRIPTION': "Silva Lost Ball Turnover (P1.T5)", 'EVENTMSGACTIONTYPE': 2, 'EVENTMSGTYPE': 5, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748, 'PLAYER2_ID': 1628449, 'PLAYER2_TEAM_ID': 1610612761}
    order = 1
    turnover_event = StatsTurnover(turnover, order)
    jump_ball = {'GAME_ID': '0021900510', 'EVENTNUM': 228, 'PCTIMESTRING': '6:29', 'HOMEDESCRIPTION': 'Jump Ball Silva vs. Boucher: Tip to Johnson', 'EVENTMSGACTIONTYPE': 0, 'EVENTMSGTYPE': 10, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748, 'PLAYER2_ID': 1628449, 'PLAYER2_TEAM_ID': 1610612761, 'PLAYER3_ID': 1626169, 'PLAYER3_TEAM_ID': 1610612761}
    order = 1
    jump_ball_event = StatsJumpBall(jump_ball, order)
    shot2 = {'GAME_ID': '0021900510', 'EVENTNUM': 225, 'PCTIMESTRING': '6:15', 'VISITORDESCRIPTION': 'Silva Lowry  3PT Jump Shot', 'EVENTMSGACTIONTYPE': 1, 'EVENTMSGTYPE': 2, 'PLAYER1_ID': 1629735, 'PLAYER1_TEAM_ID': 1610612748}
    order = 1
    shot2_event = StatsFieldGoal(shot2, order)

    shot_event.previous_event = None
    shot_event.next_event = rebound_event
    rebound_event.previous_event = shot_event
    rebound_event.next_event = turnover_event
    turnover_event.previous_event = rebound_event
    turnover_event.next_event = jump_ball_event
    jump_ball_event.previous_event = turnover_event
    jump_ball_event.next_event = shot2_event
    shot2_event.previous_event = jump_ball_event
    shot2_event.next_event = None

    assert jump_ball_event.is_possession_ending_event is False
