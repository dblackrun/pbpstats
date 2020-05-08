"""
Instantiating a ``Game`` object will load all resources for the ``Game``
object that were set in the settings when the client was instantiated

The following code will instantiate the client and get possession data
for game id 0021900001 from files in ``/response_data`` subdirectories

.. code-block:: python

    from pbpstats.client import Client

    settings = {
        "dir": "/response_data",
        "Possessions": {"source": "file", "data_provider": "stats_nba"}
    }
    client = Client(settings)
    game = client.Game('0021900001')
    for possession in game.possessions.items:
        print(possession)
"""
import inspect

import pbpstats.client as client


class Game(object):
    """
    Class for loading resource data from data loaders with a ``parent_object`` of ``Game``

    :param str game_id: NBA Stats Game Id
    """

    def __init__(self, game_id):
        self.game_id = game_id
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        data_loaders = [
            a for a in attributes if a[0].endswith(client.DATA_LOADER_SUFFIX)
        ]
        data_source_map = {
            a[0].replace(client.DATA_SOURCE_SUFFIX, ""): a[1]
            for a in attributes
            if a[0].endswith(client.DATA_SOURCE_SUFFIX)
        }
        for data_loader in data_loaders:
            attr_name = data_loader[0].replace(client.DATA_LOADER_SUFFIX, "")
            source = data_source_map[attr_name]
            data = data_loader[1](game_id, source, self.data_directory)
            resource_cls = getattr(self, attr_name)
            setattr(
                self,
                client.PATTERN.sub("_", attr_name).lower(),
                resource_cls(data.items),
            )
