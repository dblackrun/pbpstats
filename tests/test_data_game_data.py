import json

import responses
import pbpstats
from pbpstats.data_game_data import DataGameData


class TestDataGameData:
    @responses.activate
    def setup_class(cls):
        cls.GameId = '0021600270'
        with open('tests/data/data_game_pbp_response.json') as f:
            game_pbp_response = json.loads(f.read())

        with open('tests/data/data_game_summary_response.json') as f:
            game_summary_response = json.loads(f.read())

        game_summary_url = f'http://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/gamedetail/{cls.GameId}_gamedetail.json'
        pbp_url = f'http://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/pbp/{cls.GameId}_full_pbp.json'

        responses.add(responses.GET, pbp_url, json=game_pbp_response, status=200)
        responses.add(responses.GET, game_summary_url, json=game_summary_response, status=200)

        with open('tests/data/missing_period_starters.json') as f:
            period_starters_override = json.loads(f.read())

        cls.GameData = DataGameData(cls.GameId, response_data_directory=None)
        cls.GameData.get_game_data(period_starters_override=period_starters_override)

    def test_season_is_set(self):
        assert self.GameData.Season == '2016-17'
        assert self.GameData.SeasonType == pbpstats.REGULAR_SEASON_STRING

    def test_periods_are_set(self):
        assert len(self.GameData.Periods) == 5  # overtime game, should have 5 periods
        assert self.GameData.Periods[0].Number == 1  # make sure first period is at index 0
        assert len(self.GameData.Periods[0].Events) > 0  # make sure there are pbp events for period

    def test_basic_game_info_is_set(self):
        assert self.GameData.GameDate == '2016-11-30'
        assert self.GameData.HomeTeamId == '1610612760'
        assert self.GameData.VisitorTeamId == '1610612764'
        assert self.GameData.HomeTeamAbbreviation == 'OKC'
        assert self.GameData.VisitorTeamAbbreviation == 'WAS'
        assert self.GameData.Players['1610612760'] == {'203460': 'Andre Roberson', '1627734': 'Domantas Sabonis', '203500': 'Steven Adams', '203506': 'Victor Oladipo', '201566': 'Russell Westbrook', '203530': 'Joffrey Lauvergne', '201627': 'Anthony Morrow', '203902': 'Semaj Christon', '202683': 'Enes Kanter', '203924': 'Jerami Grant'}
        assert self.GameData.Players['1610612764'] == {'202693': 'Markieff Morris', '203490': 'Otto Porter Jr.', '101162': 'Marcin Gortat', '203078': 'Bradley Beal', '202322': 'John Wall', '201160': 'Jason Smith', '203107': 'Tomas Satoransky', '201977': 'Marcus Thornton', '1626162': 'Kelly Oubre Jr.'}

    def test_period_starters(self):
        assert sorted(self.GameData.Periods[0].Starters['1610612760']) == sorted(['203500', '1627734', '203506', '201566', '203460'])
        assert sorted(self.GameData.Periods[0].Starters['1610612764']) == sorted(['202693', '202322', '101162', '203078', '203490'])
        assert sorted(self.GameData.Periods[1].Starters['1610612760']) == sorted(['201627', '203530', '203506', '203902', '202683'])
        assert sorted(self.GameData.Periods[1].Starters['1610612764']) == sorted(['1626162', '202693', '201160', '201977', '203107'])
        assert sorted(self.GameData.Periods[2].Starters['1610612760']) == sorted(['203500', '1627734', '203506', '201566', '203460'])
        assert sorted(self.GameData.Periods[2].Starters['1610612764']) == sorted(['202693', '202322', '101162', '203078', '203490'])
        assert sorted(self.GameData.Periods[3].Starters['1610612760']) == sorted(['201627', '203530', '203506', '203902', '202683'])
        assert sorted(self.GameData.Periods[3].Starters['1610612764']) == sorted(['1626162', '203490', '201160', '201977', '203107'])
        assert sorted(self.GameData.Periods[4].Starters['1610612760']) == sorted(['203924', '203506', '201566', '201627', '203460'])
        assert sorted(self.GameData.Periods[4].Starters['1610612764']) == sorted(['202693', '203078', '202322', '1626162', '203490'])

    def test_subs_change_current_players(self):
        # outgoing player
        assert '1627734' in self.GameData.Periods[0].Events[37].current_players['1610612760']  # event before sub, player should be in
        assert '1627734' not in self.GameData.Periods[0].Events[38].current_players['1610612760']  # sub event, player should be out
        # incoming player
        assert '203530' not in self.GameData.Periods[0].Events[37].current_players['1610612760']  # event before sub, player should be out
        assert '203530' in self.GameData.Periods[0].Events[38].current_players['1610612760']  # sub event, player should be in

    def test_number_of_possessions(self):
        assert len(self.GameData.Periods[0].Possessions) == 53
        assert len(self.GameData.Periods[1].Possessions) == 54
        assert len(self.GameData.Periods[2].Possessions) == 44
        assert len(self.GameData.Periods[3].Possessions) == 47
        assert len(self.GameData.Periods[4].Possessions) == 22

    def test_first_possession(self):
        o_player_stats_dict = self.GameData.Periods[0].Possessions[0].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']
        d_player_stats_dict = self.GameData.Periods[0].Possessions[0].PlayerStats['1610612760']['1627734-201566-203460-203500-203506']['101162-202322-202693-203078-203490']
        assert o_player_stats_dict['101162'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['202322'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['202693'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'UnassistedShortMidRange': 1, 'Total2ptShotDistance': 12.1, 'Total2ptShotsWithDistance': 1, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['203078'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['203490'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert d_player_stats_dict['1627734'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['201566'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['203460'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['203500'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['203506'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}

        expected_shot_data = [
            {
                'PlayerId': '202693',
                'TeamId': '1610612764',
                'OpponentTeamId': '1610612760',
                'LineupId': '101162-202322-202693-203078-203490',
                'OpponentLineupId': '1627734-201566-203460-203500-203506',
                'Made': True,
                'X': -19,
                'Y': 120,
                'Time': 699,
                'ShotValue': 2,
                'Assisted': False,
                'Putback': False,
                'ShotType': 'ShortMidRange',
                'ScoreMargin': 0
            }
        ]
        assert self.GameData.Periods[0].Possessions[0].ShotData == expected_shot_data
        assert self.GameData.Periods[0].Possessions[0].GameId == self.GameId
        assert self.GameData.Periods[0].Possessions[0].Period == 1
        assert self.GameData.Periods[0].Possessions[0].PossessionNumber == 1
        assert self.GameData.Periods[0].Possessions[0].OffenseTeamId == '1610612764'
        assert self.GameData.Periods[0].Possessions[0].DefenseTeamId == '1610612760'
        assert self.GameData.Periods[0].Possessions[0].StartTime == 720
        assert self.GameData.Periods[0].Possessions[0].EndTime == 699
        assert self.GameData.Periods[0].Possessions[0].PreviousPossessionEndEventNum == 0
        assert self.GameData.Periods[0].Possessions[0].EndEventNum == 2
        assert self.GameData.Periods[0].Possessions[0].StartScoreDifferential == 0
        assert len(self.GameData.Periods[0].Possessions[0].Events) == 3
        assert len(self.GameData.Periods[0].Possessions[0].PreviousPossessionEvents) == 0
        assert self.GameData.Periods[0].Possessions[0].OffensiveRebounds == 0
        assert self.GameData.Periods[0].Possessions[0].SecondChanceTime == 0
        assert self.GameData.Periods[0].Possessions[0].StartType == pbpstats.OFF_DEADBALL_STRING
        assert self.GameData.Periods[0].Possessions[0].PreviousPossessionEndShooterPlayerId == 0
        assert self.GameData.Periods[0].Possessions[0].PreviousPossessionEndReboundPlayerId == 0
        assert self.GameData.Periods[0].Possessions[0].PreviousPossessionEndTurnoverPlayerId == 0
        assert self.GameData.Periods[0].Possessions[0].PreviousPossessionEndStealPlayerId == 0

    def test_second_possession(self):
        o_player_stats_dict = self.GameData.Periods[0].Possessions[1].PlayerStats['1610612760']['1627734-201566-203460-203500-203506']['101162-202322-202693-203078-203490']
        d_player_stats_dict = self.GameData.Periods[0].Possessions[1].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']
        assert o_player_stats_dict['1627734'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'AssistedShortMidRange': 1, 'Total2ptShotDistance': 12.9, 'Total2ptShotsWithDistance': 1, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['201566'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['203460'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['203500'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'PlusMinus': 2, 'OffPoss': 1}
        assert o_player_stats_dict['203506'] == {'SecondsPlayedOff': 21, 'Period1Fouls0SecondsPlayedOff': 21, 'ShortMidRangeAssists': 1, '203506:AssistsTo:1627734:ShortMidRange': 1, 'PlusMinus': 2, 'OffPoss': 1}
        assert d_player_stats_dict['101162'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['202322'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['202693'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['203078'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}
        assert d_player_stats_dict['203490'] == {'SecondsPlayedDef': 21, 'Period1Fouls0SecondsPlayedDef': 21, 'PlusMinus': -2, 'OpponentPoints': 2, 'DefPoss': 1}

        expected_shot_data = [
            {
                'PlayerId': '1627734',
                'TeamId': '1610612760',
                'OpponentTeamId': '1610612764',
                'LineupId': '1627734-201566-203460-203500-203506',
                'OpponentLineupId': '101162-202322-202693-203078-203490',
                'Made': True,
                'X': -120,
                'Y': 46,
                'Time': 678,
                'ShotValue': 2,
                'Assisted': True,
                'Putback': False,
                'AssistPlayerId': '203506',
                'ShotType': 'ShortMidRange',
                'ScoreMargin': -2
            }
        ]
        assert self.GameData.Periods[0].Possessions[1].ShotData == expected_shot_data
        assert self.GameData.Periods[0].Possessions[1].GameId == self.GameId
        assert self.GameData.Periods[0].Possessions[1].Period == 1
        assert self.GameData.Periods[0].Possessions[1].PossessionNumber == 2
        assert self.GameData.Periods[0].Possessions[1].OffenseTeamId == '1610612760'
        assert self.GameData.Periods[0].Possessions[1].DefenseTeamId == '1610612764'
        assert self.GameData.Periods[0].Possessions[1].StartTime == 699
        assert self.GameData.Periods[0].Possessions[1].EndTime == 678
        assert self.GameData.Periods[0].Possessions[1].PreviousPossessionEndEventNum == 2
        assert self.GameData.Periods[0].Possessions[1].EndEventNum == 3
        assert self.GameData.Periods[0].Possessions[1].StartScoreDifferential == -2
        assert len(self.GameData.Periods[0].Possessions[1].Events) == 1
        assert len(self.GameData.Periods[0].Possessions[1].PreviousPossessionEvents) == 3
        assert self.GameData.Periods[0].Possessions[1].OffensiveRebounds == 0
        assert self.GameData.Periods[0].Possessions[1].SecondChanceTime == 0
        assert self.GameData.Periods[0].Possessions[1].StartType == f'Off{pbpstats.SHORT_MID_RANGE_STRING}{pbpstats.MAKE_STRING}'
        assert self.GameData.Periods[0].Possessions[1].PreviousPossessionEndShooterPlayerId == '202693'
        assert self.GameData.Periods[0].Possessions[1].PreviousPossessionEndReboundPlayerId == 0
        assert self.GameData.Periods[0].Possessions[1].PreviousPossessionEndTurnoverPlayerId == 0
        assert self.GameData.Periods[0].Possessions[1].PreviousPossessionEndStealPlayerId == 0

    def test_possession_with_second_chance(self):
        expected_shot_data = [
            {
                'PlayerId': '201566',
                'TeamId': '1610612760',
                'OpponentTeamId': '1610612764',
                'LineupId': '1627734-201566-203460-203500-203506',
                'OpponentLineupId': '101162-202322-202693-203078-203490',
                'Made': False,
                'X': 1,
                'Y': 21,
                'Time': 651.0,
                'ShotValue': 2,
                'Blocked': False,
                'Putback': False,
                'ShotType': 'AtRim',
                'ScoreMargin': 0
            },
            {
                'PlayerId': '203500',
                'TeamId': '1610612760',
                'OpponentTeamId': '1610612764',
                'LineupId': '1627734-201566-203460-203500-203506',
                'OpponentLineupId': '101162-202322-202693-203078-203490',
                'Made': False,
                'X': 27,
                'Y': 57,
                'Time': 644.0,
                'ShotValue': 2,
                'SecondsSinceOReb': 6.0,
                'OrebShotPlayerId': '201566',
                'OrebReboundPlayerId': None,
                'OrebShotType': 'Team',
                'Blocked': False,
                'Putback': False,
                'ShotType': 'ShortMidRange',
                'ScoreMargin': 0
            }
        ]
        assert self.GameData.Periods[0].Possessions[3].ShotData == expected_shot_data

        o_player_stats_dict = self.GameData.Periods[0].Possessions[3].PlayerStats['1610612760']['1627734-201566-203460-203500-203506']['101162-202322-202693-203078-203490']
        d_player_stats_dict = self.GameData.Periods[0].Possessions[3].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']

        assert o_player_stats_dict['1627734'] == {'SecondsPlayedOff': 16, 'Period1Fouls0SecondsPlayedOff': 16, 'SecondChanceSecondsPlayedOff': 6.0, 'AtRimOffReboundOpportunities': 1, 'OnFloorOffReb': 1, 'ShortMidRangeOffReboundOpportunities': 1, 'OffPoss': 1, 'SecondChanceOffPoss': 1}
        assert o_player_stats_dict['201566'] == {'SecondsPlayedOff': 16, 'Period1Fouls0SecondsPlayedOff': 16, 'MissedAtRim': 1, 'Total2ptShotDistance': 2.1, 'Total2ptShotsWithDistance': 1, 'SecondChanceSecondsPlayedOff': 6.0, 'AtRimOffReboundOpportunities': 1, 'OnFloorOffReb': 1, 'AtRimOffRebounded': 1, 'AtRimOffReboundedOpportunities': 1, 'ShortMidRangeOffReboundOpportunities': 1, 'OffPoss': 1, 'SecondChanceOffPoss': 1}
        assert o_player_stats_dict['203460'] == {'SecondsPlayedOff': 16, 'Period1Fouls0SecondsPlayedOff': 16, 'SecondChanceSecondsPlayedOff': 6.0, 'AtRimOffReboundOpportunities': 1, 'OnFloorOffReb': 1, 'ShortMidRangeOffReboundOpportunities': 1, 'OffPoss': 1, 'SecondChanceOffPoss': 1}
        assert o_player_stats_dict['203500'] == {'SecondsPlayedOff': 16, 'Period1Fouls0SecondsPlayedOff': 16, 'SecondChanceSecondsPlayedOff': 6.0, 'AtRimOffReboundOpportunities': 1, 'OnFloorOffReb': 1, 'MissedShortMidRange': 1, 'Total2ptShotDistance': 6.3, 'Total2ptShotsWithDistance': 1, 'SecondChanceMissedShortMidRange': 1, 'ShortMidRangeOffReboundOpportunities': 1, 'ShortMidRangeOffReboundedOpportunities': 1, 'OffPoss': 1, 'SecondChanceOffPoss': 1}
        assert o_player_stats_dict['203506'] == {'SecondsPlayedOff': 16, 'Period1Fouls0SecondsPlayedOff': 16, 'SecondChanceSecondsPlayedOff': 6.0, 'AtRimOffReboundOpportunities': 1, 'OnFloorOffReb': 1, 'ShortMidRangeOffReboundOpportunities': 1, 'OffPoss': 1, 'SecondChanceOffPoss': 1}
        assert o_player_stats_dict['0'] == {'AtRimOffRebounds': 1}
        assert d_player_stats_dict['101162'] == {'SecondsPlayedDef': 16, 'Period1Fouls0SecondsPlayedDef': 16, 'SecondChanceSecondsPlayedDef': 6.0, 'AtRimDefReboundOpportunities': 1, 'ShortMidRangeDefRebounds': 1, 'ShortMidRangeDefReboundOpportunities': 1, 'DefPoss': 1, 'SecondChanceDefPoss': 1}
        assert d_player_stats_dict['202322'] == {'SecondsPlayedDef': 16, 'Period1Fouls0SecondsPlayedDef': 16, 'SecondChanceSecondsPlayedDef': 6.0, 'AtRimDefReboundOpportunities': 1, 'ShortMidRangeDefReboundOpportunities': 1, 'DefPoss': 1, 'SecondChanceDefPoss': 1}
        assert d_player_stats_dict['202693'] == {'SecondsPlayedDef': 16, 'Period1Fouls0SecondsPlayedDef': 16, 'SecondChanceSecondsPlayedDef': 6.0, 'AtRimDefReboundOpportunities': 1, 'ShortMidRangeDefReboundOpportunities': 1, 'DefPoss': 1, 'SecondChanceDefPoss': 1}
        assert d_player_stats_dict['203078'] == {'SecondsPlayedDef': 16, 'Period1Fouls0SecondsPlayedDef': 16, 'SecondChanceSecondsPlayedDef': 6.0, 'AtRimDefReboundOpportunities': 1, 'ShortMidRangeDefReboundOpportunities': 1, 'DefPoss': 1, 'SecondChanceDefPoss': 1}
        assert d_player_stats_dict['203490'] == {'SecondsPlayedDef': 16, 'Period1Fouls0SecondsPlayedDef': 16, 'SecondChanceSecondsPlayedDef': 6.0, 'AtRimDefReboundOpportunities': 1, 'ShortMidRangeDefReboundOpportunities': 1, 'DefPoss': 1, 'SecondChanceDefPoss': 1}
        assert self.GameData.Periods[0].Possessions[3].ShotData == expected_shot_data
        assert self.GameData.Periods[0].Possessions[3].GameId == self.GameId
        assert self.GameData.Periods[0].Possessions[3].Period == 1
        assert self.GameData.Periods[0].Possessions[3].PossessionNumber == 4
        assert self.GameData.Periods[0].Possessions[3].OffenseTeamId == '1610612760'
        assert self.GameData.Periods[0].Possessions[3].DefenseTeamId == '1610612764'
        assert self.GameData.Periods[0].Possessions[3].StartTime == 660
        assert self.GameData.Periods[0].Possessions[3].EndTime == 644
        assert self.GameData.Periods[0].Possessions[3].PreviousPossessionEndEventNum == 5
        assert self.GameData.Periods[0].Possessions[3].EndEventNum == 11
        assert self.GameData.Periods[0].Possessions[3].StartScoreDifferential == 0
        assert len(self.GameData.Periods[0].Possessions[3].Events) == 4
        assert len(self.GameData.Periods[0].Possessions[3].PreviousPossessionEvents) == 2
        assert self.GameData.Periods[0].Possessions[3].OffensiveRebounds == 1
        assert self.GameData.Periods[0].Possessions[3].SecondChanceTime == 6
        assert self.GameData.Periods[0].Possessions[3].StartType == f'Off{pbpstats.ARC_3_STRING}{pbpstats.MISS_STRING}'
        assert self.GameData.Periods[0].Possessions[3].PreviousPossessionEndShooterPlayerId == '202322'
        assert self.GameData.Periods[0].Possessions[3].PreviousPossessionEndReboundPlayerId == '1627734'
        assert self.GameData.Periods[0].Possessions[3].PreviousPossessionEndTurnoverPlayerId == 0
        assert self.GameData.Periods[0].Possessions[3].PreviousPossessionEndStealPlayerId == 0

    def test_last_possession_does_not_count_as_possession(self):
        o_player_stats_dict = self.GameData.Periods[1].Possessions[-1].PlayerStats['1610612764']['101162-1626162-202322-203078-203107']['201566-201627-203500-203506-203924']
        d_player_stats_dict = self.GameData.Periods[1].Possessions[-1].PlayerStats['1610612760']['201566-201627-203500-203506-203924']['101162-1626162-202322-203078-203107']
        assert o_player_stats_dict['101162'] == {'SecondsPlayedOff': 1.9, 'Period2Fouls2SecondsPlayedOff': 1.9, 'PenaltySecondsPlayedOff': 1.9}
        assert o_player_stats_dict['1626162'] == {'SecondsPlayedOff': 1.9, 'Period2Fouls1SecondsPlayedOff': 1.9, 'PenaltySecondsPlayedOff': 1.9}
        assert o_player_stats_dict['202322'] == {'SecondsPlayedOff': 1.9, 'Period2Fouls0SecondsPlayedOff': 1.9, 'PenaltySecondsPlayedOff': 1.9}
        assert o_player_stats_dict['203078'] == {'SecondsPlayedOff': 1.9, 'Period2Fouls1SecondsPlayedOff': 1.9, 'PenaltySecondsPlayedOff': 1.9}
        assert o_player_stats_dict['203107'] == {'SecondsPlayedOff': 1.9, 'Period2Fouls1SecondsPlayedOff': 1.9, 'PenaltySecondsPlayedOff': 1.9}
        assert d_player_stats_dict['201566'] == {'SecondsPlayedDef': 1.9, 'Period2Fouls2SecondsPlayedDef': 1.9, 'PenaltySecondsPlayedDef': 1.9}
        assert d_player_stats_dict['201627'] == {'SecondsPlayedDef': 1.9, 'Period2Fouls0SecondsPlayedDef': 1.9, 'PenaltySecondsPlayedDef': 1.9}
        assert d_player_stats_dict['203500'] == {'SecondsPlayedDef': 1.9, 'Period2Fouls1SecondsPlayedDef': 1.9, 'PenaltySecondsPlayedDef': 1.9}
        assert d_player_stats_dict['203506'] == {'SecondsPlayedDef': 1.9, 'Period2Fouls1SecondsPlayedDef': 1.9, 'PenaltySecondsPlayedDef': 1.9}
        assert d_player_stats_dict['203924'] == {'SecondsPlayedDef': 1.9, 'Period2Fouls2SecondsPlayedDef': 1.9, 'PenaltySecondsPlayedDef': 1.9}
        assert self.GameData.Periods[1].Possessions[-1].ShotData == []
        assert self.GameData.Periods[1].Possessions[-1].GameId == self.GameId
        assert self.GameData.Periods[1].Possessions[-1].Period == 2
        assert self.GameData.Periods[1].Possessions[-1].PossessionNumber == 54
        assert self.GameData.Periods[1].Possessions[-1].OffenseTeamId == '1610612764'
        assert self.GameData.Periods[1].Possessions[-1].DefenseTeamId == '1610612760'
        assert self.GameData.Periods[1].Possessions[-1].StartTime == 1.9
        assert self.GameData.Periods[1].Possessions[-1].EndTime == 0
        assert self.GameData.Periods[1].Possessions[-1].PreviousPossessionEndEventNum == 273
        assert self.GameData.Periods[1].Possessions[-1].EndEventNum == 274
        assert self.GameData.Periods[1].Possessions[-1].StartScoreDifferential == -7
        assert len(self.GameData.Periods[1].Possessions[-1].Events) == 1
        assert len(self.GameData.Periods[1].Possessions[-1].PreviousPossessionEvents) == 3
        assert self.GameData.Periods[1].Possessions[-1].OffensiveRebounds == 0
        assert self.GameData.Periods[1].Possessions[-1].SecondChanceTime == 0
        assert self.GameData.Periods[1].Possessions[-1].StartType == f'Off{pbpstats.AT_RIM_STRING}{pbpstats.MAKE_STRING}'
        assert self.GameData.Periods[1].Possessions[-1].PreviousPossessionEndShooterPlayerId == '201566'
        assert self.GameData.Periods[1].Possessions[-1].PreviousPossessionEndReboundPlayerId == 0
        assert self.GameData.Periods[1].Possessions[-1].PreviousPossessionEndTurnoverPlayerId == 0
        assert self.GameData.Periods[1].Possessions[-1].PreviousPossessionEndStealPlayerId == 0

    def test_number_of_fouls_time_split_up(self):
        assert self.GameData.Periods[0].Possessions[11].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']['101162'][f'Period1Fouls0{pbpstats.SECONDS_PLAYED_DEFENSE_STRING}'] == 7
        assert self.GameData.Periods[0].Possessions[11].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']['101162'][f'Period1Fouls1{pbpstats.SECONDS_PLAYED_DEFENSE_STRING}'] == 7
        assert self.GameData.Periods[0].Possessions[11].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']['101162'][pbpstats.SECONDS_PLAYED_DEFENSE_STRING] == 14

    def test_off_steal_possession(self):
        assert self.GameData.Periods[0].Possessions[5].StartType == pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
        assert self.GameData.Periods[0].Possessions[5].PreviousPossessionEndStealPlayerId == '1627734'
        assert self.GameData.Periods[0].Possessions[5].PreviousPossessionEndTurnoverPlayerId == '202693'

    def test_shooting_foul_player_stats(self):
        assert self.GameData.Periods[0].Possessions[6].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']['203078'][pbpstats.SHOOTING_FOUL_TYPE_STRING + pbpstats.FOULS_DRAWN_TYPE_STRING] == 1
        assert self.GameData.Periods[0].Possessions[6].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']['203078']['2pt Shooting Foul Free Throw Trips'] == 1
        assert self.GameData.Periods[0].Possessions[6].PlayerStats['1610612764']['101162-202322-202693-203078-203490']['1627734-201566-203460-203500-203506']['203078'][pbpstats.FTS_MADE_STRING] == 1
        assert self.GameData.Periods[0].Possessions[6].PlayerStats['1610612760']['1627734-201566-203460-203500-203506']['101162-202322-202693-203078-203490']['203500'][pbpstats.SHOOTING_FOUL_TYPE_STRING] == 1

    def test_personal_take_foul_in_penalty(self):
        assert self.GameData.Periods[-1].Possessions[-2].PlayerStats['1610612760']['201566-203460-203506-203902-203924']['101162-202322-202693-203078-203490']['201566'][pbpstats.PENALTY_STRING + pbpstats.OFFENSIVE_POSSESSION_STRING] == 1
        assert self.GameData.Periods[-1].Possessions[-2].PlayerStats['1610612760']['201566-203460-203506-203902-203924']['101162-202322-202693-203078-203490']['201566'][pbpstats.PENALTY_STRING + pbpstats.FTS_MADE_STRING] == 2
        assert self.GameData.Periods[-1].Possessions[-2].PlayerStats['1610612760']['201566-203460-203506-203902-203924']['101162-202322-202693-203078-203490']['201566'][pbpstats.FINAL_MINUTE_PENALTY_TAKE_FOUL_STRING + pbpstats.OFFENSIVE_POSSESSION_STRING] == 1
        assert self.GameData.Periods[-1].Possessions[-2].PlayerStats['1610612760']['201566-203460-203506-203902-203924']['101162-202322-202693-203078-203490']['201566'][pbpstats.FINAL_MINUTE_PENALTY_TAKE_FOUL_STRING + pbpstats.FTS_MADE_STRING] == 2
