from pbpstats.data_loader.data_nba.schedule_loader import DataNbaScheduleLoader
from pbpstats.objects.season import Season
from pbpstats.resources.games.games import Games


def test_season_init_loads_data():
    season_cls = Season
    season_cls.Games = Games
    season_cls.GamesDataLoaderClass = DataNbaScheduleLoader
    season_cls.GamesDataSource = 'file'
    season_cls.data_directory = 'tests/data'

    league = 'wnba'
    season = '2019'
    season_type = 'Regular Season'

    season = season_cls(league, season, season_type)
    assert len(season.games.items) == 204
