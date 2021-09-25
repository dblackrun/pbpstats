"""
``LiveBoxscoreLoader`` loads boxscore data for a game and creates :obj:`~pbpstats.resources.boxscore.live_boxscore_item.LiveBoxscoreItem` objects for each player and team

The following code will load boxscore data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import LiveBoxscoreFileLoader, LiveBoxscoreLoader

    source_loader = LiveBoxscoreFileLoader("/data")
    boxscore_loader = LiveBoxscoreLoader("0021900001", source_loader)
    print(boxscore_loader.items[0].data) # prints dict with a player's boxscore data for game
"""
from pbpstats.data_loader.live.base import LiveLoaderBase
from pbpstats.resources.boxscore.live_boxscore_item import LiveBoxscoreItem


class LiveBoxscoreLoader(LiveLoaderBase):
    """
    Loads data.nba.com source boxscore data for game.
    Team/Player data is stored in items attribute as :obj:`~pbpstats.resources.boxscore.live_boxscore_item.LiveBoxscoreItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.live.boxscore.file.LiveBoxscoreFileLoader` or :obj:`~pbpstats.data_loader.live.boxscore.web.LiveBoxscoreWebLoader` object
    """

    data_provider = "live"
    resource = "Boxscore"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self._make_boxscore_items()

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
