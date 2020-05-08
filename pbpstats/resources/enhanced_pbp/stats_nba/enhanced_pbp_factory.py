"""
``StatsNbaEnhancedPbpFactory`` can be used to create enhanced pbp event objects from
the :mod:`pbpstats.resources.enhanced_pbp.stats_nba` module based on the event type.

The following code will get the event class for event type 1 (which is the event type for a field goal make)

.. code-block:: python

    from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_factory import StatsNbaEnhancedPbpFactory

    factory = StatsNbaEnhancedPbpFactory()
    event_class = factory.get_event_class(1)
    print(event_class)  # prints "<class 'pbpstats.resources.enhanced_pbp.stats_nba.field_goal.StatsFieldGoal'>"
"""
import pbpstats.resources.enhanced_pbp.stats_nba as event_types
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)


class StatsNbaEnhancedPbpFactory(object):
    """
    Class for factory of event type classes. On initialization will load
    in all event classes in the :mod:`pbpstats.resources.enhanced_pbp.stats_nba` module
    """

    def __init__(self):
        self.event_classes = {}
        self._load_event_classes()

    def _load_event_classes(self):
        event_classes = dict(
            [
                (name, cls)
                for name, cls in event_types.__dict__.items()
                if isinstance(cls, type)
            ]
        )
        for _, event_cls in event_classes.items():
            if isinstance(event_cls.event_type, list):
                for event_type in event_cls.event_type:
                    self.event_classes[event_type] = event_cls
            else:
                self.event_classes[event_cls.event_type] = event_cls

    def get_event_class(self, event_type):
        """
        Gets the class for the event based on the event_type

        :param int event_type: event action type for the event

        :returns: class for event type
        """
        return self.event_classes.get(event_type, StatsEnhancedPbpItem)
