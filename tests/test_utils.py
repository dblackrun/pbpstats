import pbpstats
from pbpstats import utils


def test_swap_team_id_for_game():
    team1 = 'a'
    team2 = 'b'
    teams = [team1, team2]
    assert utils.swap_team_id_for_game(team1, teams) == 'b'
    assert utils.swap_team_id_for_game(team2, teams) == 'a'


def test_generate_lineup_ids():
    current_players_str = {'1': ['3', '4', '5', '2', '7'], '2': ['11', '9', '6', '12', '14']}
    current_players_int = {'1': [3, 4, 5, 2, 7], '2': [11, 9, 6, 12, 14]}
    expected_lineup_ids = {
        '1': '2-3-4-5-7',
        '2': '11-12-14-6-9'
    }
    assert utils.generate_lineup_ids(current_players_str) == expected_lineup_ids
    assert utils.generate_lineup_ids(current_players_int) == expected_lineup_ids


def test_get_season_from_game_id():
    assert utils.get_season_from_game_id('0021600001') == '2016-17'
    assert utils.get_season_from_game_id('0041600001') == '2016-17'
    assert utils.get_season_from_game_id('0020900001') == '2009-10'
    assert utils.get_season_from_game_id('0049900001') == '1999-00'
    assert utils.get_season_from_game_id('1021600001') == '2016'
    assert utils.get_season_from_game_id('1029900001') == '1999'
    assert utils.get_season_from_game_id('0049800001') == '1998-99'
    assert utils.get_season_from_game_id('1029800001') == '1998'
    assert utils.get_season_from_game_id('1020900001') == '2009'


def test_get_season_type_from_game_id():
    assert utils.get_season_type_from_game_id('0021600001') == 'Regular Season'
    assert utils.get_season_type_from_game_id('0041600001') == 'Playoffs'
    assert utils.get_season_type_from_game_id('0031600001') is None


def test_get_league_from_game_id():
    assert utils.get_league_from_game_id('0021600001') == pbpstats.NBA_STRING
    assert utils.get_league_from_game_id('2041600001') == pbpstats.G_LEAGUE_STRING
    assert utils.get_league_from_game_id('4031600001') is None
