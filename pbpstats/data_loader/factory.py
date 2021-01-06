"""
``DataLoaderFactory`` can be used to create data loader objects from the ``data_loader`` module.

The following code will create a data loader object for loading enhanced pbp from stats.nba.com.

.. code-block:: python

    from pbpstats.data_loader.factory import DataLoaderFactory

    data_loader = DataLoaderFactory()
    stats_enhanced_pbp_data_loader = data_loader.get_data_loader("stats_nba", "EnhancedPbp")
    print(stats_enhanced_pbp_data_loader[0])
    # prints "<class 'pbpstats.data_loader.stats_nba.enhanced_pbp_loader.StatsNbaEnhancedPbpLoader'>"
"""

from collections import defaultdict

import pbpstats.data_loader as data_loader


class DataLoaderFactory(object):
    """
    Class for factory of data loader classes. On initialization will load in all data loader classes in ``data_loader`` module
    """

    def __init__(self):
        self.loaders = defaultdict(lambda: defaultdict(lambda: []))
        self._load_data_loaders()

    def _load_data_loaders(self):
        """
        loads data loaders from data_loader package
        """
        loaders = dict(
            [
                (name, cls)
                for name, cls in data_loader.__dict__.items()
                if isinstance(cls, type)
            ]
        )
        for _, loader_cls in loaders.items():
            self.loaders[loader_cls.resource][loader_cls.data_provider].append(
                loader_cls
            )

    def get_data_loader(self, data_provider, resource):
        """
        Gets data loader classes for given data provider and resource.

        :param str data_provider: Which data provider should data be loaded from. Options are 'stats_nba' or 'data_nba' or 'live'
        :param str resource: Name of class from resources directory

        :return: list of data loader classes
        :rtype: list
        """
        return self.loaders[resource][data_provider]
