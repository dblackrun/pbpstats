# class for pulling and cleaning data from stats.nba.com api
import requests

import pbpstats
from pbpstats.game_data import GameData
from pbpstats.stats_period import StatsPeriod
from pbpstats import utils


class StatsGameData(GameData):
    """
    class for stats derived from pbp data from data.nba.com

    to get all data:
    game_data = StatsGameData('0041800406')
    game_data.get_game_data()

    to get player stats:
    player_stats = game_data.get_aggregated_possession_stats_for_entity_type('player')

    to get team stats:
    team_stats = game_data.get_aggregated_possession_stats_for_entity_type('team')

    to get opponent stats:
    opponent_stats = game_data.get_aggregated_possession_stats_for_entity_type('opponent')

    to get lineup stats:
    lineup_stats = game_data.get_aggregated_possession_stats_for_entity_type('lineup')

    to get lineup opponent stats:
    lineup_opponent_stats = game_data.get_aggregated_possession_stats_for_entity_type('lineupopponent')

    to see data for specific possession (see PossessionDetails object for specifics of what data it holds):
    print(game_data.Periods[0].Possessions[14])
    """
    def __init__(self, game_id, response_data_directory=pbpstats.DATA_DIRECTORY):
        """
        game_id - string
        response_data_directory - directory in which request response json will be stored
            defaults to DATA_DIRECTORY which is pulled from env variable PBP_STATS_DATA_DIRECTORY
        """
        self.GameId = game_id
        self.Season = utils.get_season_from_game_id(self.GameId)
        self.SeasonType = utils.get_season_type_from_game_id(self.GameId)
        self.League = utils.get_league_from_game_id(game_id)
        league_url_part = 'gleague.nba' if self.League == pbpstats.G_LEAGUE_STRING else self.League

        self.PbpBaseUrl = f'https://stats.{league_url_part}.com/stats/playbyplayv2'
        self.BoxscoreBaseUrl = f'https://stats.{league_url_part}.com/stats/boxscoretraditionalv2'
        self.SummaryBaseUrl = f'https://stats.{league_url_part}.com/stats/boxscoresummaryv2'
        self.ShotsBaseUrl = f'https://stats.{league_url_part}.com/stats/shotchartdetail'

        self.PbpFilePath = f'{response_data_directory}pbp/stats_{self.GameId}.json' if response_data_directory is not None else None
        self.BoxscoreFilePath = f'{response_data_directory}game_details/stats_boxscore_{self.GameId}.json' if response_data_directory is not None else None
        self.SummaryFilePath = f'{response_data_directory}game_details/stats_summary_{self.GameId}.json' if response_data_directory is not None else None
        self.HomeShotsFilePath = f'{response_data_directory}game_details/stats_home_shots_{self.GameId}.json' if response_data_directory is not None else None
        self.VisitorShotsFilePath = f'{response_data_directory}game_details/stats_away_shots_{self.GameId}.json' if response_data_directory is not None else None

    def __repr__(self):
        return f'<StatsGameData: {self.__dict__}>'

    def get_game_data(self, **kwargs):
        """
        gets and cleans game data from stats.nba.com
        kwargs:
        ignore_rebound_and_shot_order, default False, set to True to avoid raising possession_details.PbpEventOrderErrorException
            - do this if you don't want to fix issues with pbp and don't care about rebound stats
        ignore_back_to_back_possessions set to True to avoid raising possession_details.TeamHasBackToBackPossessionsException
            - do this if you don't want to fix issues with pbp and don't care about possession stats
        period_starters_override - dict with missing period starters
        """
        pbp_response = self.get_pbp_response()
        pbp_events_list = self.get_array_of_dicts_from_response(pbp_response, 0, dedupe=True)
        self.set_period_events(pbp_events_list)
        boxscore_response = self.get_boxscore_response()
        boxscore_players = self.get_array_of_dicts_from_response(boxscore_response, 0)
        boxscore_teams = self.get_array_of_dicts_from_response(boxscore_response, 1)
        game_summary_response = self.get_game_summary_response()
        game_summary = self.get_array_of_dicts_from_response(game_summary_response, 0)
        try:
            data_game_summary = self.convert_boxscore_to_data_game_summary(boxscore_players, boxscore_teams, game_summary)
        except IndexError:
            # some issues with stats boxscore endpoint not having results, use data boxscore
            data_game_summary = self.get_game_summary_from_data_nba_com()
        self.instantiate_team_and_player_data(data_game_summary)
        home_shots_response = self.get_shots_response(self.HomeTeamId, self.HomeShotsFilePath)
        visitor_shots_response = self.get_shots_response(self.VisitorTeamId, self.VisitorShotsFilePath)
        home_shots_list = self.get_array_of_dicts_from_response(home_shots_response, 0)
        visitor_shots_list = self.get_array_of_dicts_from_response(visitor_shots_response, 0)
        shots = home_shots_list + visitor_shots_list
        self.add_shot_locations_to_pbp(shots)
        if 'period_starters_override' in kwargs:
            self.set_period_starters(missing_period_starters=kwargs.get('period_starters_override'))
        else:
            self.set_period_starters()
        self.add_players_on_floor()
        self.add_possession_details(ignore_rebound_and_shot_order=kwargs.get('ignore_rebound_and_shot_order', False), ignore_back_to_back_possessions=kwargs.get('ignore_back_to_back_possessions', False))

    def get_pbp_response(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        """
        gets play by play response from stats.nba.com for game id
        returns request response (error if response status is not 200)
        """
        parameters = {
            'GameId': self.GameId,
            'StartPeriod': start_period,
            'EndPeriod': end_period,
            'RangeType': range_type,
            'StartRange': start_range,
            'EndRange': end_range
        }
        return utils.get_json_response(self.PbpBaseUrl, parameters, self.PbpFilePath)

    def get_boxscore_response(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        """
        gets boxscore response from stats.nba.com for game id
        returns request response (error if response status is not 200)
        """
        parameters = {
            'GameId': self.GameId,
            'StartPeriod': start_period,
            'EndPeriod': end_period,
            'RangeType': range_type,
            'StartRange': start_range,
            'EndRange': end_range
        }
        return utils.get_json_response(self.BoxscoreBaseUrl, parameters, self.BoxscoreFilePath)

    def get_game_summary_response(self):
        """
        gets game summary response from stats.nba.com for game id
        returns request response (error if response status is not 200)
        """
        parameters = {'GameId': self.GameId}
        return utils.get_json_response(self.SummaryBaseUrl, parameters, self.SummaryFilePath)

    def get_shots_response(self, team_id, file_path):
        """
        gets shots response from stats.nba.com for game id
        returns request response (error if response status is not 200)
        """
        if self.League == pbpstats.NBA_STRING:
            league_id = pbpstats.NBA_GAME_ID_PREFIX
        elif self.League == pbpstats.G_LEAGUE_STRING:
            league_id = pbpstats.G_LEAGUE_GAME_ID_PREFIX
        elif self.League == pbpstats.WNBA_STRING:
            league_id = pbpstats.WNBA_GAME_ID_PREFIX
        parameters = {
            'GameID': self.GameId,
            'Season': self.Season,
            'SeasonType': self.SeasonType,
            'TeamID': team_id,
            'PlayerID': 0,
            'Outcome': '',
            'Location': '',
            'Month': 0,
            'SeasonSegment': '',
            'DateFrom': '',
            'DateTo': '',
            'OpponentTeamID': 0,
            'VsConference': '',
            'VsDivision': '',
            'Position': '',
            'RookieYear': '',
            'GameSegment': '',
            'Period': 0,
            'LastNGames': 0,
            'ContextMeasure': 'FG_PCT',
            'PlayerPosition': '',
            'LeagueID': league_id,
        }
        return utils.get_json_response(self.ShotsBaseUrl, parameters, file_path)

    def get_array_of_dicts_from_response(self, response_json, results_set_index, dedupe=False):
        """
        creates array of dicts from pbp response json
        """
        headers = response_json['resultSets'][results_set_index]['headers']
        rows = response_json['resultSets'][results_set_index]['rowSet']
        if dedupe:
            rows = self.dedupe_events_row_set(rows)
        return [dict(zip(headers, row)) for row in rows]

    @staticmethod
    def dedupe_events_row_set(events_row_set):
        """
        dedupes list of list while preserving order
        used to dedupe events rowSets pbp response because some games have duplicate events
        """
        deduped_events_row_set = []
        for sublist in events_row_set:
            if sublist not in deduped_events_row_set:
                deduped_events_row_set.append(sublist)
        return deduped_events_row_set

    def set_period_events(self, events_list):
        """
        splits events up by period and adds score to each event before creating StatsPeriod object for each period
        """
        events_by_period = {}
        home_score = 0
        visitor_score = 0
        for event in events_list:
            period = event['PERIOD']
            if period not in events_by_period.keys():
                events_by_period[period] = []

            score = event['SCORE']
            # score is None if no points are scored when no points are scored score should be whatever it was at the most recent scoring event
            if score is not None:
                score_split = score.split(' - ')
                home_score = int(score_split[1])
                visitor_score = int(score_split[0])

            event['home_score'] = home_score
            event['visitor_score'] = visitor_score

            events_by_period[period].append(event)

        self.Periods = [StatsPeriod(events_by_period[period], self.GameId, period) for period in events_by_period.keys()]

    def convert_boxscore_to_data_game_summary(self, players, teams, game_summary):
        """
        converts stats.nba.com boxscore and game summary stats to same format as response from data.nba.com
        only need team id, abbreviation, city, name for teams
        only need player id, player name and total seconds played for players
        """
        data_game_summary = {
            'g': {
                'hls': {
                    'pstsg': []
                },
                'vls': {
                    'pstsg': []
                }
            }
        }
        date = game_summary[0]['GAME_DATE_EST'].split('T')[0]  # format for this field is 2016-11-30T00:00:00
        data_game_summary['g']['gdte'] = date

        self.HomeTeamId = game_summary[0]['HOME_TEAM_ID']
        if self.HomeTeamId == teams[1]['TEAM_ID']:
            # for some stupid reason home team and away team arent always ordered correctly
            home_index = 1
            away_index = 0
        else:
            home_index = 0
            away_index = 1

        data_game_summary['g']['hls']['tid'] = teams[home_index]['TEAM_ID']
        data_game_summary['g']['hls']['tn'] = teams[home_index]['TEAM_NAME']
        data_game_summary['g']['hls']['tc'] = teams[home_index]['TEAM_CITY']
        data_game_summary['g']['hls']['ta'] = teams[home_index]['TEAM_ABBREVIATION']

        data_game_summary['g']['vls']['tid'] = teams[away_index]['TEAM_ID']
        data_game_summary['g']['vls']['tn'] = teams[away_index]['TEAM_NAME']
        data_game_summary['g']['vls']['tc'] = teams[away_index]['TEAM_CITY']
        data_game_summary['g']['vls']['ta'] = teams[away_index]['TEAM_ABBREVIATION']

        for player in players:
            if player['MIN'] is not None:
                split = player['MIN'].split(":")  # clock is formatted mm:ss
                seconds_played = float(split[0]) * 60 + float(split[1])
                name_split = player['PLAYER_NAME'].split(' ')
                first_name = name_split[0]
                last_name = ' '.join(name_split[1:])
                player_dict = {
                    'pid': player['PLAYER_ID'],
                    'totsec': seconds_played,
                    'fn': first_name,
                    'ln': last_name
                }
                if player['TEAM_ID'] == data_game_summary['g']['hls']['tid']:
                    data_game_summary['g']['hls']['pstsg'].append(player_dict)
                else:
                    data_game_summary['g']['vls']['pstsg'].append(player_dict)
        return data_game_summary

    def add_shot_locations_to_pbp(self, shots):
        """
        itterates though each event and adds x and y coordinates to each each
        match is done by pbp event number
        args:
        shots - list of dicts with shot data for each shot
        """
        for period in self.Periods:
            for pbp_event in period.Events:
                pbp_event.loc_x = None
                pbp_event.loc_y = None
                for shot in shots:
                    if pbp_event.number == shot['GAME_EVENT_ID']:
                        pbp_event.loc_x = shot['LOC_X']
                        pbp_event.loc_y = shot['LOC_Y']

    def get_game_summary_from_data_nba_com(self):
        """
        gets game summary response from data.nba.com for game id
        only used if there is no data in stats.nba.com boxscore response
        doesn't work for games pre 2016
        returns request response (error if response status is not 200)
        """
        if self.League == pbpstats.NBA_STRING:
            season_year = self.Season.split('-')[0]
            url = (f"http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{season_year}/scores/gamedetail/{self.GameId}_gamedetail.json")
        elif self.League == pbpstats.WNBA_STRING:
            url = (f"http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/{self.Season}/scores/gamedetail/{self.GameId}_gamedetail.json")
        elif self.League == pbpstats.G_LEAGUE_STRING:
            season_year = self.Season.split('-')[0]
            url = (f"http://data.nba.com/data/10s/v2015/json/mobile_teams/dleague/{season_year}/scores/gamedetail/{self.GameId}_gamedetail.json")
        response = requests.get(url, timeout=pbpstats.REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
