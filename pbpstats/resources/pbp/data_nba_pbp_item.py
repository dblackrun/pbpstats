class DataNbaPbpItem(object):
    def __init__(self, item, period):
        self.period = period
        for key, value in item.items():
            setattr(self, key, value)

    @property
    def data(self):
        return self.__dict__
