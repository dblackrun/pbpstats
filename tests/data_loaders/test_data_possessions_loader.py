import json

import responses

from pbpstats.data_loader.data_nba.possessions_loader import DataNbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession


class TestDataPossessionsLoader:
    game_id = '0021600270'
    data_directory = 'tests/data'
    expected_first_item_data = {
        'game_id': '0021600270',
        'period': 1,
        'events': [
            '<DataStartOfPeriod GameId: 0021600270, Description: Start Period, Time: 12:00, EventNum: 0>',
            '<DataJumpBall GameId: 0021600270, Description: Jump Ball Adams vs Gortat (Mark Morris gains possession), Time: 12:00, EventNum: 1>',
            "<DataFieldGoal GameId: 0021600270, Description: [WAS 2-0] Mark Morris Step Back Jump shot: Made (2 PTS), Time: 11:39, EventNum: 2>"
        ],
        'previous_possession': None,
        'next_possession': '<Possession GameId: 0021600270, Period: 1, Number: 2, StartTime: 11:39, EndTime: 11:18, OffenseTeamId: 1610612760>',
        'number': 1
    }

    def test_file_loader_loads_data(self):
        possessions_loader = DataNbaPossessionLoader(self.game_id, 'file', self.data_directory)
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
        with open(f'{self.data_directory}/pbp/data_{self.game_id}.json') as f:
            pbp_response = json.loads(f.read())
        pbp_url = f'https://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/pbp/{self.game_id}_full_pbp.json'
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        possessions_loader = DataNbaPossessionLoader(self.game_id, 'web', self.data_directory)
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
