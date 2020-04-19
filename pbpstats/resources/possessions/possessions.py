from pbpstats.resources.base import Base


class Possessions(Base):
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        return self.__dict__
