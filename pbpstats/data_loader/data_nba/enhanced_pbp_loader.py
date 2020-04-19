from pbpstats.data_loader.data_nba.pbp_loader import DataNbaPbpLoader
from pbpstats.data_loader.nba_enhanced_pbp_loader import NbaEnhancedPbpLoader
from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_factory import DataNbaEnhancedPbpFactory


class DataNbaEnhancedPbpLoader(DataNbaPbpLoader, NbaEnhancedPbpLoader):
    data_provider = 'data_nba'
    resource = 'EnhancedPbp'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory=None):
        super().__init__(game_id, source, file_directory)

    def _make_pbp_items(self):
        factory = DataNbaEnhancedPbpFactory()
        self.items = [factory.get_event_class(event['etype'])(event, item['p'], self.game_id) for item in self.data for event in item['pla']]
        self._add_extra_attrs_to_all_events()
