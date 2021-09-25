import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.boxscore.file import StatsNbaBoxscoreFileLoader
from pbpstats.data_loader.stats_nba.boxscore.loader import StatsNbaBoxscoreLoader
from pbpstats.data_loader.stats_nba.boxscore.web import StatsNbaBoxscoreWebLoader
from pbpstats.resources.boxscore.stats_nba_boxscore_item import StatsNbaBoxscoreItem


class TestStatsBoxscoreLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "game_id": "0021600270",
        "team_id": 1610612764,
        "team_abbreviation": "WAS",
        "team_city": "Washington",
        "player_id": 202693,
        "name": "Markieff Morris",
        "start_position": "F",
        "comment": "",
        "min": "36:42",
        "fgm": 7,
        "fga": 16,
        "fg_pct": 0.438,
        "fg3m": 0,
        "fg3a": 2,
        "fg3_pct": 0,
        "ftm": 5,
        "fta": 8,
        "ft_pct": 0.625,
        "oreb": 1,
        "dreb": 6,
        "reb": 7,
        "ast": 2,
        "stl": 1,
        "blk": 1,
        "to": 2,
        "pf": 5,
        "pts": 19,
        "plus_minus": -17,
    }

    def test_file_loader_loads_data(self):
        source_loader = StatsNbaBoxscoreFileLoader(self.data_directory)
        boxscore_loader = StatsNbaBoxscoreLoader(self.game_id, source_loader)
        assert len(boxscore_loader.items) == 21
        assert isinstance(boxscore_loader.items[0], StatsNbaBoxscoreItem)
        assert boxscore_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(
            f"{self.data_directory}/game_details/stats_boxscore_{self.game_id}.json"
        ) as f:
            boxscore_response = json.loads(f.read())
        boxscore_base_url = "https://stats.nba.com/stats/boxscoretraditionalv2"
        boxscore_query_params = {
            "EndPeriod": 10,
            "EndRange": 55800,
            "GameId": self.game_id,
            "RangeType": 2,
            "StartPeriod": 0,
            "StartRange": 0,
        }
        boxscore_url = furl(boxscore_base_url).add(boxscore_query_params).url
        responses.add(responses.GET, boxscore_url, json=boxscore_response, status=200)

        source_loader = StatsNbaBoxscoreWebLoader(self.data_directory)
        boxscore_loader = StatsNbaBoxscoreLoader(self.game_id, source_loader)
        assert len(boxscore_loader.items) == 21
        assert isinstance(boxscore_loader.items[0], StatsNbaBoxscoreItem)
        assert boxscore_loader.items[0].data == self.expected_first_item_data
