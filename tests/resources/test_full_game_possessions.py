import pbpstats
from pbpstats.client import Client


class TestFullGamePossessions:
    settings = {
        'dir': 'tests/data',
        'Possessions': {'source': 'file', 'data_provider': 'stats_nba'},
    }
    client = Client(settings)
    game = client.Game('0021600270')

    def test_first_possession_start_time(self):
        assert self.game.possessions.items[0].start_time == '12:00'

    def test_first_possession_start_type(self):
        assert self.game.possessions.items[0].possession_start_type == pbpstats.OFF_DEADBALL_STRING

    def test_off_short_mid_range_make_start_type(self):
        assert self.game.possessions.items[1].possession_start_type == f'Off{pbpstats.SHORT_MID_RANGE_STRING}{pbpstats.MAKE_STRING}'
        assert self.game.possessions.items[1].previous_possession_end_shooter_player_id == 202693
        assert self.game.possessions.items[1].previous_possession_end_rebound_player_id == 0
        assert self.game.possessions.items[1].previous_possession_end_turnover_player_id == 0
        assert self.game.possessions.items[1].previous_possession_end_steal_player_id == 0

    def test_off_arc3_miss_start_type(self):
        assert self.game.possessions.items[3].possession_start_type == f'Off{pbpstats.ARC_3_STRING}{pbpstats.MISS_STRING}'
        assert self.game.possessions.items[3].previous_possession_end_shooter_player_id == 202322
        assert self.game.possessions.items[3].previous_possession_end_rebound_player_id == 1627734

    def test_off_short_mid_range_miss_start_type(self):
        assert self.game.possessions.items[4].possession_start_type == f'Off{pbpstats.SHORT_MID_RANGE_STRING}{pbpstats.MISS_STRING}'

    def test_off_live_ball_turnover_start_type(self):
        assert self.game.possessions.items[5].possession_start_type == pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
        assert self.game.possessions.items[5].previous_possession_end_shooter_player_id == 0
        assert self.game.possessions.items[5].previous_possession_end_rebound_player_id == 0
        assert self.game.possessions.items[5].previous_possession_end_turnover_player_id == 202693
        assert self.game.possessions.items[5].previous_possession_end_steal_player_id == 1627734

    def test_dead_ball_turnover_start_type(self):
        assert self.game.possessions.items[20].possession_start_type == pbpstats.OFF_DEADBALL_STRING

    def test_off_timeout_start_type(self):
        assert self.game.possessions.items[23].possession_start_type == pbpstats.OFF_TIMEOUT_STRING

    def test_team_rebound_start_type(self):
        assert self.game.possessions.items[24].possession_start_type == pbpstats.OFF_DEADBALL_STRING

    def test_first_possession_stats(self):
        assert self.game.possessions.items[0].possession_stats == [
            {'player_id': 101162, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'OffPoss', 'stat_value': 1},
            {'player_id': 101162, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'PlusMinus', 'stat_value': 2},
            {'player_id': 101162, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'SecondsPlayedOff', 'stat_value': 21.0},
            {'player_id': 201566, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'DefPoss', 'stat_value': 1},
            {'player_id': 201566, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'OpponentPoints', 'stat_value': 2},
            {'player_id': 201566, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'PlusMinus', 'stat_value': -2},
            {'player_id': 201566, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'SecondsPlayedDef', 'stat_value': 21.0},
            {'player_id': 202322, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'OffPoss', 'stat_value': 1},
            {'player_id': 202322, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'PlusMinus', 'stat_value': 2},
            {'player_id': 202322, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'SecondsPlayedOff', 'stat_value': 21.0},
            {'player_id': 202693, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'OffPoss', 'stat_value': 1},
            {'player_id': 202693, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'PlusMinus', 'stat_value': 2},
            {'player_id': 202693, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'SecondsPlayedOff', 'stat_value': 21.0},
            {'player_id': 202693, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'Total2ptShotDistance', 'stat_value': 12.1},
            {'player_id': 202693, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'Total2ptShotsWithDistance', 'stat_value': 1},
            {'player_id': 202693, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'UnassistedShortMidRange', 'stat_value': 1},
            {'player_id': 203078, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'OffPoss', 'stat_value': 1},
            {'player_id': 203078, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'PlusMinus', 'stat_value': 2},
            {'player_id': 203078, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'SecondsPlayedOff', 'stat_value': 21.0},
            {'player_id': 203460, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'DefPoss', 'stat_value': 1},
            {'player_id': 203460, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'OpponentPoints', 'stat_value': 2},
            {'player_id': 203460, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'PlusMinus', 'stat_value': -2},
            {'player_id': 203460, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'SecondsPlayedDef', 'stat_value': 21.0},
            {'player_id': 203490, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'OffPoss', 'stat_value': 1},
            {'player_id': 203490, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'PlusMinus', 'stat_value': 2},
            {'player_id': 203490, 'team_id': 1610612764, 'opponent_team_id': 1610612760, 'lineup_id': '101162-202322-202693-203078-203490', 'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'stat_key': 'SecondsPlayedOff', 'stat_value': 21.0},
            {'player_id': 203500, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'DefPoss', 'stat_value': 1},
            {'player_id': 203500, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'OpponentPoints', 'stat_value': 2},
            {'player_id': 203500, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'PlusMinus', 'stat_value': -2},
            {'player_id': 203500, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'SecondsPlayedDef', 'stat_value': 21.0},
            {'player_id': 203506, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'DefPoss', 'stat_value': 1},
            {'player_id': 203506, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'OpponentPoints', 'stat_value': 2},
            {'player_id': 203506, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'PlusMinus', 'stat_value': -2},
            {'player_id': 203506, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'SecondsPlayedDef', 'stat_value': 21.0},
            {'player_id': 1627734, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'DefPoss', 'stat_value': 1},
            {'player_id': 1627734, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'OpponentPoints', 'stat_value': 2},
            {'player_id': 1627734, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'PlusMinus', 'stat_value': -2},
            {'player_id': 1627734, 'team_id': 1610612760, 'opponent_team_id': 1610612764, 'lineup_id': '1627734-201566-203460-203500-203506', 'opponent_lineup_id': '101162-202322-202693-203078-203490', 'stat_key': 'SecondsPlayedDef', 'stat_value': 21.0}
        ]

    def test_team_stats(self):
        results = self.game.possessions.team_stats
        assert results == [
            {'team_id': 1610612760, 'stat_key': '1627734:AssistsTo:201566:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '1627734:AssistsTo:203506:LongMidRange', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:1627734:AtRim', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:202683:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:202683:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:203460:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:203460:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:203500:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:203506:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201566:AssistsTo:203530:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201627:AssistsTo:202683:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201627:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201627:AssistsTo:203530:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '201627:AssistsTo:203924:Corner3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203506:AssistsTo:1627734:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203506:AssistsTo:1627734:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203506:AssistsTo:201566:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203506:AssistsTo:201566:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203506:AssistsTo:203460:Corner3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203506:AssistsTo:203500:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203530:AssistsTo:201627:Corner3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203902:AssistsTo:201627:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203902:AssistsTo:202683:AtRim', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203902:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '203924:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': '2pt And 1 Free Throw Trips', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': '2pt Shooting Foul Free Throw Trips', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'Arc3Assists', 'stat_value': 7},
            {'team_id': 1610612760, 'stat_key': 'Arc3DefReboundOpportunities', 'stat_value': 12},
            {'team_id': 1610612760, 'stat_key': 'Arc3DefRebounds', 'stat_value': 10},
            {'team_id': 1610612760, 'stat_key': 'Arc3OffReboundOpportunities', 'stat_value': 12},
            {'team_id': 1610612760, 'stat_key': 'Arc3OffRebounded', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'Arc3OffReboundedOpportunities', 'stat_value': 12},
            {'team_id': 1610612760, 'stat_key': 'Arc3OffRebounds', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'AssistedArc3', 'stat_value': 7},
            {'team_id': 1610612760, 'stat_key': 'AssistedAtRim', 'stat_value': 14},
            {'team_id': 1610612760, 'stat_key': 'AssistedCorner3', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AssistedLongMidRange', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'AssistedShortMidRange', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimAssists', 'stat_value': 14},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlocked', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlockedDefReboundOpportunities', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlockedDefRebounds', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffReboundOpportunities', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffRebounded', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffReboundedOpportunities', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffRebounds', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'AtRimDefReboundOpportunities', 'stat_value': 10},
            {'team_id': 1610612760, 'stat_key': 'AtRimDefRebounds', 'stat_value': 8},
            {'team_id': 1610612760, 'stat_key': 'AtRimOffReboundOpportunities', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'AtRimOffRebounded', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimOffReboundedOpportunities', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'AtRimOffRebounds', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'AtRimSelfOReb', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'BadPassOutOfBoundsTurnovers', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'BadPassSteals', 'stat_value': 8},
            {'team_id': 1610612760, 'stat_key': 'BadPassTurnovers', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'BlockedAtRim', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'BlockedAtRimRecovered', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'BlockedShortMidRange', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'BlockedShortMidRangeRecovered', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'Corner3Assists', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'Corner3DefReboundOpportunities', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'Corner3DefRebounds', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'Corner3OffReboundOpportunities', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'Corner3OffRebounded', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'Corner3OffReboundedOpportunities', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'Corner3OffRebounds', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'DeadBallTurnovers', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'DefPoss', 'stat_value': 108},
            {'team_id': 1610612760, 'stat_key': 'DefensiveGoaltends', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'FTDefReboundOpportunities', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'FTDefRebounds', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'FTOffReboundOpportunities', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'FTOffRebounded', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'FTOffReboundedOpportunities', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'FTOffRebounds', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'FtsMade', 'stat_value': 22},
            {'team_id': 1610612760, 'stat_key': 'FtsMissed', 'stat_value': 9},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeAssists', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeDefReboundOpportunities', 'stat_value': 9},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeDefRebounds', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeOffReboundOpportunities', 'stat_value': 10},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeOffRebounded', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeOffReboundedOpportunities', 'stat_value': 10},
            {'team_id': 1610612760, 'stat_key': 'LongMidRangeOffRebounds', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'Loose Ball Fouls', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'Loose Ball Fouls Drawn', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'LostBallOutOfBoundsTurnovers', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'LostBallSteals', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'LostBallTurnovers', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'MissedArc3', 'stat_value': 12},
            {'team_id': 1610612760, 'stat_key': 'MissedAtRim', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'MissedCorner3', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'MissedLongMidRange', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'MissedShortMidRange', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'OffPoss', 'stat_value': 109},
            {'team_id': 1610612760, 'stat_key': 'OnFloorOffReb', 'stat_value': 65},
            {'team_id': 1610612760, 'stat_key': 'OpponentPoints', 'stat_value': 115},
            {'team_id': 1610612760, 'stat_key': 'Penalty Free Throw Trips', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'Personal Block Fouls Drawn', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'Personal Fouls', 'stat_value': 7},
            {'team_id': 1610612760, 'stat_key': 'Personal Fouls Drawn', 'stat_value': 7},
            {'team_id': 1610612760, 'stat_key': 'Personal Take Fouls', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'Personal Take Fouls Drawn', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'PlusMinus', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'Putbacks', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'SecondsPlayedDef', 'stat_value': 1636},
            {'team_id': 1610612760, 'stat_key': 'SecondsPlayedOff', 'stat_value': 1544},
            {'team_id': 1610612760, 'stat_key': 'Shooting Block Fouls Drawn', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'Shooting Fouls', 'stat_value': 12},
            {'team_id': 1610612760, 'stat_key': 'Shooting Fouls Drawn', 'stat_value': 11},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeAssists', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeBlockedDefReboundOpportunities', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeBlockedDefRebounds', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeDefReboundOpportunities', 'stat_value': 12},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeDefRebounds', 'stat_value': 8},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffReboundOpportunities', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffRebounded', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffReboundedOpportunities', 'stat_value': 6},
            {'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffRebounds', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'ShotClockViolations', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'Technical Free Throw Trips', 'stat_value': 1},
            {'team_id': 1610612760, 'stat_key': 'Total2ptShotDistance', 'stat_value': 428.5},
            {'team_id': 1610612760, 'stat_key': 'Total2ptShotsWithDistance', 'stat_value': 65},
            {'team_id': 1610612760, 'stat_key': 'Total3ptShotDistance', 'stat_value': 728.0},
            {'team_id': 1610612760, 'stat_key': 'Total3ptShotsWithDistance', 'stat_value': 30},
            {'team_id': 1610612760, 'stat_key': 'Travels', 'stat_value': 3},
            {'team_id': 1610612760, 'stat_key': 'UnassistedArc3', 'stat_value': 2},
            {'team_id': 1610612760, 'stat_key': 'UnassistedAtRim', 'stat_value': 9},
            {'team_id': 1610612760, 'stat_key': 'UnassistedLongMidRange', 'stat_value': 4},
            {'team_id': 1610612760, 'stat_key': 'UnassistedShortMidRange', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': '101162:AssistsTo:203078:Arc3', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '101162:AssistsTo:203078:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '1626162:AssistsTo:203490:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:101162:AtRim', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:1626162:Arc3', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:201160:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:202693:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203078:AtRim', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203078:Corner3', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203078:LongMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203078:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203490:Arc3', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203490:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202322:AssistsTo:203490:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202693:AssistsTo:101162:ShortMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '202693:AssistsTo:203078:Arc3', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '203078:AssistsTo:203490:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '203107:AssistsTo:1626162:Arc3', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '203107:AssistsTo:201977:Arc3', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '203107:AssistsTo:202693:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '203490:AssistsTo:1626162:AtRim', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '2pt And 1 Free Throw Trips', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': '2pt Shooting Foul Free Throw Trips', 'stat_value': 11},
            {'team_id': 1610612764, 'stat_key': 'Arc3Assists', 'stat_value': 6},
            {'team_id': 1610612764, 'stat_key': 'Arc3DefReboundOpportunities', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'Arc3DefRebounds', 'stat_value': 10},
            {'team_id': 1610612764, 'stat_key': 'Arc3OffReboundOpportunities', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'Arc3OffRebounded', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'Arc3OffReboundedOpportunities', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'Arc3OffRebounds', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'AssistedArc3', 'stat_value': 6},
            {'team_id': 1610612764, 'stat_key': 'AssistedAtRim', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'AssistedCorner3', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'AssistedLongMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'AssistedShortMidRange', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'AtRimAssists', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlocked', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlockedDefReboundOpportunities', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlockedDefRebounds', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlockedOffReboundOpportunities', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlockedOffRebounded', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlockedOffReboundedOpportunities', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'AtRimBlockedOffRebounds', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'AtRimDefReboundOpportunities', 'stat_value': 11},
            {'team_id': 1610612764, 'stat_key': 'AtRimDefRebounds', 'stat_value': 8},
            {'team_id': 1610612764, 'stat_key': 'AtRimOffReboundOpportunities', 'stat_value': 10},
            {'team_id': 1610612764, 'stat_key': 'AtRimOffRebounded', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'AtRimOffReboundedOpportunities', 'stat_value': 10},
            {'team_id': 1610612764, 'stat_key': 'AtRimOffRebounds', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'BadPassSteals', 'stat_value': 6},
            {'team_id': 1610612764, 'stat_key': 'BadPassTurnovers', 'stat_value': 8},
            {'team_id': 1610612764, 'stat_key': 'BlockedAtRim', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'BlockedAtRimRecovered', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'Corner3Assists', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'Corner3DefReboundOpportunities', 'stat_value': 6},
            {'team_id': 1610612764, 'stat_key': 'Corner3DefRebounds', 'stat_value': 5},
            {'team_id': 1610612764, 'stat_key': 'Corner3OffReboundOpportunities', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'Corner3OffReboundedOpportunities', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'DeadBallTurnovers', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'DefPoss', 'stat_value': 109},
            {'team_id': 1610612764, 'stat_key': 'FTDefReboundOpportunities', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'FTDefRebounds', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'FTOffReboundOpportunities', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'FTOffReboundedOpportunities', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'FtsMade', 'stat_value': 17},
            {'team_id': 1610612764, 'stat_key': 'FtsMissed', 'stat_value': 9},
            {'team_id': 1610612764, 'stat_key': 'HeaveMisses', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeAssists', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeDefReboundOpportunities', 'stat_value': 10},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeDefRebounds', 'stat_value': 7},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeOffReboundOpportunities', 'stat_value': 9},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeOffRebounded', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeOffReboundedOpportunities', 'stat_value': 9},
            {'team_id': 1610612764, 'stat_key': 'LongMidRangeOffRebounds', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'Loose Ball Fouls', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'Loose Ball Fouls Drawn', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'LostBallOutOfBoundsTurnovers', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'LostBallSteals', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'LostBallTurnovers', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'MissedArc3', 'stat_value': 13},
            {'team_id': 1610612764, 'stat_key': 'MissedAtRim', 'stat_value': 10},
            {'team_id': 1610612764, 'stat_key': 'MissedCorner3', 'stat_value': 5},
            {'team_id': 1610612764, 'stat_key': 'MissedLongMidRange', 'stat_value': 9},
            {'team_id': 1610612764, 'stat_key': 'MissedShortMidRange', 'stat_value': 13},
            {'team_id': 1610612764, 'stat_key': 'OffPoss', 'stat_value': 108},
            {'team_id': 1610612764, 'stat_key': 'OnFloorOffReb', 'stat_value': 65},
            {'team_id': 1610612764, 'stat_key': 'OpponentPoints', 'stat_value': 126},
            {'team_id': 1610612764, 'stat_key': 'Penalty Free Throw Trips', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'Personal Block Fouls', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'Personal Fouls', 'stat_value': 7},
            {'team_id': 1610612764, 'stat_key': 'Personal Fouls Drawn', 'stat_value': 7},
            {'team_id': 1610612764, 'stat_key': 'Personal Take Fouls', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'Personal Take Fouls Drawn', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'PlusMinus', 'stat_value': -11},
            {'team_id': 1610612764, 'stat_key': 'Putbacks', 'stat_value': 3},
            {'team_id': 1610612764, 'stat_key': 'SecondsPlayedDef', 'stat_value': 1544},
            {'team_id': 1610612764, 'stat_key': 'SecondsPlayedOff', 'stat_value': 1636},
            {'team_id': 1610612764, 'stat_key': 'Shooting Block Fouls', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'Shooting Fouls', 'stat_value': 11},
            {'team_id': 1610612764, 'stat_key': 'Shooting Fouls Drawn', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeAssists', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeBlocked', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeBlockedOffReboundOpportunities', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeBlockedOffReboundedOpportunities', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeDefReboundOpportunities', 'stat_value': 6},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeDefRebounds', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeOffReboundOpportunities', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeOffRebounded', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeOffReboundedOpportunities', 'stat_value': 12},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeOffRebounds', 'stat_value': 4},
            {'team_id': 1610612764, 'stat_key': 'ShortMidRangeSelfOReb', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'ShotClockViolations', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'Technical Free Throw Trips', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'Total2ptShotDistance', 'stat_value': 442.3},
            {'team_id': 1610612764, 'stat_key': 'Total2ptShotsWithDistance', 'stat_value': 70},
            {'team_id': 1610612764, 'stat_key': 'Total3ptShotDistance', 'stat_value': 697.3},
            {'team_id': 1610612764, 'stat_key': 'Total3ptShotsWithDistance', 'stat_value': 28},
            {'team_id': 1610612764, 'stat_key': 'UnassistedArc3', 'stat_value': 2},
            {'team_id': 1610612764, 'stat_key': 'UnassistedAtRim', 'stat_value': 10},
            {'team_id': 1610612764, 'stat_key': 'UnassistedLongMidRange', 'stat_value': 1},
            {'team_id': 1610612764, 'stat_key': 'UnassistedShortMidRange', 'stat_value': 6},
        ]

    def test_opponent_stats(self):
        results = self.game.possessions.opponent_stats
        assert results == [
            {'opponent_team_id': 1610612760, 'stat_key': '101162:AssistsTo:203078:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '101162:AssistsTo:203078:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '1626162:AssistsTo:203490:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:101162:AtRim', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:1626162:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:201160:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:202693:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203078:AtRim', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203078:Corner3', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203078:LongMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203078:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203490:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203490:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202322:AssistsTo:203490:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202693:AssistsTo:101162:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '202693:AssistsTo:203078:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '203078:AssistsTo:203490:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '203107:AssistsTo:1626162:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '203107:AssistsTo:201977:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '203107:AssistsTo:202693:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '203490:AssistsTo:1626162:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '2pt And 1 Free Throw Trips', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': '2pt Shooting Foul Free Throw Trips', 'stat_value': 11},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3Assists', 'stat_value': 6},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3DefReboundOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3DefRebounds', 'stat_value': 10},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3OffReboundOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3OffRebounded', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3OffReboundedOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'Arc3OffRebounds', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'AssistedArc3', 'stat_value': 6},
            {'opponent_team_id': 1610612760, 'stat_key': 'AssistedAtRim', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'AssistedCorner3', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'AssistedLongMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'AssistedShortMidRange', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimAssists', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlocked', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlockedDefReboundOpportunities', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlockedDefRebounds', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlockedOffReboundOpportunities', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlockedOffRebounded', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlockedOffReboundedOpportunities', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimBlockedOffRebounds', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimDefReboundOpportunities', 'stat_value': 11},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimDefRebounds', 'stat_value': 8},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimOffReboundOpportunities', 'stat_value': 10},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimOffRebounded', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimOffReboundedOpportunities', 'stat_value': 10},
            {'opponent_team_id': 1610612760, 'stat_key': 'AtRimOffRebounds', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'BadPassSteals', 'stat_value': 6},
            {'opponent_team_id': 1610612760, 'stat_key': 'BadPassTurnovers', 'stat_value': 8},
            {'opponent_team_id': 1610612760, 'stat_key': 'BlockedAtRim', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'BlockedAtRimRecovered', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'Corner3Assists', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'Corner3DefReboundOpportunities', 'stat_value': 6},
            {'opponent_team_id': 1610612760, 'stat_key': 'Corner3DefRebounds', 'stat_value': 5},
            {'opponent_team_id': 1610612760, 'stat_key': 'Corner3OffReboundOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'Corner3OffReboundedOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'DeadBallTurnovers', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'DefPoss', 'stat_value': 109},
            {'opponent_team_id': 1610612760, 'stat_key': 'FTDefReboundOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'FTDefRebounds', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'FTOffReboundOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'FTOffReboundedOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'FtsMade', 'stat_value': 17},
            {'opponent_team_id': 1610612760, 'stat_key': 'FtsMissed', 'stat_value': 9},
            {'opponent_team_id': 1610612760, 'stat_key': 'HeaveMisses', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeAssists', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeDefReboundOpportunities', 'stat_value': 10},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeDefRebounds', 'stat_value': 7},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeOffReboundOpportunities', 'stat_value': 9},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeOffRebounded', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeOffReboundedOpportunities', 'stat_value': 9},
            {'opponent_team_id': 1610612760, 'stat_key': 'LongMidRangeOffRebounds', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'Loose Ball Fouls', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'Loose Ball Fouls Drawn', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'LostBallOutOfBoundsTurnovers', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'LostBallSteals', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'LostBallTurnovers', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'MissedArc3', 'stat_value': 13},
            {'opponent_team_id': 1610612760, 'stat_key': 'MissedAtRim', 'stat_value': 10},
            {'opponent_team_id': 1610612760, 'stat_key': 'MissedCorner3', 'stat_value': 5},
            {'opponent_team_id': 1610612760, 'stat_key': 'MissedLongMidRange', 'stat_value': 9},
            {'opponent_team_id': 1610612760, 'stat_key': 'MissedShortMidRange', 'stat_value': 13},
            {'opponent_team_id': 1610612760, 'stat_key': 'OffPoss', 'stat_value': 108},
            {'opponent_team_id': 1610612760, 'stat_key': 'OnFloorOffReb', 'stat_value': 65},
            {'opponent_team_id': 1610612760, 'stat_key': 'OpponentPoints', 'stat_value': 126},
            {'opponent_team_id': 1610612760, 'stat_key': 'Penalty Free Throw Trips', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'Personal Block Fouls', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'Personal Fouls', 'stat_value': 7},
            {'opponent_team_id': 1610612760, 'stat_key': 'Personal Fouls Drawn', 'stat_value': 7},
            {'opponent_team_id': 1610612760, 'stat_key': 'Personal Take Fouls', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'Personal Take Fouls Drawn', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'PlusMinus', 'stat_value': -11},
            {'opponent_team_id': 1610612760, 'stat_key': 'Putbacks', 'stat_value': 3},
            {'opponent_team_id': 1610612760, 'stat_key': 'SecondsPlayedDef', 'stat_value': 1544},
            {'opponent_team_id': 1610612760, 'stat_key': 'SecondsPlayedOff', 'stat_value': 1636},
            {'opponent_team_id': 1610612760, 'stat_key': 'Shooting Block Fouls', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'Shooting Fouls', 'stat_value': 11},
            {'opponent_team_id': 1610612760, 'stat_key': 'Shooting Fouls Drawn', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeAssists', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeBlocked', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeBlockedOffReboundOpportunities', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeBlockedOffReboundedOpportunities', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeDefReboundOpportunities', 'stat_value': 6},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeDefRebounds', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeOffReboundOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeOffRebounded', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeOffReboundedOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeOffRebounds', 'stat_value': 4},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShortMidRangeSelfOReb', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'ShotClockViolations', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'Technical Free Throw Trips', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'Total2ptShotDistance', 'stat_value': 442.3},
            {'opponent_team_id': 1610612760, 'stat_key': 'Total2ptShotsWithDistance', 'stat_value': 70},
            {'opponent_team_id': 1610612760, 'stat_key': 'Total3ptShotDistance', 'stat_value': 697.3},
            {'opponent_team_id': 1610612760, 'stat_key': 'Total3ptShotsWithDistance', 'stat_value': 28},
            {'opponent_team_id': 1610612760, 'stat_key': 'UnassistedArc3', 'stat_value': 2},
            {'opponent_team_id': 1610612760, 'stat_key': 'UnassistedAtRim', 'stat_value': 10},
            {'opponent_team_id': 1610612760, 'stat_key': 'UnassistedLongMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612760, 'stat_key': 'UnassistedShortMidRange', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': '1627734:AssistsTo:201566:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '1627734:AssistsTo:203506:LongMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:1627734:AtRim', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:202683:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:202683:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:203460:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:203460:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:203500:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:203506:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201566:AssistsTo:203530:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201627:AssistsTo:202683:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201627:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201627:AssistsTo:203530:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '201627:AssistsTo:203924:Corner3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203506:AssistsTo:1627734:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203506:AssistsTo:1627734:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203506:AssistsTo:201566:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203506:AssistsTo:201566:ShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203506:AssistsTo:203460:Corner3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203506:AssistsTo:203500:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203530:AssistsTo:201627:Corner3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203902:AssistsTo:201627:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203902:AssistsTo:202683:AtRim', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203902:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '203924:AssistsTo:203506:Arc3', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': '2pt And 1 Free Throw Trips', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': '2pt Shooting Foul Free Throw Trips', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3Assists', 'stat_value': 7},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3DefReboundOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3DefRebounds', 'stat_value': 10},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3OffReboundOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3OffRebounded', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3OffReboundedOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612764, 'stat_key': 'Arc3OffRebounds', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'AssistedArc3', 'stat_value': 7},
            {'opponent_team_id': 1610612764, 'stat_key': 'AssistedAtRim', 'stat_value': 14},
            {'opponent_team_id': 1610612764, 'stat_key': 'AssistedCorner3', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AssistedLongMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'AssistedShortMidRange', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimAssists', 'stat_value': 14},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlocked', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlockedDefReboundOpportunities', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlockedDefRebounds', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlockedOffReboundOpportunities', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlockedOffRebounded', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlockedOffReboundedOpportunities', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimBlockedOffRebounds', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimDefReboundOpportunities', 'stat_value': 10},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimDefRebounds', 'stat_value': 8},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimOffReboundOpportunities', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimOffRebounded', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimOffReboundedOpportunities', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimOffRebounds', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'AtRimSelfOReb', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'BadPassOutOfBoundsTurnovers', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'BadPassSteals', 'stat_value': 8},
            {'opponent_team_id': 1610612764, 'stat_key': 'BadPassTurnovers', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'BlockedAtRim', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'BlockedAtRimRecovered', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'BlockedShortMidRange', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'BlockedShortMidRangeRecovered', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3Assists', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3DefReboundOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3DefRebounds', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3OffReboundOpportunities', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3OffRebounded', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3OffReboundedOpportunities', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'Corner3OffRebounds', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'DeadBallTurnovers', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'DefPoss', 'stat_value': 108},
            {'opponent_team_id': 1610612764, 'stat_key': 'DefensiveGoaltends', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'FTDefReboundOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'FTDefRebounds', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'FTOffReboundOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'FTOffRebounded', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'FTOffReboundedOpportunities', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'FTOffRebounds', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'FtsMade', 'stat_value': 22},
            {'opponent_team_id': 1610612764, 'stat_key': 'FtsMissed', 'stat_value': 9},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeAssists', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeDefReboundOpportunities', 'stat_value': 9},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeDefRebounds', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeOffReboundOpportunities', 'stat_value': 10},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeOffRebounded', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeOffReboundedOpportunities', 'stat_value': 10},
            {'opponent_team_id': 1610612764, 'stat_key': 'LongMidRangeOffRebounds', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'Loose Ball Fouls', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'Loose Ball Fouls Drawn', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'LostBallOutOfBoundsTurnovers', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'LostBallSteals', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'LostBallTurnovers', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'MissedArc3', 'stat_value': 12},
            {'opponent_team_id': 1610612764, 'stat_key': 'MissedAtRim', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'MissedCorner3', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'MissedLongMidRange', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'MissedShortMidRange', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'OffPoss', 'stat_value': 109},
            {'opponent_team_id': 1610612764, 'stat_key': 'OnFloorOffReb', 'stat_value': 65},
            {'opponent_team_id': 1610612764, 'stat_key': 'OpponentPoints', 'stat_value': 115},
            {'opponent_team_id': 1610612764, 'stat_key': 'Penalty Free Throw Trips', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'Personal Block Fouls Drawn', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'Personal Fouls', 'stat_value': 7},
            {'opponent_team_id': 1610612764, 'stat_key': 'Personal Fouls Drawn', 'stat_value': 7},
            {'opponent_team_id': 1610612764, 'stat_key': 'Personal Take Fouls', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'Personal Take Fouls Drawn', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'PlusMinus', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'Putbacks', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'SecondsPlayedDef', 'stat_value': 1636},
            {'opponent_team_id': 1610612764, 'stat_key': 'SecondsPlayedOff', 'stat_value': 1544},
            {'opponent_team_id': 1610612764, 'stat_key': 'Shooting Block Fouls Drawn', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'Shooting Fouls', 'stat_value': 12},
            {'opponent_team_id': 1610612764, 'stat_key': 'Shooting Fouls Drawn', 'stat_value': 11},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeAssists', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeBlockedDefReboundOpportunities', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeBlockedDefRebounds', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeDefReboundOpportunities', 'stat_value': 12},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeDefRebounds', 'stat_value': 8},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeOffReboundOpportunities', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeOffRebounded', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeOffReboundedOpportunities', 'stat_value': 6},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShortMidRangeOffRebounds', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'ShotClockViolations', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'Technical Free Throw Trips', 'stat_value': 1},
            {'opponent_team_id': 1610612764, 'stat_key': 'Total2ptShotDistance', 'stat_value': 428.5},
            {'opponent_team_id': 1610612764, 'stat_key': 'Total2ptShotsWithDistance', 'stat_value': 65},
            {'opponent_team_id': 1610612764, 'stat_key': 'Total3ptShotDistance', 'stat_value': 728.0},
            {'opponent_team_id': 1610612764, 'stat_key': 'Total3ptShotsWithDistance', 'stat_value': 30},
            {'opponent_team_id': 1610612764, 'stat_key': 'Travels', 'stat_value': 3},
            {'opponent_team_id': 1610612764, 'stat_key': 'UnassistedArc3', 'stat_value': 2},
            {'opponent_team_id': 1610612764, 'stat_key': 'UnassistedAtRim', 'stat_value': 9},
            {'opponent_team_id': 1610612764, 'stat_key': 'UnassistedLongMidRange', 'stat_value': 4},
            {'opponent_team_id': 1610612764, 'stat_key': 'UnassistedShortMidRange', 'stat_value': 3},
        ]

    def test_player_stats(self):
        results = self.game.possessions.player_stats
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'OffPoss', 'stat_value': 87} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'DefPoss', 'stat_value': 88} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'SecondsPlayedDef', 'stat_value': 1288.0} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'SecondsPlayedOff', 'stat_value': 1179.0} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'PlusMinus', 'stat_value': 4} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'FtsMade', 'stat_value': 10} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AssistedAtRim', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AssistedShortMidRange', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'UnassistedArc3', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'UnassistedAtRim', 'stat_value': 4} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'UnassistedLongMidRange', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'UnassistedShortMidRange', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'MissedArc3', 'stat_value': 4} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'MissedAtRim', 'stat_value': 8} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'MissedCorner3', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'MissedLongMidRange', 'stat_value': 6} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'MissedShortMidRange', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimBlocked', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Putbacks', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Total2ptShotDistance', 'stat_value': 225.0} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Total2ptShotsWithDistance', 'stat_value': 29} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Total3ptShotDistance', 'stat_value': 148.3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Total3ptShotsWithDistance', 'stat_value': 6} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Arc3Assists', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimAssists', 'stat_value': 7} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeAssists', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': '2pt And 1 Free Throw Trips', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': '2pt Shooting Foul Free Throw Trips', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Penalty Free Throw Trips', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Technical Free Throw Trips', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Personal Block Fouls Drawn', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Personal Fouls Drawn', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Personal Fouls', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Personal Take Fouls Drawn', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Personal Take Fouls', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Shooting Block Fouls Drawn', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Shooting Fouls Drawn', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'DeadBallTurnovers', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LostBallTurnovers', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'BadPassTurnovers', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LostBallSteals', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'BadPassSteals', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffRebounded', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffReboundedOpportunities', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LongMidRangeOffRebounded', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LongMidRangeOffReboundedOpportunities', 'stat_value': 6} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Corner3DefReboundOpportunities', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Corner3OffReboundedOpportunities', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimOffRebounded', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimOffReboundedOpportunities', 'stat_value': 8} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffRebounded', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffReboundedOpportunities', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Arc3OffReboundedOpportunities', 'stat_value': 4} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Arc3DefReboundOpportunities', 'stat_value': 10} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Arc3DefRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Arc3OffReboundOpportunities', 'stat_value': 9} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Arc3OffRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimBlockedDefReboundOpportunities', 'stat_value': 2} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimBlockedDefRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimBlockedOffReboundOpportunities', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimDefReboundOpportunities', 'stat_value': 8} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimDefRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimOffReboundOpportunities', 'stat_value': 9} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'AtRimOffRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'Corner3OffReboundOpportunities', 'stat_value': 6} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'FTDefReboundOpportunities', 'stat_value': 4} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'FTDefRebounds', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'FTOffReboundOpportunities', 'stat_value': 4} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'FTOffRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LongMidRangeDefReboundOpportunities', 'stat_value': 7} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LongMidRangeDefRebounds', 'stat_value': 3} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LongMidRangeOffReboundOpportunities', 'stat_value': 9} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'LongMidRangeOffRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeBlockedDefReboundOpportunities', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeDefReboundOpportunities', 'stat_value': 5} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeDefRebounds', 'stat_value': 1} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'ShortMidRangeOffReboundOpportunities', 'stat_value': 5} in results
        assert {'player_id': 201566, 'team_id': 1610612760, 'stat_key': 'OnFloorOffReb', 'stat_value': 12} in results

    def test_lineup_stats(self):
        results = self.game.possessions.lineup_stats
        assert {'lineup_id': '1627734-201566-203460-203500-203506', 'team_id': 1610612760, 'stat_key': 'OffPoss', 'stat_value': 19} in results
        assert {'lineup_id': '1627734-201566-203460-203500-203506', 'team_id': 1610612760, 'stat_key': 'DefPoss', 'stat_value': 19} in results
        assert {'lineup_id': '1627734-201566-203460-203500-203506', 'team_id': 1610612760, 'stat_key': 'SecondsPlayedDef', 'stat_value': 358} in results
        assert {'lineup_id': '1627734-201566-203460-203500-203506', 'team_id': 1610612760, 'stat_key': 'SecondsPlayedOff', 'stat_value': 313} in results
        assert {'lineup_id': '1627734-201566-203460-203500-203506', 'team_id': 1610612760, 'stat_key': 'PlusMinus', 'stat_value': 4} in results

    def test_lineup_opponent_stats(self):
        results = self.game.possessions.lineup_opponent_stats
        assert {'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'opponent_team_id': 1610612760, 'stat_key': 'OffPoss', 'stat_value': 19} in results
        assert {'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'opponent_team_id': 1610612760, 'stat_key': 'DefPoss', 'stat_value': 19} in results
        assert {'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'opponent_team_id': 1610612760, 'stat_key': 'SecondsPlayedDef', 'stat_value': 313} in results
        assert {'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'opponent_team_id': 1610612760, 'stat_key': 'SecondsPlayedOff', 'stat_value': 358} in results
        assert {'opponent_lineup_id': '1627734-201566-203460-203500-203506', 'opponent_team_id': 1610612760, 'stat_key': 'PlusMinus', 'stat_value': -4} in results
