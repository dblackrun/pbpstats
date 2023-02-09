import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.league_game_log.file import (
    StatsNbaLeagueGameLogFileLoader,
)
from pbpstats.data_loader.stats_nba.league_game_log.loader import (
    StatsNbaLeagueGameLogLoader,
)
from pbpstats.data_loader.stats_nba.league_game_log.web import (
    StatsNbaLeagueGameLogWebLoader,
)
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class TestStatsLeagueGameLogLoader:
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
        source_loader = StatsNbaLeagueGameLogFileLoader(self.data_directory)
        scoreboard_loader = StatsNbaLeagueGameLogLoader(
            self.league, self.season, self.season_type, source_loader
        )
        assert len(scoreboard_loader.items) == 1230
        assert isinstance(scoreboard_loader.items[0], StatsNbaGameItem)
        assert scoreboard_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(
            f'{self.data_directory}/schedule/stats_leaguegamelog_{self.league}_{self.season.replace("-", "_")}_{self.season_type.replace(" ", "_")}.json'
        ) as f:
            scoreboard_response = json.loads(f.read())
        base_url = f"https://stats.nba.com/stats/leaguegamelog"
        query_params = {
            "LeagueID": "00",
            "Season": self.season,
            "SeasonType": self.season_type,
            "PlayerOrTeam": "T",
            "Counter": 1000,
            "Sorter": "DATE",
            "Direction": "DESC",
        }
        scoreboard_url = furl(base_url).add(query_params).url
        responses.add(
            responses.GET, scoreboard_url, json=scoreboard_response, status=200
        )

        source_loader = StatsNbaLeagueGameLogWebLoader(self.data_directory)
        scoreboard_loader = StatsNbaLeagueGameLogLoader(
            self.league, self.season, self.season_type, source_loader
        )
        assert len(scoreboard_loader.items) == 1230
        assert isinstance(scoreboard_loader.items[0], StatsNbaGameItem)
        assert scoreboard_loader.items[0].data == self.expected_first_item_data
