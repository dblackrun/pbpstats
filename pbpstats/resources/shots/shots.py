from pbpstats.resources.base import Base


class Shots(Base):
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        return [item.data for item in self.items]
