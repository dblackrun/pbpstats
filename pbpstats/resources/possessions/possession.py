class Possession(object):
    def __init__(self, events):
        self.game_id = events[0].game_id
        self.period = events[0].period
        self.events = events
        self.stats = [event.event_stats for event in events]
        print(self.stats)

    def __repr__(self):
        return f'<{type(self).__name__} GameId: {self.game_id}, Period: {self.period}, Number: {self.number}, StartTime: {self.start_time}, EndTime: {self.end_time}>'

    @property
    def data(self):
        return self.__dict__

    @property
    def start_time(self):
        if not hasattr(self, 'previous_possession') or self.previous_possession is None:
            return self.events[0].clock
        return self.previous_possession.events[-1].clock

    @property
    def end_time(self):
        return self.events[-1].clock
