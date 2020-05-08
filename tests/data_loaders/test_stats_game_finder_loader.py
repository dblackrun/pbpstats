import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.game_finder_loader import StatsNbaGameFinderLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class TestStatsGameFinderLoader:
    league = "nba"
    season = "2018-19"
    season_type = "Regular Season"
    data_directory = "tests/data"

    expected_first_item_data = {
        "game_id": "0021800001",
        "date": "2018-10-16",
        "status": "Final",
        "home_team_id": 1610612738,
        "visitor_team_id": 1610612755,
    }

    def test_file_loader_loads_data(self):
        scoreboard_loader = StatsNbaGameFinderLoader(
            self.league, self.season, self.season_type, "file", self.data_directory
        )
        assert len(scoreboard_loader.items) == 1230
        assert isinstance(scoreboard_loader.items[0], StatsNbaGameItem)
        assert scoreboard_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(
            f'{self.data_directory}/schedule/stats_{self.league}_{self.season.replace("-", "_")}_{self.season_type.replace(" ", "_")}.json'
        ) as f:
            scoreboard_response = json.loads(f.read())
        base_url = f"https://stats.nba.com/stats/leaguegamefinder"
        query_params = {
            "PlayerOrTeam": "T",
            "gtPTS": 1,
            "Season": self.season,
            "SeasonType": self.season_type,
            "LeagueID": "00",
        }
        scoreboard_url = furl(base_url).add(query_params).url
        responses.add(
            responses.GET, scoreboard_url, json=scoreboard_response, status=200
        )

        scoreboard_loader = StatsNbaGameFinderLoader(
            self.league, self.season, self.season_type, "web", self.data_directory
        )
        assert len(scoreboard_loader.items) == 1230
        assert isinstance(scoreboard_loader.items[0], StatsNbaGameItem)
        assert scoreboard_loader.items[0].data == self.expected_first_item_data
