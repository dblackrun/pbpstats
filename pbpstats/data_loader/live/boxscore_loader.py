"""
``LiveBoxscoreLoader`` loads boxscore data for a game and creates :obj:`~pbpstats.resources.boxscore.live_boxscore_item.LiveBoxscoreItem` objects for each player and team

The following code will load boxscore data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import LiveBoxscoreLoader

    boxscore_loader = LiveBoxscoreLoader("0021900001", "file", "/data")
    print(boxscore_loader.items[0].data) # prints dict with a player's boxscore data for game
"""

import json
import os

from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.live.file_loader import LiveFileLoader
from pbpstats.data_loader.live.web_loader import LiveWebLoader
from pbpstats.resources.boxscore.live_boxscore_item import LiveBoxscoreItem


class LiveBoxscoreLoader(LiveFileLoader, LiveWebLoader):
    """
    Loads data.nba.com source boxscore data for game.
    Team/Player data is stored in items attribute as :obj:`~pbpstats.resources.boxscore.live_boxscore_item.LiveBoxscoreItem` objects

    :param str game_id: NBA Stats Game Id
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `live_<game_id>.json` in the `/game_details` subdirectory.
        If not provided response data will not be saved on disk.
    """

    data_provider = "live"
    resource = "Boxscore"
    parent_object = "Game"

    def __init__(self, game_id, source, file_directory=None):
        self.game_id = game_id
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_boxscore_items()

    def _load_data(self):
        source_method = getattr(self, f"_from_{self.source}")
        source_method()

    @check_file_directory
    def _from_file(self):
        self.file_path = f"{self.file_directory}/game_details/live_{self.game_id}.json"
        self._load_data_from_file()

    def _from_web(self):
        self.url = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{self.game_id}.json"
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f"{self.file_directory}/game_details/live_{self.game_id}.json"
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)

    def _make_boxscore_items(self):
        """
        makes :obj:`~pbpstats.resources.boxscore.LiveBoxscoreItem` items for each player/team
        """
        home = self.data["homeTeam"]
        away = self.data["awayTeam"]
        self.items = [
            LiveBoxscoreItem(
                item, team_id=away["teamId"], team_abbreviation=away["teamTricode"]
            )
            for item in away["players"]
        ]
        self.items += [
            LiveBoxscoreItem(
                item, team_id=home["teamId"], team_abbreviation=home["teamTricode"]
            )
            for item in home["players"]
        ]
        self.items.append(
            LiveBoxscoreItem(
                away["statistics"],
                team_id=away["teamId"],
                team_abbreviation=away["teamTricode"],
            )
        )
        self.items.append(
            LiveBoxscoreItem(
                home["statistics"],
                team_id=home["teamId"],
                team_abbreviation=home["teamTricode"],
            )
        )

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["game"]
