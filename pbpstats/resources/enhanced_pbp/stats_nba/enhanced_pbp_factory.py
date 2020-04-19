import pbpstats.resources.enhanced_pbp.stats_nba as event_types
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem


class StatsNbaEnhancedPbpFactory(object):
    def __init__(self):
        self.event_classes = {}
        self._load_event_classes()

    def _load_event_classes(self):
        event_classes = dict([(name, cls) for name, cls in event_types.__dict__.items() if isinstance(cls, type)])
        for _, event_cls in event_classes.items():
            if isinstance(event_cls.event_type, list):
                for event_type in event_cls.event_type:
                    self.event_classes[event_type] = event_cls
            else:
                self.event_classes[event_cls.event_type] = event_cls

    def get_event_class(self, event_type):
        return self.event_classes.get(event_type, StatsEnhancedPbpItem)
