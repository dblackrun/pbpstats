import json

import responses

from pbpstats.data_loader.data_nba.pbp.file import DataNbaPbpFileLoader
from pbpstats.data_loader.data_nba.pbp.loader import DataNbaPbpLoader
from pbpstats.data_loader.data_nba.pbp.web import DataNbaPbpWebLoader
from pbpstats.resources.pbp.data_nba_pbp_item import DataNbaPbpItem


class TestDataPbpLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "period": 1,
        "evt": 0,
        "cl": "12:00",
        "de": "Start Period",
        "locX": 0,
        "locY": -80,
        "opt1": 0,
        "opt2": 0,
        "mtype": 0,
        "etype": 12,
        "opid": "",
        "tid": 0,
        "pid": 0,
        "hs": 0,
        "vs": 0,
        "epid": "",
        "oftid": 0,
    }

    def test_file_loader_loads_data(self):
        source_loader = DataNbaPbpFileLoader(self.data_directory)
        pbp_loader = DataNbaPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 538
        assert isinstance(pbp_loader.items[0], DataNbaPbpItem)
        assert pbp_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/pbp/data_{self.game_id}.json") as f:
            pbp_response = json.loads(f.read())
        pbp_url = f"https://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/pbp/{self.game_id}_full_pbp.json"
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        source_loader = DataNbaPbpWebLoader(self.data_directory)
        pbp_loader = DataNbaPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 538
        assert isinstance(pbp_loader.items[0], DataNbaPbpItem)
        assert pbp_loader.items[0].data == self.expected_first_item_data
