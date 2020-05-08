import json

import responses

from pbpstats.data_loader.data_nba.boxscore_loader import DataNbaBoxscoreLoader
from pbpstats.resources.boxscore.data_nba_boxscore_item import DataNbaBoxscoreItem


class TestDataBoxscoreLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "team_id": 1610612764,
        "team_abbreviation": "WAS",
        "fn": "Markieff",
        "ln": "Morris",
        "num": " 5",
        "pos": "F",
        "min": 36,
        "sec": 42,
        "totsec": 2202,
        "fga": 16,
        "fgm": 7,
        "tpa": 2,
        "tpm": 0,
        "fta": 8,
        "ftm": 5,
        "oreb": 1,
        "dreb": 6,
        "reb": 7,
        "ast": 2,
        "stl": 1,
        "blk": 1,
        "pf": 5,
        "pts": 19,
        "tov": 2,
        "fbpts": 0,
        "fbptsa": 0,
        "fbptsm": 0,
        "pip": 14,
        "pipa": 9,
        "pipm": 7,
        "court": 1,
        "player_id": 202693,
        "pm": -17,
        "blka": 0,
        "tf": 1,
        "status": "A",
        "memo": "",
        "name": "Markieff Morris",
    }

    def test_file_loader_loads_data(self):
        boxscore_loader = DataNbaBoxscoreLoader(
            self.game_id, "file", self.data_directory
        )
        assert len(boxscore_loader.items) == 32
        assert isinstance(boxscore_loader.items[0], DataNbaBoxscoreItem)
        assert boxscore_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/game_details/data_{self.game_id}.json") as f:
            boxscore_response = json.loads(f.read())
        boxscore_url = f"http://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/gamedetail/{self.game_id}_gamedetail.json"
        responses.add(responses.GET, boxscore_url, json=boxscore_response, status=200)

        boxscore_loader = DataNbaBoxscoreLoader(
            self.game_id, "web", self.data_directory
        )
        assert len(boxscore_loader.items) == 32
        assert isinstance(boxscore_loader.items[0], DataNbaBoxscoreItem)
        assert boxscore_loader.items[0].data == self.expected_first_item_data
