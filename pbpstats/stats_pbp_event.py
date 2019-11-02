import pbpstats

from pbpstats.pbp_event import PbpEvent


class StatsPbpEvent(PbpEvent):
    """
    class for pbp event from stats.nba.com api
    """
    def __init__(self, event):
        """
        event is a dict derived from stats.nba.com pbp response
        player ids are set to be consistent with DataPbpEvent so methods can be shared
        """
        self.number = event.get('EVENTNUM')
        if event.get('HOMEDESCRIPTION') is not None and event.get('VISITORDESCRIPTION') is not None:
            self.description = f"{event.get('HOMEDESCRIPTION')}: {event.get('VISITORDESCRIPTION')}"
        elif event.get('HOMEDESCRIPTION') is not None:
            self.description = f"{event.get('HOMEDESCRIPTION')}"
        elif event.get('VISITORDESCRIPTION') is not None:
            self.description = f"{event.get('VISITORDESCRIPTION')}"
        else:
            self.description = ''

        self.clock_time = event.get('PCTIMESTRING', '0:00')
        self.etype = event.get('EVENTMSGTYPE')
        self.mtype = event.get('EVENTMSGACTIONTYPE')
        self.player_id = str(event.get('PLAYER1_ID', 0))
        self.team_id = str(event.get('PLAYER1_TEAM_ID', 0))
        self.home_score = event.get('home_score', 0)
        self.visitor_score = event.get('visitor_score', 0)
        self.player2_id = str(event.get('PLAYER2_ID', ''))
        self.player3_id = str(event.get('PLAYER3_ID', ''))
        self.game_id = event.get('GAME_ID')
        self.loc_x = None
        self.loc_y = None

        if event.get('PLAYER1_TEAM_ID') is None and event.get('PLAYER1_ID') is not None:
            # need to set team id in these cases where player id is team id
            self.team_id = str(event.get('PLAYER1_ID', 0))
            self.player_id = '0'

        # fix team/player ids on some event types so they are consistent with DataPbpEvent
        if self.etype == 10:
            # jump ball PLAYER3_TEAM_ID is player who ball gets tipped to
            self.player2_id = str(event['PLAYER3_ID'])
            self.player3_id = str(event['PLAYER2_ID'])
            if event['PLAYER3_TEAM_ID'] is not None:
                self.offense_team_id = str(event['PLAYER3_TEAM_ID'])
            else:
                # when jump ball is tipped out of bounds, winning team is PLAYER3_ID
                self.offense_team_id = str(event['PLAYER3_ID'])
                self.player2_id = '0'
        elif self.etype == 5:
            # steals need to change PLAYER2_ID to player3_id - this is player who turned ball over
            self.player2_id = ''
            self.player3_id = str(event['PLAYER2_ID']) if event.get('PLAYER2_ID') is not None else None
        elif self.etype == 6:
            # fouls need to change PLAYER2_ID to player3_id - this is player who drew foul
            self.player2_id = ''
            self.player3_id = str(event['PLAYER2_ID']) if event.get('PLAYER2_ID') is not None else None

        # change 0 pids to empty string so they are consistent with DataPbpEvent
        if self.player2_id == '0':
            self.player2_id = ''
        if self.player3_id == '0':
            self.player3_id = ''

        # seconds remaining in period
        split = self.clock_time.split(':')  # clock is formatted mm:ss
        self.seconds_remaining = float(split[0]) * 60 + float(split[1])  # convert to seconds remaining in period

    def is_assisted_shot(self):
        return self.is_made_fg() and 'AST)' in self.description

    def is_3pt_shot(self):
        return ' 3PT ' in self.description

    def is_missed_ft(self):
        return self.etype == 3 and 'MISS ' in self.description

    def get_number_of_fta_for_foul(self):
        """
        gets number of free throws for foul
        checks event description
        """
        seconds_remaining = self.seconds_remaining
        event = self
        while event is not None and event.seconds_remaining == seconds_remaining and not ((event.is_made_ft() or event.is_missed_ft()) and not event.is_technical_ft() and self.team_id != event.team_id):
            event = event.next_event

        if event is not None and (event.is_made_ft() or event.is_missed_ft()) and not event.is_technical_ft() and event.seconds_remaining == seconds_remaining and self.player3_id != event.player3_id:
            # opid check is to make sure player who got fouled is player shooting free throws
            if 'of 1' in event.description:
                return 1
            elif 'of 2' in event.description:
                return 2
            elif 'of 3' in event.description:
                return 3

        # if we haven't found ft yet, try going backwards
        event = self
        while event is not None and event.seconds_remaining == seconds_remaining and not ((event.is_made_ft() or event.is_missed_ft()) and not event.is_technical_ft() and self.team_id != event.team_id):
            event = event.previous_event

        if event is not None and (event.is_made_ft() or event.is_missed_ft()) and not event.is_technical_ft() and event.seconds_remaining == seconds_remaining and self.player3_id != event.player3_id:
            # opid check is to make sure player who got fouled is player shooting free throws
            if 'of 1' in event.description:
                return 1
            elif 'of 2' in event.description:
                return 2
            elif 'of 3' in event.description:
                return 3
        return None

    def is_blocked_shot(self):
        return self.is_missed_fg() and ' BLK)' in self.description

    def is_steal(self):
        return self.is_turnover() and 'STEAL ' in self.description

    def get_video_url(self):
        """
        gets url for mp4 video of play
        returns url string
        """
        params = {
            'GameEventID': self.number,
            'GameID': self.game_id
        }
        response = pbpstats.utils.get_json_response(pbpstats.VIDEO_EVENT_ASSET_BASE_URL, params, None)
        video_urls = response['resultSets']['Meta']['videoUrls']
        if len(video_urls) == 1:
            return video_urls[0]['murl']
        return ''
