import json
from furl import furl

import responses
from pbpstats.data_game_data import DataGameData
from pbpstats.stats_game_data import StatsGameData


class TestPbpEventConsistency:
    @responses.activate
    def test_events_are_the_same(self):
        game_id = '0021600270'
        with open('tests/data/data_game_pbp_response.json') as f:
            game_pbp_response = json.loads(f.read())

        with open('tests/data/data_game_summary_response.json') as f:
            game_summary_response = json.loads(f.read())

        game_summary_url = f'http://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/gamedetail/{game_id}_gamedetail.json'
        pbp_url = f'http://data.nba.com/data/v2015/json/mobile_teams/nba/2016/scores/pbp/{game_id}_full_pbp.json'

        responses.add(responses.GET, pbp_url, json=game_pbp_response, status=200)
        responses.add(responses.GET, game_summary_url, json=game_summary_response, status=200)

        with open('tests/data/stats_game_pbp_response.json') as f:
            game_pbp_response = json.loads(f.read())
        pbp_base_url = 'https://stats.nba.com/stats/playbyplayv2'
        pbp_query_params = {
            'EndPeriod': 10,
            'EndRange': 55800,
            'GameId': '0021600270',
            'RangeType': 2,
            'StartPeriod': 0,
            'StartRange': 0,
        }
        pbp_url = furl(pbp_base_url).add(pbp_query_params).url
        responses.add(responses.GET, pbp_url, json=game_pbp_response, status=200)

        data_game_data = DataGameData(game_id, response_data_directory=None)
        data_game_data.get_pbp_events()

        stats_game_data = StatsGameData(game_id, response_data_directory=None)
        pbp_response = stats_game_data.get_pbp_response()
        events_list = stats_game_data.get_array_of_dicts_from_response(pbp_response, 0, dedupe=True)
        stats_game_data.set_period_events(events_list)

        for period in data_game_data.Periods:
            for event in period.Events:
                evt_num = event.number
                for stats_period in stats_game_data.Periods:
                    for stats_event in stats_period.Events:
                        if evt_num == stats_event.number:
                            assert event.etype == stats_event.etype
                            assert event.mtype == stats_event.mtype
                            assert event.home_score == stats_event.home_score
                            assert event.visitor_score == stats_event.visitor_score
                            assert event.player2_id == stats_event.player2_id
                            # data pbp has seconds to tenth, stats does not
                            assert int(event.seconds_remaining) == stats_event.seconds_remaining
                            if event.is_jump_ball():
                                # for jump balls player 1 and player 3 might be swapped but they aren't used for anything so it doesn't matter
                                assert event.player_id in [stats_event.player_id, stats_event.player3_id]
                                assert event.player3_id in [stats_event.player_id, stats_event.player3_id]
                            else:
                                assert event.player_id == stats_event.player_id
                                assert event.player3_id == stats_event.player3_id
