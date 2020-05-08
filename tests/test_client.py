import pytest

from pbpstats.client import Client
from pbpstats.data_loader.stats_nba.boxscore_loader import StatsNbaBoxscoreLoader
from pbpstats.resources.boxscore.boxscore import Boxscore


def test_client_sets_object_attrs():
    settings = {}
    client = Client(settings)
    assert hasattr(client, 'Game')
    assert hasattr(client, 'Day')
    assert hasattr(client, 'Season')


def test_client_sets_data_directory():
    settings = {
        'dir': 'tmp',
    }
    client = Client(settings)
    assert client.data_directory == settings['dir']


def test_client_sets_resource():
    settings = {
        'dir': 'tmp',
        'Boxscore': {'source': 'file', 'data_provider': 'stats_nba'},
    }
    client = Client(settings)
    assert client.Game.BoxscoreDataLoaderClass == StatsNbaBoxscoreLoader
    assert client.Game.BoxscoreDataSource == settings['Boxscore']['source']
    assert client.Game.Boxscore == Boxscore


def test_client_loads_data():
    settings = {
        'dir': 'tests/data',
        'Boxscore': {'source': 'file', 'data_provider': 'stats_nba'},
    }
    client = Client(settings)
    game = client.Game('0021600270')
    assert len(game.boxscore.items) > 0


def test_value_error_raised_when_dir_missing():
    settings = {
        'Boxscore': {'source': 'file', 'data_provider': 'data_nba'},
    }
    client = Client(settings)
    with pytest.raises(ValueError):
        assert client.Game('0021600270')
