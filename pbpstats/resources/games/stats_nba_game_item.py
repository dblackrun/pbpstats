KEY_ATTR_MAPPER = {
    'GAME_ID': 'game_id',
    'GAME_DATE_EST': 'date',
    'HOME_TEAM_ID': 'home_team_id',
    'VISITOR_TEAM_ID': 'visitor_team_id',
    'GAME_STATUS_TEXT': 'status'
}


class StatsNbaGameItem(object):
    def __init__(self, item):
        for key, value in KEY_ATTR_MAPPER.items():
            if item.get(key) is not None:
                setattr(self, value, item.get(key))

    @property
    def data(self):
        return self.__dict__

    @property
    def is_final(self):
        return self.status == 'Final'
