import json

import responses

from pbpstats.data_loader.live.possessions_loader import LivePossessionLoader
from pbpstats.resources.possessions.possession import Possession


class TestDataPossessionsLoader:
    game_id = "0022000001"
    data_directory = "tests/data"
    expected_first_item_data = {
        "game_id": "0022000001",
        "period": 1,
        "events": [
            "<LiveStartOfPeriod GameId: 0022000001, Description: Period Start, Time: PT12M00.00S, EventNum: 2>",
            "<LiveJumpBall GameId: 0022000001, Description: Jump Ball D. Jordan vs. J. Wiseman: Tip to Team (BKN), Time: PT11M58.00S, EventNum: 4>",
            "<LiveTurnover GameId: 0022000001, Description: D. Jordan bad pass out-of-bounds TURNOVER (1 TO), Time: PT11M50.00S, EventNum: 7>",
        ],
        "previous_possession": None,
        "next_possession": "<Possession GameId: 0022000001, Period: 1, Number: 2, StartTime: PT11M50.00S, EndTime: PT11M38.00S, OffenseTeamId: 1610612744>",
        "number": 1,
    }

    def test_file_loader_loads_data(self):
        possessions_loader = LivePossessionLoader(
            self.game_id, "file", self.data_directory
        )
        assert len(possessions_loader.items) == 224
        assert isinstance(possessions_loader.items[0], Possession)
        assert (
            possessions_loader.items[0].data["game_id"]
            == self.expected_first_item_data["game_id"]
        )
        assert (
            possessions_loader.items[0].data["number"]
            == self.expected_first_item_data["number"]
        )
        assert (
            possessions_loader.items[0].data["period"]
            == self.expected_first_item_data["period"]
        )
        assert (
            possessions_loader.items[0].data["previous_possession"]
            == self.expected_first_item_data["previous_possession"]
        )
        assert (
            str(possessions_loader.items[0].data["next_possession"])
            == self.expected_first_item_data["next_possession"]
        )
        assert (
            str(possessions_loader.items[0].data["events"][0])
            == self.expected_first_item_data["events"][0]
        )
        assert (
            str(possessions_loader.items[0].data["events"][1])
            == self.expected_first_item_data["events"][1]
        )
        assert (
            str(possessions_loader.items[0].data["events"][2])
            == self.expected_first_item_data["events"][2]
        )

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/pbp/live_{self.game_id}.json") as f:
            pbp_response = json.loads(f.read())
        pbp_url = f"https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.game_id}.json"
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        possessions_loader = LivePossessionLoader(
            self.game_id, "web", self.data_directory
        )
        assert len(possessions_loader.items) == 224
        assert isinstance(possessions_loader.items[0], Possession)
        assert (
            possessions_loader.items[0].data["game_id"]
            == self.expected_first_item_data["game_id"]
        )
        assert (
            possessions_loader.items[0].data["number"]
            == self.expected_first_item_data["number"]
        )
        assert (
            possessions_loader.items[0].data["period"]
            == self.expected_first_item_data["period"]
        )
        assert (
            possessions_loader.items[0].data["previous_possession"]
            == self.expected_first_item_data["previous_possession"]
        )
        assert (
            str(possessions_loader.items[0].data["next_possession"])
            == self.expected_first_item_data["next_possession"]
        )
        assert (
            str(possessions_loader.items[0].data["events"][0])
            == self.expected_first_item_data["events"][0]
        )
        assert (
            str(possessions_loader.items[0].data["events"][1])
            == self.expected_first_item_data["events"][1]
        )
        assert (
            str(possessions_loader.items[0].data["events"][2])
            == self.expected_first_item_data["events"][2]
        )
