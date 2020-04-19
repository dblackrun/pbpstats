class StatsNbaPbpItem(object):
    def __init__(self, event, order):
        for key, value in event.items():
            setattr(self, key.lower(), value)
        self.order = order

    @property
    def data(self):
        return self.__dict__
