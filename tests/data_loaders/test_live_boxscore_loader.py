import json

import responses

from pbpstats.data_loader.live.boxscore.file import LiveBoxscoreFileLoader
from pbpstats.data_loader.live.boxscore.loader import LiveBoxscoreLoader
from pbpstats.data_loader.live.boxscore.web import LiveBoxscoreWebLoader
from pbpstats.resources.boxscore.live_boxscore_item import LiveBoxscoreItem


class TestLiveBoxscoreLoader:
    game_id = "0022000001"
    data_directory = "tests/data"

    def test_file_loader_loads_data(self):
        source_loader = LiveBoxscoreFileLoader(self.data_directory)
        boxscore_loader = LiveBoxscoreLoader(self.game_id, source_loader)
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
        boxscore_url = f"https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/boxscore/boxscore_{self.game_id}.json"
        responses.add(responses.GET, boxscore_url, json=boxscore_response, status=200)

        source_loader = LiveBoxscoreWebLoader(self.data_directory)
        boxscore_loader = LiveBoxscoreLoader(self.game_id, source_loader)
        assert len(boxscore_loader.items) == 36
        assert isinstance(boxscore_loader.items[0], LiveBoxscoreItem)
        assert boxscore_loader.items[0].player_id == 203952
        assert boxscore_loader.items[0].total_seconds == 1874
        assert boxscore_loader.items[0].name == "Andrew Wiggins"
        assert boxscore_loader.items[0].team_id == 1610612744
