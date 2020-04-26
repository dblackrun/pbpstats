KEY_ATTR_MAPPER = {
    'gid': 'game_id',
    'gdte': 'date',
    'stt': 'status',
}


class DataNbaGameItem(object):
    def __init__(self, item):
        for key, value in KEY_ATTR_MAPPER.items():
            if item.get(key) is not None:
                setattr(self, value, item.get(key))
        self.home_team_id = item['h']['tid']
        self.home_team_abbreviation = item['h']['ta']
        self.home_score = item['h']['s']
        self.away_team_id = item['v']['tid']
        self.away_team_abbreviation = item['v']['ta']
        self.away_score = item['v']['s']

    @property
    def data(self):
        return self.__dict__

    @property
    def is_final(self):
        return self.status == 'Final'
