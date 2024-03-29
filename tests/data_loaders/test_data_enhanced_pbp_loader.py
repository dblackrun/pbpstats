import json

import pytest
import responses

from pbpstats.data_loader.data_nba.enhanced_pbp.file import DataNbaEnhancedPbpFileLoader
from pbpstats.data_loader.data_nba.enhanced_pbp.loader import DataNbaEnhancedPbpLoader
from pbpstats.data_loader.data_nba.enhanced_pbp.web import DataNbaEnhancedPbpWebLoader
from pbpstats.resources.enhanced_pbp import InvalidNumberOfStartersException
from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)


class TestDataEnhancedPbpLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "game_id": "0021600270",
        "event_num": 0,
        "clock": "12:00",
        "period": 1,
        "event_action_type": 0,
        "event_type": 12,
        "player1_id": 0,
        "description": "Start Period",
        "team_id": 0,
        "previous_event": None,
        "next_event": "<DataJumpBall GameId: 0021600270, Description: Jump Ball Adams vs Gortat (Mark Morris gains possession), Time: 12:00, EventNum: 1>",
        "team_starting_with_ball": 1610612760,
        "period_starters": {
            1610612760: [203500, 1627734, 203506, 201566, 203460],
            1610612764: [202693, 101162, 202322, 203078, 203490],
        },
    }

    def test_file_loader_loads_data(self):
        source_loader = DataNbaEnhancedPbpFileLoader(self.data_directory)
        pbp_loader = DataNbaEnhancedPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 538
        assert isinstance(pbp_loader.items[0], DataEnhancedPbpItem)
        assert (
            pbp_loader.items[0].data["game_id"]
            == self.expected_first_item_data["game_id"]
        )
        assert (
            pbp_loader.items[0].data["event_num"]
            == self.expected_first_item_data["event_num"]
        )
        assert (
            pbp_loader.items[0].data["clock"] == self.expected_first_item_data["clock"]
        )
        assert (
            pbp_loader.items[0].data["period"]
            == self.expected_first_item_data["period"]
        )
        assert (
            pbp_loader.items[0].data["event_action_type"]
            == self.expected_first_item_data["event_action_type"]
        )
        assert (
            pbp_loader.items[0].data["event_type"]
            == self.expected_first_item_data["event_type"]
        )
        assert (
            pbp_loader.items[0].data["player1_id"]
            == self.expected_first_item_data["player1_id"]
        )
        assert (
            pbp_loader.items[0].data["description"]
            == self.expected_first_item_data["description"]
        )
        assert (
            pbp_loader.items[0].data["team_id"]
            == self.expected_first_item_data["team_id"]
        )
        assert (
            pbp_loader.items[0].data["previous_event"]
            == self.expected_first_item_data["previous_event"]
        )
        assert (
            str(pbp_loader.items[0].data["next_event"])
            == self.expected_first_item_data["next_event"]
        )
        assert (
            pbp_loader.items[0].data["team_starting_with_ball"]
            == self.expected_first_item_data["team_starting_with_ball"]
        )
        assert (
            pbp_loader.items[0].data["period_starters"]
            == self.expected_first_item_data["period_starters"]
        )

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/pbp/data_{self.game_id}.json") as f:
            pbp_response = json.loads(f.read())
        pbp_url = f"https://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/pbp/{self.game_id}_full_pbp.json"
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        source_loader = DataNbaEnhancedPbpWebLoader(self.data_directory)
        pbp_loader = DataNbaEnhancedPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 538
        assert isinstance(pbp_loader.items[0], DataEnhancedPbpItem)
        assert (
            pbp_loader.items[0].data["game_id"]
            == self.expected_first_item_data["game_id"]
        )
        assert (
            pbp_loader.items[0].data["event_num"]
            == self.expected_first_item_data["event_num"]
        )
        assert (
            pbp_loader.items[0].data["clock"] == self.expected_first_item_data["clock"]
        )
        assert (
            pbp_loader.items[0].data["period"]
            == self.expected_first_item_data["period"]
        )
        assert (
            pbp_loader.items[0].data["event_action_type"]
            == self.expected_first_item_data["event_action_type"]
        )
        assert (
            pbp_loader.items[0].data["event_type"]
            == self.expected_first_item_data["event_type"]
        )
        assert (
            pbp_loader.items[0].data["player1_id"]
            == self.expected_first_item_data["player1_id"]
        )
        assert (
            pbp_loader.items[0].data["description"]
            == self.expected_first_item_data["description"]
        )
        assert (
            pbp_loader.items[0].data["team_id"]
            == self.expected_first_item_data["team_id"]
        )
        assert (
            pbp_loader.items[0].data["previous_event"]
            == self.expected_first_item_data["previous_event"]
        )
        assert (
            str(pbp_loader.items[0].data["next_event"])
            == self.expected_first_item_data["next_event"]
        )
        assert (
            pbp_loader.items[0].data["team_starting_with_ball"]
            == self.expected_first_item_data["team_starting_with_ball"]
        )
        assert (
            pbp_loader.items[0].data["period_starters"]
            == self.expected_first_item_data["period_starters"]
        )

    @responses.activate
    def test_web_loader_not_raises_missing_starter_exception(self):
        with open(f"{self.data_directory}/pbp/data_{self.game_id}.json") as f:
            pbp_response = json.loads(f.read())
        pbp_url = f"https://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/pbp/{self.game_id}_full_pbp.json"
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        with open(
            f"{self.data_directory}/game_details/stats_boxscore_range_{self.game_id}.json"
        ) as f:
            boxscore_range_response = json.loads(f.read())
        boxscore_range_url = f"https://stats.nba.com/stats/boxscoretraditionalv2?GameId={self.game_id}&StartPeriod=0&EndPeriod=0&RangeType=2&StartRange=28800&EndRange=28940"
        responses.add(
            responses.GET, boxscore_range_url, json=boxscore_range_response, status=200
        )

        data_directory = None
        try:
            source_loader = DataNbaEnhancedPbpWebLoader(data_directory)
            assert DataNbaEnhancedPbpLoader(self.game_id, source_loader)
        except InvalidNumberOfStartersException:
            raise pytest.fail("DID RAISE {0}".format(InvalidNumberOfStartersException))
