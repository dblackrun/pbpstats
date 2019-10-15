# class for pulling and cleaning data from data.nba.com api
import requests
import pbpstats

from pbpstats import utils
from pbpstats.game_data import GameData
from pbpstats.data_period import DataPeriod


class DataGameData(GameData):
    """
    class for stats derived from pbp data from data.nba.com

    to get all data:
    game_data = DataGameData('0041800406')
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
        self.PbpFilePath = f'{response_data_directory}pbp/data_{self.GameId}.json' if response_data_directory is not None else None
        if self.League == pbpstats.NBA_STRING:
            season_year = self.Season.split('-')[0]
            self.PbpUrl = (f"http://data.nba.com/data/v2015/json/mobile_teams/nba/{season_year}/scores/pbp/{self.GameId}_full_pbp.json")
            self.GameDetailUrl = (f"http://data.nba.com/data/v2015/json/mobile_teams/nba/{season_year}/scores/gamedetail/{self.GameId}_gamedetail.json")
        elif self.League == pbpstats.WNBA_STRING:
            self.PbpUrl = (f"http://data.wnba.com/data/v2015/json/mobile_teams/wnba/{self.Season}/scores/pbp/{self.GameId}_full_pbp.json")
            self.GameDetailUrl = (f"http://data.wnba.com/data/v2015/json/mobile_teams/wnba/{self.Season}/scores/gamedetail/{self.GameId}_gamedetail.json")
        elif self.League == pbpstats.G_LEAGUE_STRING:
            season_year = self.Season.split('-')[0]
            self.PbpUrl = (f"http://data.nba.com/data/v2015/json/mobile_teams/dleague/{season_year}/scores/pbp/{self.GameId}_full_pbp.json")
            self.GameDetailUrl = (f"http://data.nba.com/data/v2015/json/mobile_teams/dleague/{season_year}/scores/gamedetail/{self.GameId}_gamedetail.json")

    def __repr__(self):
        return f'<DataGameData: {self.__dict__}>'

    def get_game_data(self, **kwargs):
        """
        gets and cleans game data from data.nba.com
        kwargs:
        ignore_rebound_and_shot_order, default False, set to True to avoid raising possession_details.PbpEventOrderErrorException
            - do this if you don't want to fix issues with pbp and don't care about rebound stats
        period_starters_override - dict with missing period starters
        """
        game_summary_json = self.get_game_summary_response_json()
        self.get_pbp_events()
        self.instantiate_team_and_player_data(game_summary_json)
        if 'period_starters_override' in kwargs:
            self.set_period_starters(missing_period_starters=kwargs.get('period_starters_override'))
        else:
            self.set_period_starters()
        self.add_players_on_floor()
        self.add_possession_details(ignore_rebound_and_shot_order=kwargs.get('ignore_rebound_and_shot_order', False))

    def get_pbp_events(self):
        """
        Sets:
        Periods - list of DataPeriod objects
        """
        response_json = utils.get_json_response(self.PbpUrl, {}, self.PbpFilePath)
        game_periods = response_json['g']['pd']
        # verify pbp is complete
        last_period = game_periods[-1]
        last_event = last_period['pla'][-1]
        if last_event['de'] not in ['Game End', 'End Period']:
            raise Exception(f"Last event is not game end: GameId: {self.GameId}")
        self.Periods = [DataPeriod(period['pla'], self.GameId, period['p']) for period in game_periods]

    def get_game_summary_response_json(self):
        """
        gets game summary response from data.nba.com for game id

        returns request response (error if response status is not 200)
        """
        response = requests.get(self.GameDetailUrl, timeout=pbpstats.REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
