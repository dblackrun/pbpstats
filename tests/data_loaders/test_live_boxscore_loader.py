import json

import responses

from pbpstats.data_loader.live.boxscore_loader import LiveBoxscoreLoader
from pbpstats.resources.boxscore.live_boxscore_item import LiveBoxscoreItem


class TestLiveBoxscoreLoader:
    game_id = "0022000001"
    data_directory = "tests/data"

    def test_file_loader_loads_data(self):
        boxscore_loader = LiveBoxscoreLoader(self.game_id, "file", self.data_directory)
        assert len(boxscore_loader.items) == 36
        assert isinstance(boxscore_loader.items[0], LiveBoxscoreItem)
        assert boxscore_loader.items[0].player_id == 203952
        assert boxscore_loader.items[0].total_seconds == 1874
        assert boxscore_loader.items[0].name == "Andrew Wiggins"
        assert boxscore_loader.items[0].team_id == 1610612744

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/game_details/live_{self.game_id}.json") as f:
            boxscore_response = json.loads(f.read())
        boxscore_url = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{self.game_id}.json"
        responses.add(responses.GET, boxscore_url, json=boxscore_response, status=200)

        boxscore_loader = LiveBoxscoreLoader(self.game_id, "web", self.data_directory)
        assert len(boxscore_loader.items) == 36
        assert isinstance(boxscore_loader.items[0], LiveBoxscoreItem)
        assert boxscore_loader.items[0].player_id == 203952
        assert boxscore_loader.items[0].total_seconds == 1874
        assert boxscore_loader.items[0].name == "Andrew Wiggins"
        assert boxscore_loader.items[0].team_id == 1610612744
