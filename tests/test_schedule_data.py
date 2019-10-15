import json

import responses
import pbpstats
from pbpstats.schedule_data import ScheduleData


class TestScheduleData:
    @responses.activate
    def test_nba(self):
        with open('tests/data/nba_leaguegamefinder_response.json') as f:
            response = json.loads(f.read())

        url = 'https://stats.nba.com/stats/leaguegamefinder?PlayerOrTeam=T&gtPTS=1&Season=2018-19&SeasonType=Regular+Season&LeagueID=00'
        responses.add(responses.GET, url, json=response, status=200)

        schedule = ScheduleData('2018-19', pbpstats.REGULAR_SEASON_STRING, pbpstats.NBA_STRING)
        game_ids = schedule.get_all_game_ids_for_season()
        assert len(game_ids) == 1230
        assert game_ids[0] == '0021800001'

    @responses.activate
    def test_gleague(self):
        with open('tests/data/gleague_leaguegamefinder_response.json') as f:
            response = json.loads(f.read())

        url = 'https://stats.gleague.nba.com/stats/leaguegamefinder?PlayerOrTeam=T&gtPTS=1&Season=2018-19&SeasonType=Regular+Season&LeagueID=20'
        responses.add(responses.GET, url, json=response, status=200)

        schedule = ScheduleData('2018-19', pbpstats.REGULAR_SEASON_STRING, pbpstats.G_LEAGUE_STRING)
        game_ids = schedule.get_all_game_ids_for_season()
        assert len(game_ids) == 675
        assert game_ids[0] == '2021800001'

    @responses.activate
    def test_wnba(self):
        with open('tests/data/10_league_schedule_05.json') as f:
            response_05 = json.loads(f.read())
        url_05 = 'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2018/league/10_league_schedule_05.json'
        responses.add(responses.GET, url_05, json=response_05, status=200)

        with open('tests/data/10_league_schedule_06.json') as f:
            response_06 = json.loads(f.read())
        url_06 = 'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2018/league/10_league_schedule_06.json'
        responses.add(responses.GET, url_06, json=response_06, status=200)

        with open('tests/data/10_league_schedule_07.json') as f:
            response_07 = json.loads(f.read())
        url_07 = 'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2018/league/10_league_schedule_07.json'
        responses.add(responses.GET, url_07, json=response_07, status=200)

        with open('tests/data/10_league_schedule_08.json') as f:
            response_08 = json.loads(f.read())
        url_08 = 'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2018/league/10_league_schedule_08.json'
        responses.add(responses.GET, url_08, json=response_08, status=200)

        with open('tests/data/10_league_schedule_09.json') as f:
            response_09 = json.loads(f.read())
        url_09 = 'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2018/league/10_league_schedule_09.json'
        responses.add(responses.GET, url_09, json=response_09, status=200)

        with open('tests/data/10_league_schedule_10.json') as f:
            response_10 = json.loads(f.read())
        url_10 = 'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2018/league/10_league_schedule_10.json'
        responses.add(responses.GET, url_10, json=response_10, status=200)

        schedule = ScheduleData('2018', pbpstats.REGULAR_SEASON_STRING, pbpstats.WNBA_STRING)
        game_ids = schedule.get_all_game_ids_for_season()
        assert len(game_ids) == 203
        assert game_ids[0] == '1021800001'
