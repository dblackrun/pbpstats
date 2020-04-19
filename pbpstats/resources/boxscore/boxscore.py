from pbpstats.resources.base import Base


class Boxscore(Base):
    def __init__(self, items):
        self.items = items

    @property
    def data(self):
        return {'player': self.player_items, 'team': self.team_items}

    @property
    def player_items(self):
        return [item.data for item in self.items if hasattr(item, 'player_id')]

    @property
    def team_items(self):
        return [item.data for item in self.items if not hasattr(item, 'player_id')]

    @property
    def player_name_map(self):
        return {item['player_id']: item['name'] for item in self.player_items}

    @property
    def player_team_map(self):
        return {item['player_id']: item['team_id'] for item in self.player_items}
