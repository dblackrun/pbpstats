from pbpstats.data_loader.stats_nba.boxscore.file import StatsNbaBoxscoreFileLoader
from pbpstats.data_loader.stats_nba.boxscore.loader import StatsNbaBoxscoreLoader
from pbpstats.objects.game import Game
from pbpstats.resources.boxscore.boxscore import Boxscore


def test_game_init_loads_data():
    game_cls = Game
    game_cls.Boxscore = Boxscore
    game_cls.BoxscoreDataLoaderClass = StatsNbaBoxscoreLoader
    game_cls.BoxscoreDataSource = StatsNbaBoxscoreFileLoader
    game_cls.data_directory = "tests/data"

    game_id = "0021600270"

    game = game_cls(game_id)
    assert len(game.boxscore.items) == 21
