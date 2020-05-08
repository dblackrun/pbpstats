from pbpstats.resources.boxscore.boxscore import Boxscore
from pbpstats.resources.boxscore.stats_nba_boxscore_item import StatsNbaBoxscoreItem


class TestBoxscoreResource:
    items = [
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 1,
                "team_abbreviation": "ABC",
                "player_id": 909,
                "name": "Player1 Name1",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 1,
                "team_abbreviation": "ABC",
                "player_id": 908,
                "name": "Player2 Name2",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 1,
                "team_abbreviation": "ABC",
                "player_id": 907,
                "name": "Player3 Name3",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 1,
                "team_abbreviation": "ABC",
                "player_id": 906,
                "name": "Player4 Name4",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 1,
                "team_abbreviation": "ABC",
                "player_id": 905,
                "name": "Player5 Name5",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 2,
                "team_abbreviation": "DEF",
                "player_id": 904,
                "name": "Player6 Name6",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 2,
                "team_abbreviation": "DEF",
                "player_id": 903,
                "name": "Player7 Name7",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 2,
                "team_abbreviation": "DEF",
                "player_id": 902,
                "name": "Player8 Name8",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 2,
                "team_abbreviation": "DEF",
                "player_id": 901,
                "name": "Player9 Name9",
            }
        ),
        StatsNbaBoxscoreItem(
            {
                "game_id": "1",
                "team_id": 2,
                "team_abbreviation": "DEF",
                "player_id": 900,
                "name": "Player10 Name10",
            }
        ),
        StatsNbaBoxscoreItem(
            {"game_id": "1", "team_id": 2, "team_abbreviation": "DEF"}
        ),
        StatsNbaBoxscoreItem(
            {"game_id": "1", "team_id": 1, "team_abbreviation": "ABC"}
        ),
    ]
    boxscore = Boxscore(items)

    def test_player_data(self):
        assert len(self.boxscore.data["player"]) == 10

    def test_team_data(self):
        assert len(self.boxscore.data["team"]) == 2

    def test_player_name_map(self):
        assert self.boxscore.player_name_map[909] == "Player1 Name1"

    def test_player_team_map(self):
        assert self.boxscore.player_team_map[909] == 1
