class StatsNbaShot(object):
    def __init__(self, item):
        for key, value in item.items():
            setattr(self, key.lower(), value)

    @property
    def data(self):
        return self.__dict__
