import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.possessions_loader import StatsNbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession


class TestStatsPossessionsLoader:
    game_id = '0021600270'
    data_directory = 'tests/data'
    expected_first_item_data = {
        'game_id': '0021600270',
        'period': 1,
        'events': [
            '<StatsStartOfPeriod GameId: 0021600270, Description: , Time: 12:00, EventNum: 0>',
            '<StatsJumpBall GameId: 0021600270, Description: Jump Ball Adams vs. Gortat: Tip to Mark Morris, Time: 12:00, EventNum: 1>',
            "<StatsFieldGoal GameId: 0021600270, Description: Mark Morris 12' Step Back Jump Shot (2 PTS), Time: 11:39, EventNum: 2>"
        ],
        'previous_possession': None,
        'next_possession': '<Possession GameId: 0021600270, Period: 1, Number: 2, StartTime: 11:39, EndTime: 11:18, OffenseTeamId: 1610612760>',
        'number': 1
    }

    def test_file_loader_loads_data(self):
        possessions_loader = StatsNbaPossessionLoader(self.game_id, 'file', self.data_directory)
        assert len(possessions_loader.items) == 220
        assert isinstance(possessions_loader.items[0], Possession)
        assert possessions_loader.items[0].data['game_id'] == self.expected_first_item_data['game_id']
        assert possessions_loader.items[0].data['number'] == self.expected_first_item_data['number']
        assert possessions_loader.items[0].data['period'] == self.expected_first_item_data['period']
        assert possessions_loader.items[0].data['previous_possession'] == self.expected_first_item_data['previous_possession']
        assert str(possessions_loader.items[0].data['next_possession']) == self.expected_first_item_data['next_possession']
        assert str(possessions_loader.items[0].data['events'][0]) == self.expected_first_item_data['events'][0]
        assert str(possessions_loader.items[0].data['events'][1]) == self.expected_first_item_data['events'][1]
        assert str(possessions_loader.items[0].data['events'][2]) == self.expected_first_item_data['events'][2]

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f'{self.data_directory}/pbp/stats_{self.game_id}.json') as f:
            pbp_response = json.loads(f.read())
        base_url = 'https://stats.nba.com/stats/playbyplayv2'
        query_params = {
            'GameId': self.game_id,
            'StartPeriod': 0,
            'EndPeriod': 10,
            'RangeType': 2,
            'StartRange': 0,
            'EndRange': 55800
        }
        pbp_url = furl(base_url).add(query_params).url
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        with open(f'{self.data_directory}/game_details/stats_home_shots_{self.game_id}.json') as f:
            home_response = json.loads(f.read())
        with open(f'{self.data_directory}/game_details/stats_away_shots_{self.game_id}.json') as f:
            away_response = json.loads(f.read())
        base_url = 'https://stats.nba.com/stats/shotchartdetail'
        home_query_params = {
            'GameID': self.game_id,
            'TeamID': 1610612760,
            'Season': '2016-17',
            'SeasonType': 'Regular Season',
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
        away_query_params = {
            'GameID': self.game_id,
            'TeamID': 1610612764,
            'Season': '2016-17',
            'SeasonType': 'Regular Season',
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
        home_url = furl(base_url).add(home_query_params).url
        away_url = furl(base_url).add(away_query_params).url
        responses.add(responses.GET, home_url, json=home_response, status=200)
        responses.add(responses.GET, away_url, json=away_response, status=200)

        with open(f'{self.data_directory}/game_details/stats_summary_{self.game_id}.json') as f:
            summary_response = json.loads(f.read())
        summary_base_url = 'https://stats.nba.com/stats/boxscoresummaryv2'
        query_params = {'GameId': self.game_id}
        summary_url = furl(summary_base_url).add(query_params).url
        responses.add(responses.GET, summary_url, json=summary_response, status=200)

        with open(f'{self.data_directory}/period_starters_boxscore_response.json') as f:
            starters_response = json.loads(f.read())
        boxscore_base_url = 'https://stats.nba.com/stats/boxscoretraditionalv2'
        starters_query_params = {
            'GameId': self.game_id,
            'StartPeriod': 0,
            'EndPeriod': 0,
            'RangeType': 2,
            'StartRange': 28800,
            'EndRange': 28940
        }
        starters_url = furl(boxscore_base_url).add(starters_query_params).url
        responses.add(responses.GET, starters_url, json=starters_response, status=200)

        file_directory = None
        possessions_loader = StatsNbaPossessionLoader(self.game_id, 'web', file_directory)
        assert len(possessions_loader.items) == 220
        assert isinstance(possessions_loader.items[0], Possession)
        assert possessions_loader.items[0].data['game_id'] == self.expected_first_item_data['game_id']
        assert possessions_loader.items[0].data['number'] == self.expected_first_item_data['number']
        assert possessions_loader.items[0].data['period'] == self.expected_first_item_data['period']
        assert possessions_loader.items[0].data['previous_possession'] == self.expected_first_item_data['previous_possession']
        assert str(possessions_loader.items[0].data['next_possession']) == self.expected_first_item_data['next_possession']
        assert str(possessions_loader.items[0].data['events'][0]) == self.expected_first_item_data['events'][0]
        assert str(possessions_loader.items[0].data['events'][1]) == self.expected_first_item_data['events'][1]
        assert str(possessions_loader.items[0].data['events'][2]) == self.expected_first_item_data['events'][2]
