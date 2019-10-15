from collections import defaultdict

import pbpstats
from pbpstats import utils
from pbpstats.overrides import POSSESSION_CHANGING_EVENT_OVERRIDES, NON_POSSESSION_CHANGING_EVENT_OVERRIDES
from pbpstats.possession_details import PossessionDetails
from pbpstats.stats_pbp_event import StatsPbpEvent
from pbpstats.period import Period


class StatsPeriod(Period):
    """
    class for period data
    Events attribute is list of StatsPbpEvent objects in order they occur
    Possessions attribute is list of PossessionDetails objects with detailed data for each possession
    """
    def __init__(self, events, game_id, period):
        """
        events is a list of dicts or list of StatsPbpEvent objects in sequential order
        """
        self.Events = [
            event if type(event) == StatsPbpEvent else StatsPbpEvent(event)
            for event in events
        ]
        self.GameId = game_id
        self.Number = period
        self.Possessions = []
        self.set_next_and_previous_event_for_all_events()

    def __repr__(self):
        return f'<StatsPeriod: {self.__dict__}>'

    def set_base_possession_details(self, teams):
        """
        gets base possession details for each possession in period

        possession changing events are:
            - made fgs
            - defensive rebounds
            - turnovers
            - made final FTs (ex 1/1, 2/2, 3/3) that aren't flagrant/away from play etc

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
            # iterate through each event and determine if possession has changed
            possession_changing_event = False
            # defensive rebound
            if event.is_rebound():
                reb_data = event.get_rebound_data()
                if (
                    reb_data is not None and
                    reb_data['def_reb'] and
                    not(event.seconds_remaining == 0 and not reb_data['player_reb'])
                ):
                    # don't include team rebounds with 0 seconds left - they appear in pbp following missed shots at the buzzer
                    possession_changing_event = True
                    # team that started possession with ball is opposite of team who got rebound
                    team_starting_possession_with_ball = utils.swap_team_id_for_game(reb_data['team_id'], teams)
                if (
                    reb_data is not None and
                    event.seconds_remaining == 0 and reb_data['def_reb'] and
                    event.next_event is not None and not event.next_event.is_end_of_period()
                ):
                    # rebound with no time left that isn't last event of period
                    possession_changing_event = True
                    # team that started possession with ball is opposite of team who got rebound
                    team_starting_possession_with_ball = utils.swap_team_id_for_game(reb_data['team_id'], teams)
            # turnovers
            if event.is_turnover():
                possession_changing_event = True
                team_starting_possession_with_ball = event.team_id
            # made FGs
            if event.is_made_fg():
                if (
                    not event.is_and1_shot() and
                    not (
                        event.next_event is not None and
                        (event.next_event.get_foul_type() in [pbpstats.FLAGRANT_1_FOUL_TYPE_STRING, pbpstats.FLAGRANT_2_FOUL_TYPE_STRING] and event.next_event.team_id != event.team_id) and
                        event.seconds_remaining == event.next_event.seconds_remaining
                    )
                ):
                    # team that started possession with ball is team that made the shot
                    possession_changing_event = True
                    team_starting_possession_with_ball = event.team_id

            # made final FTA
            if event.is_made_ft() and (event.is_ft_1_of_1() or event.is_ft_2_of_2() or event.is_ft_3_of_3()):
                # Ignore FT 1 of 1 on away from play fouls with no made shot - away from play is msgtype 6, actiontype 6
                if (
                    not event.is_away_from_play_ft() and
                    not event.is_inbound_foul_ft() and
                    # ignore loose ball or flagrant foul going for rebound on missed FT
                    not (
                        event.next_event.is_foul() and
                        event.next_event.seconds_remaining == event.seconds_remaining and
                        event.team_id != event.next_event.team_id and
                        event.next_event.get_foul_type() in [
                            pbpstats.LOOSE_BALL_FOUL_TYPE_STRING,
                            pbpstats.PERSONAL_FOUL_TYPE_STRING,
                            pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING,
                            pbpstats.FLAGRANT_1_FOUL_TYPE_STRING,
                            pbpstats.FLAGRANT_2_FOUL_TYPE_STRING
                        ]
                    )
                ):
                    possession_changing_event = True
                    # team that started possession with ball is team that made FT, team that ended possession is other team
                    team_starting_possession_with_ball = event.team_id

            # change of possession on jump ball
            if event.previous_event is not None and not event.previous_event.is_start_of_period() and event.is_jump_ball():
                # offense_team_id is jump ball winner
                try:
                    if hasattr(event, 'offense_team_id'):
                        jump_ball_winning_team_id = event.offense_team_id
                    else:
                        jump_ball_winning_team_id = str(event.opid)

                    if jump_ball_winning_team_id != team_starting_possession_with_ball:
                        if not (event.next_event.is_rebound() or event.next_event.is_jump_ball()):
                            # ignore jump ball if next event is a rebound or jump ball since that will trigger possession change
                            # check for next event (ignoring subs) to see if it is a shot by team that had possession of the ball
                            pbp_event = event.next_event
                            while pbp_event.is_substitution():
                                pbp_event = pbp_event.next_event
                            if not (pbp_event.is_made_fg() and team_starting_possession_with_ball == pbp_event.team_id):
                                possession_changing_event = True
                        if event.next_event.is_turnover() and event.next_event.seconds_remaining == event.seconds_remaining:
                            # if next event is steal at same time of pbp don't need to change possession since steal takes care of it
                            possession_changing_event = False
                        elif event.previous_event.is_turnover() and event.previous_event.seconds_remaining == event.seconds_remaining:
                            # if previous event is steal at same time of pbp don't need to change possession since steal takes care of it
                            possession_changing_event = False
                        elif event.next_event.is_jumpball_violation():
                            # jump ball violation - turnover will be possession changing event
                            possession_changing_event = False

                except UnboundLocalError:
                    pass  # jump ball on 1st possession - ignore for now

            # fix for edge cases where there are bugs in pbp data
            if (
                possession_number > 1 and
                (
                    (event.is_made_fg() or event.is_missed_fg()) and
                    not possession_changing_event
                ) and
                event.team_id != team_starting_possession_with_ball
            ):
                possession_number += 1
                team_starting_possession_with_ball = utils.swap_team_id_for_game(team_starting_possession_with_ball, teams)
                possession_start_seconds_remaining = event.previous_event.seconds_remaining

            if self.GameId in POSSESSION_CHANGING_EVENT_OVERRIDES.keys() and event.number in POSSESSION_CHANGING_EVENT_OVERRIDES[self.GameId]:
                possession_changing_event = True

            if self.GameId in NON_POSSESSION_CHANGING_EVENT_OVERRIDES.keys() and event.number in NON_POSSESSION_CHANGING_EVENT_OVERRIDES[self.GameId]:
                possession_changing_event = False

            if event.next_event is None:
                # last event of period
                possession_changing_event = True

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
