import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.pbp.file import StatsNbaPbpFileLoader
from pbpstats.data_loader.stats_nba.pbp.loader import StatsNbaPbpLoader
from pbpstats.data_loader.stats_nba.pbp.web import StatsNbaPbpWebLoader
from pbpstats.resources.pbp.stats_nba_pbp_item import StatsNbaPbpItem


class TestStatsPbpLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "game_id": "0021600270",
        "eventnum": 0,
        "eventmsgtype": 12,
        "eventmsgactiontype": 0,
        "period": 1,
        "wctimestring": "8:11 PM",
        "pctimestring": "12:00",
        "homedescription": None,
        "neutraldescription": None,
        "visitordescription": None,
        "score": None,
        "scoremargin": None,
        "person1type": 0,
        "player1_id": 0,
        "player1_name": None,
        "player1_team_id": None,
        "player1_team_city": None,
        "player1_team_nickname": None,
        "player1_team_abbreviation": None,
        "person2type": 0,
        "player2_id": 0,
        "player2_name": None,
        "player2_team_id": None,
        "player2_team_city": None,
        "player2_team_nickname": None,
        "player2_team_abbreviation": None,
        "person3type": 0,
        "player3_id": 0,
        "player3_name": None,
        "player3_team_id": None,
        "player3_team_city": None,
        "player3_team_nickname": None,
        "player3_team_abbreviation": None,
        "video_available_flag": 0,
        "order": 0,
    }

    def test_file_loader_loads_data(self):
        source_loader = StatsNbaPbpFileLoader(self.data_directory)
        pbp_loader = StatsNbaPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 540
        assert isinstance(pbp_loader.items[0], StatsNbaPbpItem)
        assert pbp_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/pbp/stats_{self.game_id}.json") as f:
            pbp_response = json.loads(f.read())
        base_url = "https://stats.nba.com/stats/playbyplayv2"
        query_params = {
            "GameId": self.game_id,
            "StartPeriod": 0,
            "EndPeriod": 10,
            "RangeType": 2,
            "StartRange": 0,
            "EndRange": 55800,
        }
        pbp_url = furl(base_url).add(query_params).url
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        source_loader = StatsNbaPbpWebLoader(self.data_directory)
        pbp_loader = StatsNbaPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 540
        assert isinstance(pbp_loader.items[0], StatsNbaPbpItem)
        assert pbp_loader.items[0].data == self.expected_first_item_data
