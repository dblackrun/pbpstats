from pbpstats.resources.enhanced_pbp import StartOfPeriod


class NbaPossessionLoader(object):
    """
    Class for shared methods between :obj:`~pbpstats.data_loader.data_nba.possessions_loader.DataNbaPossessionLoader`
    and :obj:`~pbpstats.data_loader.stats_nba.possessions_loader.StatsNbaPossessionLoader`

    Both :obj:`~pbpstats.data_loader.data_nba.possessions_loader.DataNbaPossessionLoader`
    and :obj:`~pbpstats.data_loader.stats_nba.possessions_loader.StatsNbaPossessionLoader` should inherit from this class

    This class should not be instantiated directly
    """

    def _split_events_by_possession(self):
        """
        splits events by possession
        :returns: list of lists with events for each possession
        """
        events = []
        possession_events = []
        for event in self.events:
            possession_events.append(event)
            if event.is_possession_ending_event:
                events.append(possession_events)
                possession_events = []
        return events

    def _add_extra_attrs_to_all_possessions(self):
        """
        adds possession number and next and previous possession
        """
        number = 1
        for i, possession in enumerate(self.items):
            period_start = any(
                isinstance(event, StartOfPeriod) for event in possession.events
            )
            if i == 0 and i == len(self.items) - 1:
                possession.previous_possession = None
                possession.next_possession = None
            elif period_start or i == 0:
                possession.previous_possession = None
                possession.next_possession = self.items[i + 1]
                number = 1
            elif (
                i == len(self.items) - 1
                or possession.period != self.items[i + 1].period
            ):
                possession.previous_possession = self.items[i - 1]
                possession.next_possession = None
            else:
                possession.previous_possession = self.items[i - 1]
                possession.next_possession = self.items[i + 1]
            possession.number = number
            number += 1
