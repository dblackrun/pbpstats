from collections import defaultdict

import pbpstats.data_loader as data_loader


class DataLoaderFactory(object):
    def __init__(self):
        self.loaders = defaultdict(lambda: defaultdict(lambda: []))
        self._load_data_loaders()

    def _load_data_loaders(self):
        """
        loads data loaders from data_loader package
        """
        loaders = dict([(name, cls) for name, cls in data_loader.__dict__.items() if isinstance(cls, type)])
        for _, loader_cls in loaders.items():
            self.loaders[loader_cls.resource][loader_cls.data_provider].append(loader_cls)

    def get_data_loader(self, data_provider, resource):
        """
        data_provider - stats/data
        resource - name of class from resources directory
        """
        return self.loaders[resource][data_provider]
