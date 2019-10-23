import json

import responses
import pbpstats
from furl import furl
from pbpstats.stats_game_data import StatsGameData


class TestStatsGameData:
    @responses.activate
    def setup_class(cls):
        cls.GameId = '0021600270'
        with open('tests/data/stats_game_pbp_response.json') as f:
            game_pbp_response = json.loads(f.read())

        with open('tests/data/stats_game_summary_response.json') as f:
            game_summary_response = json.loads(f.read())

        with open('tests/data/stats_game_boxscore_response.json') as f:
            boxscore_response = json.loads(f.read())

        with open('tests/data/stats_game_home_shots_response.json') as f:
            home_shots_response = json.loads(f.read())

        with open('tests/data/stats_game_away_shots_response.json') as f:
            away_shots_response = json.loads(f.read())

        pbp_base_url = 'https://stats.nba.com/stats/playbyplayv2'
        pbp_query_params = {
            'EndPeriod': 10,
            'EndRange': 55800,
            'GameId': '0021600270',
            'RangeType': 2,
            'StartPeriod': 0,
            'StartRange': 0,
        }
        pbp_url = furl(pbp_base_url).add(pbp_query_params).url

        game_summary_url = 'https://stats.nba.com/stats/boxscoresummaryv2?GameId=0021600270'

        boxscore_base_url = 'https://stats.nba.com/stats/boxscoretraditionalv2'
        boxscore_query_params = {
            'EndPeriod': 10,
            'EndRange': 55800,
            'GameId': '0021600270',
            'RangeType': 2,
            'StartPeriod': 0,
            'StartRange': 0,
        }
        boxscore_url = furl(boxscore_base_url).add(boxscore_query_params).url

        shots_base_url = 'https://stats.nba.com/stats/shotchartdetail'
        home_shots_query_params = {
            'GameID': '0021600270',
            'Season': '2016-17',
            'SeasonType': 'Regular Season',
            'TeamID': 1610612760,
            'PlayerID': 0,
            'Outcome': '',
            'Location': '',
            'Month': 0,
            'SeasonSegment': '',
            'DateFrom': '',
            'DateTo': '',
            'OpponentTeamID': 0,
            'VsConference': '',
            'VsDivision': '',
            'Position': '',
            'RookieYear': '',
            'GameSegment': '',
            'Period': 0,
            'LastNGames': 0,
            'ContextMeasure': 'FG_PCT',
            'PlayerPosition': '',
            'LeagueID': '00',
        }
        home_shots_url = furl(shots_base_url).add(home_shots_query_params).url
        away_shots_query_params = {
            'GameID': '0021600270',
            'Season': '2016-17',
            'SeasonType': 'Regular Season',
            'TeamID': 1610612764,
            'PlayerID': 0,
            'Outcome': '',
            'Location': '',
            'Month': 0,
            'SeasonSegment': '',
            'DateFrom': '',
            'DateTo': '',
            'OpponentTeamID': 0,
            'VsConference': '',
            'VsDivision': '',
            'Position': '',
            'RookieYear': '',
            'GameSegment': '',
            'Period': 0,
            'LastNGames': 0,
            'ContextMeasure': 'FG_PCT',
            'PlayerPosition': '',
            'LeagueID': '00',
        }
        away_shots_url = furl(shots_base_url).add(away_shots_query_params).url

        responses.add(responses.GET, pbp_url, json=game_pbp_response, status=200)
        responses.add(responses.GET, game_summary_url, json=game_summary_response, status=200)
        responses.add(responses.GET, boxscore_url, json=boxscore_response, status=200)
        responses.add(responses.GET, home_shots_url, json=home_shots_response, status=200)
        responses.add(responses.GET, away_shots_url, json=away_shots_response, status=200)

        with open('tests/data/missing_period_starters.json') as f:
            period_starters_override = json.loads(f.read())

        cls.GameData = StatsGameData(cls.GameId, response_data_directory=None)
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
        assert o_player_stats_dict['101162'] == {'SecondsPlayedOff': 1, 'Period2Fouls2SecondsPlayedOff': 1, 'PenaltySecondsPlayedOff': 1}
        assert o_player_stats_dict['1626162'] == {'SecondsPlayedOff': 1, 'Period2Fouls1SecondsPlayedOff': 1, 'PenaltySecondsPlayedOff': 1}
        assert o_player_stats_dict['202322'] == {'SecondsPlayedOff': 1, 'Period2Fouls0SecondsPlayedOff': 1, 'PenaltySecondsPlayedOff': 1}
        assert o_player_stats_dict['203078'] == {'SecondsPlayedOff': 1, 'Period2Fouls1SecondsPlayedOff': 1, 'PenaltySecondsPlayedOff': 1}
        assert o_player_stats_dict['203107'] == {'SecondsPlayedOff': 1, 'Period2Fouls1SecondsPlayedOff': 1, 'PenaltySecondsPlayedOff': 1}
        assert d_player_stats_dict['201566'] == {'SecondsPlayedDef': 1, 'Period2Fouls2SecondsPlayedDef': 1, 'PenaltySecondsPlayedDef': 1}
        assert d_player_stats_dict['201627'] == {'SecondsPlayedDef': 1, 'Period2Fouls0SecondsPlayedDef': 1, 'PenaltySecondsPlayedDef': 1}
        assert d_player_stats_dict['203500'] == {'SecondsPlayedDef': 1, 'Period2Fouls1SecondsPlayedDef': 1, 'PenaltySecondsPlayedDef': 1}
        assert d_player_stats_dict['203506'] == {'SecondsPlayedDef': 1, 'Period2Fouls1SecondsPlayedDef': 1, 'PenaltySecondsPlayedDef': 1}
        assert d_player_stats_dict['203924'] == {'SecondsPlayedDef': 1, 'Period2Fouls2SecondsPlayedDef': 1, 'PenaltySecondsPlayedDef': 1}
        assert self.GameData.Periods[1].Possessions[-1].ShotData == []
        assert self.GameData.Periods[1].Possessions[-1].GameId == self.GameId
        assert self.GameData.Periods[1].Possessions[-1].Period == 2
        assert self.GameData.Periods[1].Possessions[-1].PossessionNumber == 54
        assert self.GameData.Periods[1].Possessions[-1].OffenseTeamId == '1610612764'
        assert self.GameData.Periods[1].Possessions[-1].DefenseTeamId == '1610612760'
        assert self.GameData.Periods[1].Possessions[-1].StartTime == 1
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

    def test_aggregate_team_stats(self):
        stats = self.GameData.get_aggregated_possession_stats_for_entity_type('team')
        assert stats['1610612760']['OffPoss'] == 109
        assert stats['1610612760']['DefPoss'] == 108

        assert stats['1610612764']['OffPoss'] == 108
        assert stats['1610612764']['DefPoss'] == 109
        assert stats['1610612764']['2pt And 1 Free Throw Trips'] == 1
        assert stats['1610612764']['2pt Shooting Foul Free Throw Trips'] == 11
        assert stats['1610612764']['Technical Free Throws Trips'] == 1
        assert stats['1610612764']['AssistedArc3'] == 6
        assert stats['1610612764']['AssistedAtRim'] == 12
        assert stats['1610612764']['AssistedCorner3'] == 2
        assert stats['1610612764']['AssistedLongMidRange'] == 1
        assert stats['1610612764']['AssistedShortMidRange'] == 4
        assert stats['1610612764']['UnassistedArc3'] == 2
        assert stats['1610612764']['UnassistedAtRim'] == 10
        assert stats['1610612764']['UnassistedLongMidRange'] == 1
        assert stats['1610612764']['UnassistedShortMidRange'] == 6
        assert stats['1610612764']['MissedArc3'] == 13
        assert stats['1610612764']['MissedAtRim'] == 10
        assert stats['1610612764']['MissedCorner3'] == 5
        assert stats['1610612764']['MissedLongMidRange'] == 9
        assert stats['1610612764']['MissedShortMidRange'] == 13
        assert stats['1610612764']['AtRimBlocked'] == 3
        assert stats['1610612764']['ShortMidRangeBlocked'] == 1
        assert stats['1610612764']['Putbacks'] == 3
        assert stats['1610612764']['SecondsPlayedDef'] == 1544.0
        assert stats['1610612764']['SecondsPlayedOff'] == 1636.0
        assert stats['1610612764']['PlusMinus'] == -11
        assert stats['1610612764']['OpponentPoints'] == 126
        assert round(stats['1610612764']['Total2ptShotDistance'], 1) == 442.3
        assert stats['1610612764']['Total2ptShotsWithDistance'] == 70
        assert round(stats['1610612764']['Total3ptShotDistance'], 1) == 697.3
        assert stats['1610612764']['Total3ptShotsWithDistance'] == 28
        assert stats['1610612764']['FtsMade'] == 17
        assert stats['1610612764']['HeaveMisses'] == 1
        assert stats['1610612764']['Arc3DefReboundOpportunities'] == 12
        assert stats['1610612764']['Arc3DefRebounds'] == 10
        assert stats['1610612764']['Arc3OffReboundOpportunities'] == 12
        assert stats['1610612764']['Arc3OffRebounds'] == 2
        assert stats['1610612764']['Corner3DefReboundOpportunities'] == 6
        assert stats['1610612764']['Corner3DefRebounds'] == 5
        assert stats['1610612764']['Corner3OffReboundOpportunities'] == 4
        assert stats['1610612764']['LongMidRangeDefReboundOpportunities'] == 10
        assert stats['1610612764']['LongMidRangeDefRebounds'] == 7
        assert stats['1610612764']['LongMidRangeOffReboundOpportunities'] == 9
        assert stats['1610612764']['LongMidRangeOffRebounds'] == 3
        assert stats['1610612764']['ShortMidRangeBlockedOffReboundOpportunities'] == 1
        assert stats['1610612764']['ShortMidRangeDefReboundOpportunities'] == 6
        assert stats['1610612764']['ShortMidRangeDefRebounds'] == 4
        assert stats['1610612764']['ShortMidRangeOffReboundOpportunities'] == 12
        assert stats['1610612764']['ShortMidRangeOffRebounds'] == 4
        assert stats['1610612764']['AtRimBlockedDefReboundOpportunities'] == 3
        assert stats['1610612764']['AtRimBlockedDefRebounds'] == 2
        assert stats['1610612764']['AtRimBlockedOffReboundOpportunities'] == 3
        assert stats['1610612764']['AtRimBlockedOffRebounds'] == 2
        assert stats['1610612764']['AtRimDefReboundOpportunities'] == 11
        assert stats['1610612764']['AtRimDefRebounds'] == 8
        assert stats['1610612764']['AtRimOffReboundOpportunities'] == 10
        assert stats['1610612764']['AtRimOffRebounds'] == 2
        assert stats['1610612764']['FTDefReboundOpportunities'] == 4
        assert stats['1610612764']['FTDefRebounds'] == 3
        assert stats['1610612764']['FTOffReboundOpportunities'] == 4
        assert stats['1610612764']['PenaltyDefPoss'] == 25
        assert stats['1610612764']['PenaltyOffPoss'] == 45
        assert stats['1610612764']['SecondChanceDefPoss'] == 11
        assert stats['1610612764']['SecondChanceOffPoss'] == 13
        assert stats['1610612764']['BlockedAtRimRecovered'] == 2
        assert stats['1610612764']['DeadBallTurnovers'] == 2
        assert stats['1610612764']['LiveBallTurnovers'] == 10
        assert stats['1610612764']['LostBallTurnovers'] == 2
        assert stats['1610612764']['LostBallOutOfBoundsTurnovers'] == 1
        assert stats['1610612764']['BadPassTurnovers'] == 8
        assert stats['1610612764']['BadPassOutOfBoundsTurnovers'] == 0
        assert stats['1610612764']['Steals'] == 8
        assert stats['1610612764']['FinalMinutePenaltyTakeFoulDefPoss'] == 2
        assert stats['1610612764']['Loose Ball Fouls Drawn'] == 2
        assert stats['1610612764']['Loose Ball Fouls'] == 1
        assert stats['1610612764']['Personal Block Fouls'] == 2
        assert stats['1610612764']['Personal Fouls Drawn'] == 7
        assert stats['1610612764']['Personal Fouls'] == 7
        assert stats['1610612764']['Personal Take Fouls Drawn'] == 1
        assert stats['1610612764']['Personal Take Fouls'] == 2
        assert stats['1610612764']['Shooting Block Fouls'] == 2
        assert stats['1610612764']['Shooting Fouls Drawn'] == 12
        assert stats['1610612764']['Shooting Fouls'] == 11

    def test_aggregate_opponent_stats(self):
        stats = self.GameData.get_aggregated_possession_stats_for_entity_type('opponent')
        assert stats['1610612764']['OffPoss'] == 109
        assert stats['1610612764']['DefPoss'] == 108

        assert stats['1610612760']['OffPoss'] == 108
        assert stats['1610612760']['DefPoss'] == 109
        assert stats['1610612760']['2pt And 1 Free Throw Trips'] == 1
        assert stats['1610612760']['2pt Shooting Foul Free Throw Trips'] == 11
        assert stats['1610612760']['Technical Free Throws Trips'] == 1
        assert stats['1610612760']['AssistedArc3'] == 6
        assert stats['1610612760']['AssistedAtRim'] == 12
        assert stats['1610612760']['AssistedCorner3'] == 2
        assert stats['1610612760']['AssistedLongMidRange'] == 1
        assert stats['1610612760']['AssistedShortMidRange'] == 4
        assert stats['1610612760']['UnassistedArc3'] == 2
        assert stats['1610612760']['UnassistedAtRim'] == 10
        assert stats['1610612760']['UnassistedLongMidRange'] == 1
        assert stats['1610612760']['UnassistedShortMidRange'] == 6
        assert stats['1610612760']['MissedArc3'] == 13
        assert stats['1610612760']['MissedAtRim'] == 10
        assert stats['1610612760']['MissedCorner3'] == 5
        assert stats['1610612760']['MissedLongMidRange'] == 9
        assert stats['1610612760']['MissedShortMidRange'] == 13
        assert stats['1610612760']['AtRimBlocked'] == 3
        assert stats['1610612760']['ShortMidRangeBlocked'] == 1
        assert stats['1610612760']['Putbacks'] == 3
        assert stats['1610612760']['SecondsPlayedDef'] == 1544.0
        assert stats['1610612760']['SecondsPlayedOff'] == 1636.0
        assert stats['1610612760']['PlusMinus'] == -11
        assert stats['1610612760']['OpponentPoints'] == 126
        assert round(stats['1610612760']['Total2ptShotDistance'], 1) == 442.3
        assert stats['1610612760']['Total2ptShotsWithDistance'] == 70
        assert round(stats['1610612760']['Total3ptShotDistance'], 1) == 697.3
        assert stats['1610612760']['Total3ptShotsWithDistance'] == 28
        assert stats['1610612760']['FtsMade'] == 17
        assert stats['1610612760']['HeaveMisses'] == 1
        assert stats['1610612760']['Arc3DefReboundOpportunities'] == 12
        assert stats['1610612760']['Arc3DefRebounds'] == 10
        assert stats['1610612760']['Arc3OffReboundOpportunities'] == 12
        assert stats['1610612760']['Arc3OffRebounds'] == 2
        assert stats['1610612760']['Corner3DefReboundOpportunities'] == 6
        assert stats['1610612760']['Corner3DefRebounds'] == 5
        assert stats['1610612760']['Corner3OffReboundOpportunities'] == 4
        assert stats['1610612760']['LongMidRangeDefReboundOpportunities'] == 10
        assert stats['1610612760']['LongMidRangeDefRebounds'] == 7
        assert stats['1610612760']['LongMidRangeOffReboundOpportunities'] == 9
        assert stats['1610612760']['LongMidRangeOffRebounds'] == 3
        assert stats['1610612760']['ShortMidRangeBlockedOffReboundOpportunities'] == 1
        assert stats['1610612760']['ShortMidRangeDefReboundOpportunities'] == 6
        assert stats['1610612760']['ShortMidRangeDefRebounds'] == 4
        assert stats['1610612760']['ShortMidRangeOffReboundOpportunities'] == 12
        assert stats['1610612760']['ShortMidRangeOffRebounds'] == 4
        assert stats['1610612760']['AtRimBlockedDefReboundOpportunities'] == 3
        assert stats['1610612760']['AtRimBlockedDefRebounds'] == 2
        assert stats['1610612760']['AtRimBlockedOffReboundOpportunities'] == 3
        assert stats['1610612760']['AtRimBlockedOffRebounds'] == 2
        assert stats['1610612760']['AtRimDefReboundOpportunities'] == 11
        assert stats['1610612760']['AtRimDefRebounds'] == 8
        assert stats['1610612760']['AtRimOffReboundOpportunities'] == 10
        assert stats['1610612760']['AtRimOffRebounds'] == 2
        assert stats['1610612760']['FTDefReboundOpportunities'] == 4
        assert stats['1610612760']['FTDefRebounds'] == 3
        assert stats['1610612760']['FTOffReboundOpportunities'] == 4
        assert stats['1610612760']['PenaltyDefPoss'] == 25
        assert stats['1610612760']['PenaltyOffPoss'] == 45
        assert stats['1610612760']['SecondChanceDefPoss'] == 11
        assert stats['1610612760']['SecondChanceOffPoss'] == 13
        assert stats['1610612760']['BlockedAtRimRecovered'] == 2
        assert stats['1610612760']['DeadBallTurnovers'] == 2
        assert stats['1610612760']['LiveBallTurnovers'] == 10
        assert stats['1610612760']['Steals'] == 8
        assert stats['1610612760']['FinalMinutePenaltyTakeFoulDefPoss'] == 2
        assert stats['1610612760']['Loose Ball Fouls Drawn'] == 2
        assert stats['1610612760']['Loose Ball Fouls'] == 1
        assert stats['1610612760']['Personal Block Fouls'] == 2
        assert stats['1610612760']['Personal Fouls Drawn'] == 7
        assert stats['1610612760']['Personal Fouls'] == 7
        assert stats['1610612760']['Personal Take Fouls Drawn'] == 1
        assert stats['1610612760']['Personal Take Fouls'] == 2
        assert stats['1610612760']['Shooting Block Fouls'] == 2
        assert stats['1610612760']['Shooting Fouls Drawn'] == 12
        assert stats['1610612760']['Shooting Fouls'] == 11

    def test_aggregate_player_stats(self):
        stats = self.GameData.get_aggregated_possession_stats_for_entity_type('player')
        assert stats['1610612760']['201566']['OffPoss'] == 87
        assert stats['1610612760']['201566']['DefPoss'] == 88
        assert stats['1610612760']['201566']['SecondsPlayedDef'] == 1288.0
        assert stats['1610612760']['201566']['SecondsPlayedOff'] == 1179.0
        assert stats['1610612760']['201566']['PlusMinus'] == 4
        assert stats['1610612760']['201566']['FtsMade'] == 10
        assert stats['1610612760']['201566']['AssistedAtRim'] == 2
        assert stats['1610612760']['201566']['AssistedShortMidRange'] == 1
        assert stats['1610612760']['201566']['UnassistedArc3'] == 1
        assert stats['1610612760']['201566']['UnassistedAtRim'] == 4
        assert stats['1610612760']['201566']['UnassistedLongMidRange'] == 3
        assert stats['1610612760']['201566']['UnassistedShortMidRange'] == 1
        assert stats['1610612760']['201566']['MissedArc3'] == 4
        assert stats['1610612760']['201566']['MissedAtRim'] == 8
        assert stats['1610612760']['201566']['MissedCorner3'] == 1
        assert stats['1610612760']['201566']['MissedLongMidRange'] == 6
        assert stats['1610612760']['201566']['MissedShortMidRange'] == 3
        assert stats['1610612760']['201566']['AtRimBlocked'] == 1
        assert stats['1610612760']['201566']['Putbacks'] == 2
        assert round(stats['1610612760']['201566']['Total2ptShotDistance'], 1) == 225.0
        assert stats['1610612760']['201566']['Total2ptShotsWithDistance'] == 29
        assert round(stats['1610612760']['201566']['Total3ptShotDistance'], 1) == 148.3
        assert stats['1610612760']['201566']['Total3ptShotsWithDistance'] == 6
        assert stats['1610612760']['201566']['Arc3Assists'] == 3
        assert stats['1610612760']['201566']['AtRimAssists'] == 7
        assert stats['1610612760']['201566']['ShortMidRangeAssists'] == 1
        assert stats['1610612760']['201566']['2pt And 1 Free Throw Trips'] == 1
        assert stats['1610612760']['201566']['2pt Shooting Foul Free Throw Trips'] == 2
        assert stats['1610612760']['201566']['Penalty Free Throw Trips'] == 2
        assert stats['1610612760']['201566']['Technical Free Throws Trips'] == 1
        assert stats['1610612760']['201566']['Personal Block Fouls Drawn'] == 1
        assert stats['1610612760']['201566']['Personal Fouls Drawn'] == 1
        assert stats['1610612760']['201566']['Personal Fouls'] == 2
        assert stats['1610612760']['201566']['Personal Take Fouls Drawn'] == 2
        assert stats['1610612760']['201566']['Personal Take Fouls'] == 1
        assert stats['1610612760']['201566']['Shooting Block Fouls Drawn'] == 2
        assert stats['1610612760']['201566']['Shooting Fouls Drawn'] == 1
        assert stats['1610612760']['201566']['DeadBallTurnovers'] == 1
        assert stats['1610612760']['201566']['LiveBallTurnovers'] == 4
        assert stats['1610612760']['201566']['Steals'] == 2
        assert stats['1610612760']['201566']['ShortMidRangeOffRebounded'] == 1
        assert stats['1610612760']['201566']['ShortMidRangeOffReboundedOpportunities'] == 3
        assert stats['1610612760']['201566']['LongMidRangeOffRebounded'] == 1
        assert stats['1610612760']['201566']['LongMidRangeOffReboundedOpportunities'] == 6
        assert stats['1610612760']['201566']['Corner3DefReboundOpportunities'] == 2
        assert stats['1610612760']['201566']['Corner3OffReboundedOpportunities'] == 1
        assert stats['1610612760']['201566']['AtRimOffRebounded'] == 3
        assert stats['1610612760']['201566']['AtRimOffReboundedOpportunities'] == 8
        assert stats['1610612760']['201566']['AtRimBlockedOffRebounded'] == 1
        assert stats['1610612760']['201566']['AtRimBlockedOffReboundedOpportunities'] == 1
        assert stats['1610612760']['201566']['Arc3OffReboundedOpportunities'] == 4
        assert stats['1610612760']['201566']['Arc3DefReboundOpportunities'] == 10
        assert stats['1610612760']['201566']['Arc3DefRebounds'] == 1
        assert stats['1610612760']['201566']['Arc3OffReboundOpportunities'] == 9
        assert stats['1610612760']['201566']['Arc3OffRebounds'] == 1
        assert stats['1610612760']['201566']['AtRimBlockedDefReboundOpportunities'] == 2
        assert stats['1610612760']['201566']['AtRimBlockedDefRebounds'] == 1
        assert stats['1610612760']['201566']['AtRimBlockedOffReboundOpportunities'] == 3
        assert stats['1610612760']['201566']['AtRimDefReboundOpportunities'] == 8
        assert stats['1610612760']['201566']['AtRimDefRebounds'] == 1
        assert stats['1610612760']['201566']['AtRimOffReboundOpportunities'] == 9
        assert stats['1610612760']['201566']['AtRimOffRebounds'] == 1
        assert stats['1610612760']['201566']['Corner3OffReboundOpportunities'] == 6
        assert stats['1610612760']['201566']['FTDefReboundOpportunities'] == 4
        assert stats['1610612760']['201566']['FTDefRebounds'] == 3
        assert stats['1610612760']['201566']['FTOffReboundOpportunities'] == 4
        assert stats['1610612760']['201566']['FTOffRebounds'] == 1
        assert stats['1610612760']['201566']['LongMidRangeDefReboundOpportunities'] == 7
        assert stats['1610612760']['201566']['LongMidRangeDefRebounds'] == 3
        assert stats['1610612760']['201566']['LongMidRangeOffReboundOpportunities'] == 9
        assert stats['1610612760']['201566']['LongMidRangeOffRebounds'] == 1
        assert stats['1610612760']['201566']['ShortMidRangeBlockedDefReboundOpportunities'] == 1
        assert stats['1610612760']['201566']['ShortMidRangeDefReboundOpportunities'] == 5
        assert stats['1610612760']['201566']['ShortMidRangeDefRebounds'] == 1
        assert stats['1610612760']['201566']['ShortMidRangeOffReboundOpportunities'] == 5
        assert stats['1610612760']['201566']['OnFloorOffReb'] == 12
        assert stats['1610612760']['201566']['FinalMinutePenaltyTakeFoulFtsMade'] == 4
        assert stats['1610612760']['201566']['FinalMinutePenaltyTakeFoulOffPoss'] == 2
        assert stats['1610612760']['201566']['PenaltyDefPoss'] == 35
        assert stats['1610612760']['201566']['PenaltyOffPoss'] == 17
        assert stats['1610612760']['201566']['PenaltySecondsPlayedDef'] == 445.0
        assert stats['1610612760']['201566']['PenaltySecondsPlayedOff'] == 188.0
        assert stats['1610612760']['201566']['Period1Fouls0SecondsPlayedDef'] == 193.0
        assert stats['1610612760']['201566']['Period1Fouls0SecondsPlayedOff'] == 178.0
        assert stats['1610612760']['201566']['Period1Fouls1SecondsPlayedDef'] == 77.0
        assert stats['1610612760']['201566']['Period1Fouls1SecondsPlayedOff'] == 67.0
        assert stats['1610612760']['201566']['Period2Fouls1SecondsPlayedDef'] == 144.0
        assert stats['1610612760']['201566']['Period2Fouls1SecondsPlayedOff'] == 155.0
        assert stats['1610612760']['201566']['Period2Fouls2SecondsPlayedDef'] == 111.0
        assert stats['1610612760']['201566']['Period2Fouls2SecondsPlayedOff'] == 114.0
        assert stats['1610612760']['201566']['Period3Fouls2SecondsPlayedDef'] == 273.0
        assert stats['1610612760']['201566']['Period3Fouls2SecondsPlayedOff'] == 307.0
        assert stats['1610612760']['201566']['Period4Fouls2SecondsPlayedDef'] == 335.0
        assert stats['1610612760']['201566']['Period4Fouls2SecondsPlayedOff'] == 213.0
        assert stats['1610612760']['201566']['PeriodOTFouls2SecondsPlayedDef'] == 141.0
        assert stats['1610612760']['201566']['PeriodOTFouls2SecondsPlayedOff'] == 141.0
        assert stats['1610612760']['201566']['PeriodOTFouls3SecondsPlayedDef'] == 14.0
        assert stats['1610612760']['201566']['PeriodOTFouls3SecondsPlayedOff'] == 4.0
        assert stats['1610612760']['201566']['SecondChanceOffPoss'] == 10
        assert stats['1610612760']['201566']['SecondChanceSecondsPlayedDef'] == 72.0
        assert stats['1610612760']['201566']['SecondChanceSecondsPlayedOff'] == 47.0

    def test_aggregate_lineup_stats(self):
        stats = self.GameData.get_aggregated_possession_stats_for_entity_type('lineup')
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['OffPoss'] == 19
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['DefPoss'] == 19
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['SecondsPlayedDef'] == 358.0
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['SecondsPlayedOff'] == 313.0
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['PlusMinus'] == 4

    def test_aggregate_lineup_opponent_stats(self):
        stats = self.GameData.get_aggregated_possession_stats_for_entity_type('lineupopponent')
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['OffPoss'] == 19
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['DefPoss'] == 19
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['SecondsPlayedDef'] == 313.0
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['SecondsPlayedOff'] == 358.0
        assert stats['1610612760']['1627734-201566-203460-203500-203506']['PlusMinus'] == -4

    def test_aggregate_invalid_entity_stats(self):
        stats = self.GameData.get_aggregated_possession_stats_for_entity_type('invalid')
        assert stats is None
