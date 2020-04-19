import requests

from pbpstats.data_loader.abs_data_loader import AbsDataLoader
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase

REQUEST_TIMEOUT = 10
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
REFERER = "http://stats.nba.com/"
HEADERS = {
    'User-Agent': USER_AGENT,
    'Referer': REFERER,
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}


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
        if self.game_id[0:2] == '00':
            return 'nba'
        elif self.game_id[0:2] == '20':
            return 'gleague'
        elif self.game_id[0:2] == '10':
            return 'wnba'

    @property
    def season(self):
        """
        4th and 5th characters in game id represent season year
        ex. for 2016-17 season 4th and 5th characters would be 16
        for WNBA, season is just year, ex. 2016
        """
        digit4 = self.game_id[3]
        digit5 = self.game_id[4]
        if digit4 == '9':
            if digit5 == '9':
                return '1999' if self.league == 'wnba' else '1999-00'
            else:
                return '19' + digit4 + digit5 if self.league == 'wnba' else '19' + digit4 + digit5 + '-' + digit4 + str(int(digit5) + 1)
        elif digit5 == '9':
            return '20' + digit4 + digit5 if self.league == 'wnba' else '20' + digit4 + digit5 + '-' + str(int(digit4) + 1) + '0'
        else:
            return '20' + digit4 + digit5 if self.league == 'wnba' else '20' + digit4 + digit5 + '-' + digit4 + str(int(digit5) + 1)

    @property
    def season_type(self):
        """
        3rd character in game id represent season type
        2 for reg season, 4 for playoffs
        """
        if self.game_id[2] == "4":
            return 'Playoffs'
        elif self.game_id[2] == "2":
            return 'Regular Season'
