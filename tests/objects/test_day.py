from pbpstats.data_loader.stats_nba.scoreboard_loader import StatsNbaScoreboardLoader
from pbpstats.objects.day import Day
from pbpstats.resources.games.games import Games


def test_day_init_loads_data():
    day_cls = Day
    day_cls.Games = Games
    day_cls.GamesDataLoaderClass = StatsNbaScoreboardLoader
    day_cls.GamesDataSource = "file"
    day_cls.data_directory = "tests/data"

    date = "02/25/2020"
    league = "gleague"

    day = day_cls(date, league)
    assert len(day.games.items) == 7
