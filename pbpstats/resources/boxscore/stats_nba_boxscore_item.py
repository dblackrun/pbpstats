OVERRIDES = {
    'PLAYER_NAME': 'name',
}


class StatsNbaBoxscoreItem(object):
    def __init__(self, item):
        for key, value in item.items():
            setattr(self, OVERRIDES.get(key, key.lower()), value)

    @property
    def data(self):
        return self.__dict__
