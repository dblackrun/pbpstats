from collections import defaultdict

from pbpstats import utils
from pbpstats.possession_details import PossessionDetails
from pbpstats.data_pbp_event import DataPbpEvent
from pbpstats.period import Period


class DataPeriod(Period):
    """
    class for period data
    Events attribute is list of DataPbpEvent objects in order they occur
    Possessions attribute is list of PossessionDetails objects with detailed data for each possession
    """
    def __init__(self, events, game_id, period):
        """
        events is a list of dicts or list of DataPbpEvent objects
        events should be passed in in order they occur
        """
        self.Events = [
            event if type(event) == DataPbpEvent else DataPbpEvent(event)
            for event in events
        ]
        self.GameId = game_id
        self.Number = period
        self.Possessions = []
        self.set_next_and_previous_event_for_all_events()

    def __repr__(self):
        return f'<DataPeriod: {self.__dict__}>'

    def set_base_possession_details(self, teams):
        """
        gets base possession details for each possession in period - uses offense_team_id
        Will have small differences from StatsPeriod version for some games
            - I think partly because of how oftid changes on flagrant fouls
            - There also seem to be a few issues where oftid changes when it shouldn't (see lane violation at start of Q2 0021800012)
            - I think this will very slightly over count total possessions

        teams - list of team ids for game, home team id listed first
        """
        possession_number = 1
        previous_possession_end_event_num = 0
        possession_events = []
        previous_possession_events = []
        for event in self.Events:
            possession_events.append(event)
            if event.previous_event is None:
                score_differential = event.home_score - event.visitor_score
                possession_start_seconds_remaining = event.seconds_remaining

            possession_changing_event = False

            # iterate through each event and determine if possession has changed
            if event.next_event is None:
                # last event of period
                possession_changing_event = True
            else:
                oftid_changed = event.offense_team_id != event.next_event.offense_team_id
                # offense_team_id is 0 for first event of first quarter and overtimes - don't count it
                # sometimes there is an event before period start event that breaks things so check that too
                oftid_is_0 = event.offense_team_id == '0' or event.next_event.offense_team_id == '0'
                start_of_period = event.is_start_of_period() or event.next_event.is_start_of_period()
                if oftid_changed and not oftid_is_0 and not start_of_period:
                    possession_changing_event = True

            if event.offense_team_id != '0':
                team_starting_possession_with_ball = str(event.offense_team_id)
            if possession_changing_event:
                if team_starting_possession_with_ball != teams[0]:
                    # score_differential is from home team perspective, change to from offensive team perspective
                    score_differential = -1 * score_differential
                team_id_on_defense = utils.swap_team_id_for_game(team_starting_possession_with_ball, teams)

                possession_details = PossessionDetails(
                    GameId=self.GameId,
                    Period=self.Number,
                    PossessionNumber=possession_number,
                    OffenseTeamId=team_starting_possession_with_ball,
                    DefenseTeamId=team_id_on_defense,
                    StartTime=possession_start_seconds_remaining,
                    EndTime=event.seconds_remaining,
                    PreviousPossessionEndEventNum=previous_possession_end_event_num,
                    EndEventNum=event.number,
                    StartScoreDifferential=score_differential,
                    Events=possession_events,
                    PreviousPossessionEvents=previous_possession_events,
                    OffensiveRebounds=0,
                    SecondChanceTime=0,
                    PlayerStats={
                        team_starting_possession_with_ball: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))),
                        team_id_on_defense: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
                    },
                    ShotData=[]
                )
                self.Possessions .append(possession_details)
                # update inital data to start next possession
                possession_number += 1
                team_starting_possession_with_ball = team_id_on_defense
                possession_start_seconds_remaining = event.seconds_remaining
                previous_possession_end_event_num = event.number
                score_differential = event.home_score - event.visitor_score
                previous_possession_events = possession_events.copy()
                possession_events = []
