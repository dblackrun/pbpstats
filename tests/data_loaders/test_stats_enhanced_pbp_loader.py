import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.enhanced_pbp.file import StatsNbaEnhancedPbpFileLoader
from pbpstats.data_loader.stats_nba.enhanced_pbp.loader import StatsNbaEnhancedPbpLoader
from pbpstats.data_loader.stats_nba.enhanced_pbp.web import StatsNbaEnhancedPbpWebLoader
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)


class TestStatsEnhancedPbpLoader:
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
        "video_available": 0,
        "description": "",
        "team_id": 0,
        "order": 0,
        "previous_event": None,
        "next_event": "<StatsJumpBall GameId: 0021600270, Description: Jump Ball Adams vs. Gortat: Tip to Mark Morris, Time: 12:00, EventNum: 1>",
        "team_starting_with_ball": 1610612764,
        "period_starters": {
            1610612760: [203500, 1627734, 203506, 201566, 203460],
            1610612764: [202693, 101162, 202322, 203078, 203490],
        },
    }

    def test_file_loader_loads_data(self):
        source_loader = StatsNbaEnhancedPbpFileLoader(self.data_directory)
        pbp_loader = StatsNbaEnhancedPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 540
        assert isinstance(pbp_loader.items[0], StatsEnhancedPbpItem)
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
            pbp_loader.items[0].data["video_available"]
            == self.expected_first_item_data["video_available"]
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
            pbp_loader.items[0].data["order"] == self.expected_first_item_data["order"]
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
        with open(f"{self.data_directory}/pbp/stats_{self.game_id}.json") as f:
            pbp_response = json.loads(f.read())
        base_url = "https://stats.nba.com/stats/playbyplayv2"
        query_params = {
            "GameId": self.game_id,
            "StartPeriod": 0,
            "EndPeriod": 10,
            "RangeType": 2,
            "StartRange": 0,
            "EndRange": 55800,
        }
        pbp_url = furl(base_url).add(query_params).url
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        with open(
            f"{self.data_directory}/game_details/stats_home_shots_{self.game_id}.json"
        ) as f:
            home_response = json.loads(f.read())
        with open(
            f"{self.data_directory}/game_details/stats_away_shots_{self.game_id}.json"
        ) as f:
            away_response = json.loads(f.read())
        base_url = "https://stats.nba.com/stats/shotchartdetail"
        home_query_params = {
            "GameID": self.game_id,
            "TeamID": 1610612760,
            "Season": "2016-17",
            "SeasonType": "Regular Season",
            "PlayerID": 0,
            "Outcome": "",
            "Location": "",
            "Month": 0,
            "SeasonSegment": "",
            "DateFrom": "",
            "DateTo": "",
            "OpponentTeamID": 0,
            "VsConference": "",
            "VsDivision": "",
            "Position": "",
            "RookieYear": "",
            "GameSegment": "",
            "Period": 0,
            "LastNGames": 0,
            "ContextMeasure": "FG_PCT",
            "PlayerPosition": "",
            "LeagueID": "00",
        }
        away_query_params = {
            "GameID": self.game_id,
            "TeamID": 1610612764,
            "Season": "2016-17",
            "SeasonType": "Regular Season",
            "PlayerID": 0,
            "Outcome": "",
            "Location": "",
            "Month": 0,
            "SeasonSegment": "",
            "DateFrom": "",
            "DateTo": "",
            "OpponentTeamID": 0,
            "VsConference": "",
            "VsDivision": "",
            "Position": "",
            "RookieYear": "",
            "GameSegment": "",
            "Period": 0,
            "LastNGames": 0,
            "ContextMeasure": "FG_PCT",
            "PlayerPosition": "",
            "LeagueID": "00",
        }
        home_url = furl(base_url).add(home_query_params).url
        away_url = furl(base_url).add(away_query_params).url
        responses.add(responses.GET, home_url, json=home_response, status=200)
        responses.add(responses.GET, away_url, json=away_response, status=200)

        with open(
            f"{self.data_directory}/game_details/stats_summary_{self.game_id}.json"
        ) as f:
            summary_response = json.loads(f.read())
        summary_base_url = "https://stats.nba.com/stats/boxscoresummaryv2"
        query_params = {"GameId": self.game_id}
        summary_url = furl(summary_base_url).add(query_params).url
        responses.add(responses.GET, summary_url, json=summary_response, status=200)

        with open(f"{self.data_directory}/period_starters_boxscore_response.json") as f:
            starters_response = json.loads(f.read())
        boxscore_base_url = "https://stats.nba.com/stats/boxscoretraditionalv2"
        starters_query_params = {
            "GameId": self.game_id,
            "StartPeriod": 0,
            "EndPeriod": 0,
            "RangeType": 2,
            "StartRange": 28800,
            "EndRange": 28940,
        }
        starters_url = furl(boxscore_base_url).add(starters_query_params).url
        responses.add(responses.GET, starters_url, json=starters_response, status=200)

        file_directory = None
        source_loader = StatsNbaEnhancedPbpWebLoader(file_directory)
        pbp_loader = StatsNbaEnhancedPbpLoader(self.game_id, source_loader)
        assert len(pbp_loader.items) == 540
        assert isinstance(pbp_loader.items[0], StatsEnhancedPbpItem)
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
            pbp_loader.items[0].data["video_available"]
            == self.expected_first_item_data["video_available"]
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
            pbp_loader.items[0].data["order"] == self.expected_first_item_data["order"]
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

    def test_web_loader_with_events_out_of_order_loads_data(self):
        game_id = "0021900001"
        with open(f"{self.data_directory}/pbp/raw_stats_{game_id}.json") as f:
            pbp_response = json.loads(f.read())
        base_url = "https://stats.nba.com/stats/playbyplayv2"
        query_params = {
            "GameId": game_id,
            "StartPeriod": 0,
            "EndPeriod": 10,
            "RangeType": 2,
            "StartRange": 0,
            "EndRange": 55800,
        }
        pbp_url = furl(base_url).add(query_params).url
        responses.add(responses.GET, pbp_url, json=pbp_response, status=200)

        with open(
            f"{self.data_directory}/game_details/stats_home_shots_{game_id}.json"
        ) as f:
            home_response = json.loads(f.read())
        with open(
            f"{self.data_directory}/game_details/stats_away_shots_{game_id}.json"
        ) as f:
            away_response = json.loads(f.read())
        base_url = "https://stats.nba.com/stats/shotchartdetail"
        home_query_params = {
            "GameID": game_id,
            "TeamID": 1610612761,
            "Season": "2016-17",
            "SeasonType": "Regular Season",
            "PlayerID": 0,
            "Outcome": "",
            "Location": "",
            "Month": 0,
            "SeasonSegment": "",
            "DateFrom": "",
            "DateTo": "",
            "OpponentTeamID": 0,
            "VsConference": "",
            "VsDivision": "",
            "Position": "",
            "RookieYear": "",
            "GameSegment": "",
            "Period": 0,
            "LastNGames": 0,
            "ContextMeasure": "FG_PCT",
            "PlayerPosition": "",
            "LeagueID": "00",
        }
        away_query_params = {
            "GameID": game_id,
            "TeamID": 1610612740,
            "Season": "2016-17",
            "SeasonType": "Regular Season",
            "PlayerID": 0,
            "Outcome": "",
            "Location": "",
            "Month": 0,
            "SeasonSegment": "",
            "DateFrom": "",
            "DateTo": "",
            "OpponentTeamID": 0,
            "VsConference": "",
            "VsDivision": "",
            "Position": "",
            "RookieYear": "",
            "GameSegment": "",
            "Period": 0,
            "LastNGames": 0,
            "ContextMeasure": "FG_PCT",
            "PlayerPosition": "",
            "LeagueID": "00",
        }
        home_url = furl(base_url).add(home_query_params).url
        away_url = furl(base_url).add(away_query_params).url
        responses.add(responses.GET, home_url, json=home_response, status=200)
        responses.add(responses.GET, away_url, json=away_response, status=200)

        with open(
            f"{self.data_directory}/game_details/stats_summary_{game_id}.json"
        ) as f:
            summary_response = json.loads(f.read())
        summary_base_url = "https://stats.nba.com/stats/boxscoresummaryv2"
        query_params = {"GameId": self.game_id}
        summary_url = furl(summary_base_url).add(query_params).url
        responses.add(responses.GET, summary_url, json=summary_response, status=200)

        with open(f"{self.data_directory}/period_starters_boxscore_response.json") as f:
            starters_response = json.loads(f.read())
        boxscore_base_url = "https://stats.nba.com/stats/boxscoretraditionalv2"
        starters_query_params = {
            "GameId": self.game_id,
            "StartPeriod": 0,
            "EndPeriod": 0,
            "RangeType": 2,
            "StartRange": 28800,
            "EndRange": 28940,
        }
        starters_url = furl(boxscore_base_url).add(starters_query_params).url
        responses.add(responses.GET, starters_url, json=starters_response, status=200)

        file_directory = None
        source_loader = StatsNbaEnhancedPbpWebLoader(file_directory)
        pbp_loader = StatsNbaEnhancedPbpLoader(game_id, source_loader)
        assert len(pbp_loader.items) == 573
