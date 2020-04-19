import inspect

import pbpstats.client as client


class Day(object):
    def __init__(self, date, league):
        """
        date format - 'MM/DD/YYYY
        """
        self.date = date
        self.league = league
        attributes = inspect.getmembers(self, lambda a: not(inspect.isroutine(a)))
        data_loaders = [a for a in attributes if a[0].endswith(client.DATA_LOADER_SUFFIX)]
        data_source_map = {a[0].replace(client.DATA_SOURCE_SUFFIX, ''): a[1] for a in attributes if a[0].endswith(client.DATA_SOURCE_SUFFIX)}
        for data_loader in data_loaders:
            attr_name = data_loader[0].replace(client.DATA_LOADER_SUFFIX, '')
            source = data_source_map[attr_name]
            data = data_loader[1](date, league, self.data_directory, source)
            resource_cls = getattr(self, attr_name)
            setattr(self, client.PATTERN.sub('_', attr_name).lower(), resource_cls(data.items))
