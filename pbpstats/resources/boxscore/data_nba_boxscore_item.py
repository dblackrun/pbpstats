OVERRIDES = {
    'pid': 'player_id'
}


class DataNbaBoxscoreItem(object):
    def __init__(self, item, team_id=None, team_abbreviation=None):
        self.team_id = team_id
        self.team_abbreviation = team_abbreviation
        for key, value in item.items():
            setattr(self, OVERRIDES.get(key, key), value)
        if hasattr(self, 'fn') and hasattr(self, 'ln'):
            self.name = f'{self.fn} {self.ln}'

    @property
    def data(self):
        return self.__dict__
