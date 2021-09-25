import json

import responses
from furl import furl

from pbpstats.data_loader.stats_nba.shots.file import StatsNbaShotsFileLoader
from pbpstats.data_loader.stats_nba.shots.loader import StatsNbaShotsLoader
from pbpstats.data_loader.stats_nba.shots.web import StatsNbaShotsWebLoader
from pbpstats.resources.shots.stats_nba_shot import StatsNbaShot


class TestStatsShotsLoader:
    game_id = "0021600270"
    data_directory = "tests/data"
    expected_first_item_data = {
        "grid_type": "Shot Chart Detail",
        "game_id": "0021600270",
        "game_event_id": 3,
        "player_id": 1627734,
        "player_name": "Domantas Sabonis",
        "team_id": 1610612760,
        "team_name": "Oklahoma City Thunder",
        "period": 1,
        "minutes_remaining": 11,
        "seconds_remaining": 18,
        "event_type": "Made Shot",
        "action_type": "Jump Shot",
        "shot_type": "2PT Field Goal",
        "shot_zone_basic": "Mid-Range",
        "shot_zone_area": "Left Side(L)",
        "shot_zone_range": "8-16 ft.",
        "shot_distance": 12,
        "loc_x": -120,
        "loc_y": 46,
        "shot_attempted_flag": 1,
        "shot_made_flag": 1,
        "game_date": "20161130",
        "htm": "OKC",
        "vtm": "WAS",
    }

    def test_file_loader_loads_data(self):
        source_loader = StatsNbaShotsFileLoader(self.data_directory)
        shots_loader = StatsNbaShotsLoader(self.game_id, source_loader)
        assert len(shots_loader.items) == 193
        assert isinstance(shots_loader.items[0], StatsNbaShot)
        assert shots_loader.items[0].data == self.expected_first_item_data

    @responses.activate
    def test_web_loader_loads_data(self):
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

        source_loader = StatsNbaShotsWebLoader(self.data_directory)
        shots_loader = StatsNbaShotsLoader(self.game_id, source_loader)
        assert len(shots_loader.items) == 193
        assert isinstance(shots_loader.items[0], StatsNbaShot)
        assert shots_loader.items[0].data == self.expected_first_item_data
