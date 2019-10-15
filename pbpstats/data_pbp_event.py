from pbpstats.pbp_event import PbpEvent


class DataPbpEvent(PbpEvent):
    """
    class for pbp event from data.nba.com api
    """
    def __init__(self, event):
        """
        event is a dict from data.nba.com pbp response
        """
        self.number = event.get('evt')
        self.description = event.get('de', '')
        self.clock_time = event.get('cl', '0:00')
        self.etype = event.get('etype')
        self.mtype = event.get('mtype')
        self.player_id = str(event.get('pid', 0))
        self.team_id = str(event.get('tid', 0))
        self.offense_team_id = str(event.get('oftid', 0))
        self.home_score = event.get('hs', 0)
        self.visitor_score = event.get('vs', 0)
        self.player2_id = str(event.get('epid', ''))
        self.player3_id = str(event.get('opid', ''))
        self.loc_x = event.get('locX')
        self.loc_y = event.get('locY')

        # seconds remaining in period
        split = self.clock_time.split(':')  # clock is formatted mm:ss
        self.seconds_remaining = float(split[0]) * 60 + float(split[1])  # convert to seconds remaining in period

    def is_assisted_shot(self):
        return self.is_made_fg() and 'Assist: ' in self.description

    def is_3pt_shot(self):
        return '3pt Shot' in self.description

    def is_missed_ft(self):
        return self.etype == 3 and 'Missed' in self.description

    def get_number_of_fta_for_foul(self):
        """
        checks event description
        """
        if '(1 FTA)' in self.description:
            return 1
        elif '(2 FTA)' in self.description:
            return 2
        elif '(3 FTA)' in self.description:
            return 3

    def is_blocked_shot(self):
        return self.is_missed_fg() and self.player3_id != ''

    def is_steal(self):
        return self.is_turnover() and 'Steal:' in self.description
