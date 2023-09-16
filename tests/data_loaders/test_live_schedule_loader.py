import json

import responses

from pbpstats.data_loader.live.schedule.file import LiveScheduleFileLoader
from pbpstats.data_loader.live.schedule.loader import LiveScheduleLoader
from pbpstats.data_loader.live.schedule.web import LiveScheduleWebLoader
from pbpstats.resources.games.live_game_item import LiveGameItem


class TestDataScheduleLoader:
    league = "nba"
    season = "2023-24"
    data_directory = "tests/data"

    def test_file_loader_loads_data(self):
        season_type = "Regular Season"
        source_loader = LiveScheduleFileLoader(self.data_directory)
        schedule_loader = LiveScheduleLoader(
            self.league, self.season, season_type, source_loader
        )
        assert len(schedule_loader.items) == 1206
        assert isinstance(schedule_loader.items[0], LiveGameItem)
        assert schedule_loader.items[0].data == {
            "game_id": "0022300061",
            "date": "2023-10-24T00:00:00Z",
            "status": "7:30 pm ET",
            "home_team_id": 1610612743,
            "home_team_abbreviation": "DEN",
            "home_score": 0,
            "away_team_id": 1610612747,
            "away_team_abbreviation": "LAL",
            "away_score": 0,
        }

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(f"{self.data_directory}/schedule/live_nba_2023.json") as f:
            schedule_response = json.loads(f.read())
        schedule_url = (
            f"https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_2.json"
        )
        responses.add(responses.GET, schedule_url, json=schedule_response, status=200)

        season_type = "Playoffs"
        source_loader = LiveScheduleWebLoader(self.data_directory)
        schedule_loader = LiveScheduleLoader(
            self.league, self.season, season_type, source_loader
        )
        assert len(schedule_loader.items) == 0
