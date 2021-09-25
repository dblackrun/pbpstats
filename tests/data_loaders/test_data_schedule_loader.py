import json

import responses

from pbpstats.data_loader.data_nba.schedule.file import DataNbaScheduleFileLoader
from pbpstats.data_loader.data_nba.schedule.loader import DataNbaScheduleLoader
from pbpstats.data_loader.data_nba.schedule.web import DataNbaScheduleWebLoader
from pbpstats.resources.games.data_nba_game_item import DataNbaGameItem


class TestDataScheduleLoader:
    league = "wnba"
    season = "2019"
    data_directory = "tests/data"

    def test_file_loader_loads_data(self):
        season_type = "Regular Season"
        source_loader = DataNbaScheduleFileLoader(self.data_directory)
        schedule_loader = DataNbaScheduleLoader(
            self.league, self.season, season_type, source_loader
        )
        assert len(schedule_loader.items) == 204
        assert isinstance(schedule_loader.items[0], DataNbaGameItem)
        assert schedule_loader.items[0].data == {
            "game_id": "1021900001",
            "date": "2019-05-24",
            "status": "Final",
            "home_team_id": 1611661330,
            "home_team_abbreviation": "ATL",
            "home_score": "76",
            "away_team_id": 1611661321,
            "away_team_abbreviation": "DAL",
            "away_score": "72",
        }

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(
            f"{self.data_directory}/schedule/data_{self.league}_{self.season}.json"
        ) as f:
            boxscore_response = json.loads(f.read())
        boxscore_url = f"https://data.{self.league}.com/data/10s/v2015/json/mobile_teams/{self.league}/{self.season}/league/10_full_schedule.json"
        responses.add(responses.GET, boxscore_url, json=boxscore_response, status=200)

        season_type = "Playoffs"
        source_loader = DataNbaScheduleWebLoader(self.data_directory)
        schedule_loader = DataNbaScheduleLoader(
            self.league, self.season, season_type, source_loader
        )
        assert len(schedule_loader.items) == 16
        assert isinstance(schedule_loader.items[0], DataNbaGameItem)
        assert schedule_loader.items[0].data == {
            "game_id": "1041900101",
            "date": "2019-09-11",
            "status": "Final",
            "home_team_id": 1611661329,
            "home_team_abbreviation": "CHI",
            "home_score": "105",
            "away_team_id": 1611661317,
            "away_team_abbreviation": "PHO",
            "away_score": "76",
        }
