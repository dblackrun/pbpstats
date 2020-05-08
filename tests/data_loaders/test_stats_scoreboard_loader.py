import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.scoreboard_loader import StatsNbaScoreboardLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class TestStatsScoreboardLoader:
    date = "02/25/2020"
    league = "gleague"
    data_directory = "tests/data"
    expected_first_item_data = {
        "game_id": "2021900490",
        "date": "2020-02-25T00:00:00",
        "status": "Final",
        "home_team_id": 1612709917,
        "visitor_team_id": 1612709923,
    }

    def test_file_loader_loads_data(self):
        scoreboard_loader = StatsNbaScoreboardLoader(
            self.date, self.league, self.data_directory, "file"
        )
        assert len(scoreboard_loader.items) == 7
        assert isinstance(scoreboard_loader.items[0], StatsNbaGameItem)
        assert scoreboard_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(
            f'{self.data_directory}/schedule/stats_{self.league}_{self.date.replace("/", "_")}.json'
        ) as f:
            scoreboard_response = json.loads(f.read())
        base_url = f"https://stats.gleague.nba.com/stats/scoreboardV2"
        query_params = {"DayOffset": 0, "LeagueID": "20", "gameDate": self.date}
        scoreboard_url = furl(base_url).add(query_params).url
        responses.add(
            responses.GET, scoreboard_url, json=scoreboard_response, status=200
        )

        scoreboard_loader = StatsNbaScoreboardLoader(
            self.date, self.league, self.data_directory, "web"
        )
        assert len(scoreboard_loader.items) == 7
        assert isinstance(scoreboard_loader.items[0], StatsNbaGameItem)
        assert scoreboard_loader.items[0].data == self.expected_first_item_data
