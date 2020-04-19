from pbpstats.data_loader.stats_nba.pbp_loader import StatsNbaPbpLoader
from pbpstats.data_loader.stats_nba.shots_loader import StatsNbaShotsLoader
from pbpstats.data_loader.nba_enhanced_pbp_loader import NbaEnhancedPbpLoader
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_factory import StatsNbaEnhancedPbpFactory
from pbpstats.resources.enhanced_pbp.field_goal import FieldGoal


class StatsNbaEnhancedPbpLoader(StatsNbaPbpLoader, NbaEnhancedPbpLoader):
    data_provider = 'stats_nba'
    resource = 'EnhancedPbp'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory=None):
        super().__init__(game_id, source, file_directory)

    def _make_pbp_items(self):
        factory = StatsNbaEnhancedPbpFactory()
        self.items = [factory.get_event_class(item['EVENTMSGTYPE'])(item, i) for i, item in enumerate(self.data)]
        self._add_shot_x_y_coords()
        self._add_extra_attrs_to_all_events()

    def _add_shot_x_y_coords(self):
        shots_loader = StatsNbaShotsLoader(self.game_id, self.source, self.file_directory)
        shots_event_num_map = {item.game_event_id: {'loc_x': item.loc_x, 'loc_y': item.loc_y} for item in shots_loader.items}
        for item in self.items:
            if isinstance(item, FieldGoal) and item.event_num in shots_event_num_map.keys():
                item.locX = shots_event_num_map[item.event_num]['loc_x']
                item.locY = shots_event_num_map[item.event_num]['loc_y']
