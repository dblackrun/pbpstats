"""
``LiveEnhancedPbpFactory`` can be used to create enhanced pbp event objects from
the :mod:`pbpstats.resources.enhanced_pbp.live` module based on the event type.

The following code will get the event class for a turnover event

.. code-block:: python

    from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_factory import LiveEnhancedPbpFactory

    factory = LiveEnhancedPbpFactory()
    event_class = factory.get_event_class('turnover', 'out-of-bounds')
    print(event_class)  # prints "<class 'pbpstats.resources.enhanced_pbp.live.turnover.LiveTurnover'>"
"""
import pbpstats.resources.enhanced_pbp.live as event_types
from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem


class LiveEnhancedPbpFactory(object):
    """
    Class for factory of event type classes. On initialization will load
    in all event classes in the :mod:`pbpstats.resources.enhanced_pbp.live` module
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
            if isinstance(event_cls.action_type, list):
                for action_type in event_cls.action_type:
                    self.event_classes[action_type] = event_cls
            elif hasattr(event_cls, "sub_type"):
                self.event_classes[
                    f"{event_cls.action_type}{event_cls.sub_type}"
                ] = event_cls
            else:
                self.event_classes[event_cls.action_type] = event_cls

    def get_event_class(self, action_type, sub_type):
        """
        Gets the class for the event based on the event_type

        :param str action_type: event action type for the event

        :returns: class for event type
        """
        if self.event_classes.get(f"{action_type}{sub_type}") is not None:
            return self.event_classes.get(f"{action_type}{sub_type}")
        return self.event_classes.get(action_type, LiveEnhancedPbpItem)
