import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.summary.file import StatsNbaSummaryFileLoader
from pbpstats.data_loader.stats_nba.summary.loader import StatsNbaSummaryLoader
from pbpstats.data_loader.stats_nba.summary.web import StatsNbaSummaryWebLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class TestStatsSummaryLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "game_id": "0021600270",
        "date": "2016-11-30T00:00:00",
        "status": "Final",
        "home_team_id": 1610612760,
        "visitor_team_id": 1610612764,
    }

    def test_file_loader_loads_data(self):
        source_loader = StatsNbaSummaryFileLoader(self.data_directory)
        summary_loader = StatsNbaSummaryLoader(self.game_id, source_loader)
        assert len(summary_loader.items) == 1
        assert isinstance(summary_loader.items[0], StatsNbaGameItem)
        assert summary_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
        with open(
            f"{self.data_directory}/game_details/stats_summary_{self.game_id}.json"
        ) as f:
            summary_response = json.loads(f.read())
        base_url = "https://stats.nba.com/stats/boxscoresummaryv2"
        query_params = {"GameId": self.game_id}
        summary_url = furl(base_url).add(query_params).url
        responses.add(responses.GET, summary_url, json=summary_response, status=200)

        source_loader = StatsNbaSummaryWebLoader(self.data_directory)
        summary_loader = StatsNbaSummaryLoader(self.game_id, source_loader)
        assert len(summary_loader.items) == 1
        assert isinstance(summary_loader.items[0], StatsNbaGameItem)
        assert summary_loader.items[0].data == self.expected_first_item_data
