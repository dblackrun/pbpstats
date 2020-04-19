from pbpstats.resources.enhanced_pbp.start_of_period import StartOfPeriod
from pbpstats.resources.enhanced_pbp.end_of_period import EndOfPeriod


class NbaEnhancedPbpLoader(object):
    """
    class for shared methods between data and stats nba pbp loaders
    both DataNbaEnhancedPbpLoader and StatsNbaEnhancedPbpLoader should inherit this
    """
    def _add_extra_attrs_to_all_events(self):
        start_period_indices = []
        for i, event in enumerate(self.items):
            if i == 0 and i == len(self.items) - 1:
                event.previous_event = None
                event.next_event = None
            elif isinstance(event, StartOfPeriod) or i == 0:
                event.previous_event = None
                event.next_event = self.items[i + 1]
                start_period_indices.append(i)
            elif isinstance(event, EndOfPeriod) or i == len(self.items) - 1:
                event.previous_event = self.items[i - 1]
                event.next_event = None
            else:
                event.previous_event = self.items[i - 1]
                event.next_event = self.items[i + 1]
        # these need next and previous event to be added to all events
        for i in start_period_indices:
            team_id = self.items[i].get_team_starting_with_ball()
            self.items[i].team_starting_with_ball = team_id
            period_starters = self.items[i].get_period_starters()
            self.items[i].period_starters = period_starters
