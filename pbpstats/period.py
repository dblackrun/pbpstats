class Period(object):
    """
    class for methods shared by DataPeriod and StatsPeriod objects
    """
    def set_next_and_previous_event_for_all_events(self):
        """
        sets next and previous event for each event in Events
        first event should return None for previous_event
        last event should return None for next_event
        """
        for i, event in enumerate(self.Events):
            event.order = i
            if i == 0 and i == len(self.Events) - 1:
                event.previous_event = None
                event.next_event = None
            elif i == 0:
                event.previous_event = None
                event.next_event = self.Events[i + 1]
            elif i == len(self.Events) - 1:
                event.previous_event = self.Events[i - 1]
                event.next_event = None
            else:
                event.previous_event = self.Events[i - 1]
                event.next_event = self.Events[i + 1]
