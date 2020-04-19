from pbpstats.data_loader.stats_nba.enhanced_pbp_loader import StatsNbaEnhancedPbpLoader
from pbpstats.data_loader.nba_possession_loader import NbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession


class StatsNbaPossessionLoader(NbaPossessionLoader):
    data_provider = 'stats_nba'
    resource = 'Possessions'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory=None):
        pbp_events = StatsNbaEnhancedPbpLoader(game_id, source, file_directory)
        self.events = pbp_events.items
        events_by_possession = self._split_events_by_possession()
        self.items = [Possession(possession_events) for possession_events in events_by_possession]
        self._add_extra_attrs_to_all_possessions()
