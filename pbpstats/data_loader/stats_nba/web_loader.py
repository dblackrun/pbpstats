import requests

from pbpstats import (
    NBA_STRING, G_LEAGUE_STRING, WNBA_STRING, PLAYOFFS_STRING, REGULAR_SEASON_STRING,
    NBA_GAME_ID_PREFIX, G_LEAGUE_GAME_ID_PREFIX, WNBA_GAME_ID_PREFIX
)
from pbpstats import HEADERS, REQUEST_TIMEOUT
from pbpstats.data_loader.abs_data_loader import AbsDataLoader
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase


class StatsNbaWebLoader(AbsDataLoader, StatsNbaLoaderBase):
    """
    base class for loading data from stats.nba.com api endpoint
    should not be called directly
    """
    def _load_request_data(self):
        response = requests.get(self.base_url, self.parameters, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            self.source_data = response.json()
            self._save_data_to_file()
        else:
            response.raise_for_status()

    @property
    def data(self):
        return self.make_list_of_dicts()

    @property
    def league(self):
        """
        First 2 in game id represent league
        00 for nba, 10 for wnba, 20 for g-league
        """
        if self.game_id[0:2] == NBA_GAME_ID_PREFIX:
            return NBA_STRING
        elif self.game_id[0:2] == G_LEAGUE_GAME_ID_PREFIX:
            return G_LEAGUE_STRING
        elif self.game_id[0:2] == WNBA_GAME_ID_PREFIX:
            return WNBA_STRING

    @property
    def season(self):
        """
        4th and 5th characters in game id represent season year
        ex. for 2016-17 season 4th and 5th characters would be 16
        for WNBA, season is just year, ex. 2016
        """
        digit4 = int(self.game_id[3])
        digit5 = int(self.game_id[4])
        if digit4 == 9:
            if digit5 == 9:
                return '1999' if self.league == WNBA_STRING else '1999-00'
            else:
                return f'19{digit4}{digit5}' if self.league == WNBA_STRING else f'19{digit4}{digit5}-{digit4}{digit5 + 1}'
        elif digit5 == 9:
            return f'20{digit4}{digit5}' if self.league == WNBA_STRING else f'20{digit4}{digit5}-{digit4 + 1}0'
        else:
            return f'20{digit4}{digit5}'if self.league == WNBA_STRING else f'20{digit4}{digit5}-{digit4}{digit5 + 1}'

    @property
    def season_type(self):
        """
        3rd character in game id represent season type
        2 for reg season, 4 for playoffs
        """
        if self.game_id[2] == "4":
            return PLAYOFFS_STRING
        elif self.game_id[2] == "2":
            return REGULAR_SEASON_STRING
