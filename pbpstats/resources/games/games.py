from pbpstats.resources.base import Base


class Games(Base):
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        return [item.data for item in self.items]

    @property
    def final_games(self):
        return [item.data for item in self.items if item.is_final]
