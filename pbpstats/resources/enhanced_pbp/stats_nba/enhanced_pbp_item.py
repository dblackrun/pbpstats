"""
``StatsEnhancedPbpItem`` is the base class for all stats.nba.com enhanced pbp event types
"""
from collections import defaultdict

import requests

from pbpstats import HEADERS, REQUEST_TIMEOUT
from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.enhanced_pbp import (
    FieldGoal,
    Foul,
    FreeThrow,
    JumpBall,
    Rebound,
    StartOfPeriod,
    Turnover,
    Violation,
)


KEY_ATTR_MAPPER = {
    "GAME_ID": "game_id",
    "EVENTNUM": "event_num",
    "PCTIMESTRING": "clock",
    "PERIOD": "period",
    "EVENTMSGACTIONTYPE": "event_action_type",
    "EVENTMSGTYPE": "event_type",
    "PLAYER1_ID": "player1_id",
    "PLAYER1_TEAM_ID": "team_id",
    "PLAYER2_ID": "player2_id",
    "PLAYER3_ID": "player3_id",
    "VIDEO_AVAILABLE_FLAG": "video_available",
}


class StatsEnhancedPbpItem(EnhancedPbpItem):
    """
    Base class for enhanced pbp events from stats.nba.com

    :param dict event: dict with event data
    :param int order: sequential order in which event occurs
    """

    def __init__(self, event, order):
        for key, value in KEY_ATTR_MAPPER.items():
            if event.get(key) is not None:
                setattr(self, value, event.get(key))

        if (
            event.get("HOMEDESCRIPTION") is not None
            and event.get("VISITORDESCRIPTION") is not None
        ):
            self.description = (
                f"{event.get('HOMEDESCRIPTION')}: {event.get('VISITORDESCRIPTION')}"
            )
        elif event.get("HOMEDESCRIPTION") is not None:
            self.description = f"{event.get('HOMEDESCRIPTION')}"
        elif event.get("VISITORDESCRIPTION") is not None:
            self.description = f"{event.get('VISITORDESCRIPTION')}"
        elif event.get("NEUTRALDESCRIPTION") is not None:
            self.description = f"{event.get('NEUTRALDESCRIPTION')}"
        else:
            self.description = ""

        if event.get("PLAYER1_TEAM_ID") is None and event.get("PLAYER1_ID") is not None:
            # need to set team id in these cases where player id is team id
            self.team_id = event.get("PLAYER1_ID", 0)
            self.player1_id = 0

        # fix team/player ids on some event types so they are consistent with DataPbpItem
        if self.event_type == 10:
            # jump ball PLAYER3_TEAM_ID is player who ball gets tipped to
            self.player2_id = event["PLAYER3_ID"]
            self.player3_id = event["PLAYER2_ID"]
            if event["PLAYER3_TEAM_ID"] is not None:
                self.team_id = event["PLAYER3_TEAM_ID"]
            else:
                # when jump ball is tipped out of bounds, winning team is PLAYER3_ID
                self.team_id = event["PLAYER3_ID"]
                if hasattr(self, "player2_id"):
                    delattr(self, "player2_id")
        elif self.event_type in [5, 6]:
            # steals need to change PLAYER2_ID to player3_id - this is player who turned ball over
            # fouls need to change PLAYER2_ID to player3_id - this is player who drew foul
            if hasattr(self, "player2_id"):
                delattr(self, "player2_id")
            if event.get("PLAYER2_ID") is not None:
                self.player3_id = event["PLAYER2_ID"]

        if hasattr(self, "player2_id") and self.player2_id == 0:
            delattr(self, "player2_id")
        if hasattr(self, "player3_id") and self.player3_id == 0:
            delattr(self, "player3_id")
        self.order = order
        self.player_game_fouls = defaultdict(int)
        self.possession_changing_override = False
        self.non_possession_changing_override = False
        self.score = defaultdict(int)

    @property
    def data(self):
        """
        returns event as a dict
        """
        return self.__dict__

    @property
    def video_url(self):
        """
        returns url for mp4 video of play, if available
        """
        if self.video_available == 1:
            parameters = {"GameEventID": self.event_num, "GameID": self.game_id}
            base_url = "https://stats.nba.com/stats/videoeventsasset"
            response = requests.get(
                base_url, parameters, headers=HEADERS, timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                response_json = response.json()
                video_urls = response_json["resultSets"]["Meta"]["videoUrls"]
                if len(video_urls) == 1:
                    return video_urls[0]["murl"]
            else:
                response.raise_for_status()
        return None

    def get_offense_team_id(self):
        """
        returns team id for team on offense for event
        """
        if isinstance(self, Foul) and (self.is_charge or self.is_offensive_foul):
            # offensive foul returns team id
            # this isn't separate method in Foul class because some fouls can be committed
            # on offense or defense (loose ball, flagrant, technical)
            return self.team_id
        event_to_check = self.previous_event
        team_ids = list(self.current_players.keys())
        while event_to_check is not None and not (
            isinstance(event_to_check, (FieldGoal, JumpBall))
            or (
                isinstance(event_to_check, Turnover)
                and not event_to_check.is_no_turnover
            )
            or (isinstance(event_to_check, Rebound) and event_to_check.is_real_rebound)
            or (
                isinstance(event_to_check, FreeThrow)
                and not event_to_check.is_technical_ft
            )
        ):
            event_to_check = event_to_check.previous_event
        if event_to_check is None and self.next_event is not None:
            # should only get here on first possession of period when first event is non-offensive foul,
            # FieldGoal, FreeThrow, Rebound, Turnover, JumpBall
            return self.next_event.get_offense_team_id()
        if isinstance(event_to_check, Turnover) and not event_to_check.is_no_turnover:
            return (
                team_ids[0]
                if team_ids[1] == event_to_check.get_offense_team_id()
                else team_ids[1]
            )
        if isinstance(event_to_check, Rebound) and event_to_check.is_real_rebound:
            if not event_to_check.oreb:
                return (
                    team_ids[0]
                    if team_ids[1] == event_to_check.get_offense_team_id()
                    else team_ids[1]
                )
            return event_to_check.get_offense_team_id()
        if isinstance(event_to_check, (FieldGoal, FreeThrow)):
            if event_to_check.is_possession_ending_event:
                return (
                    team_ids[0]
                    if team_ids[1] == event_to_check.get_offense_team_id()
                    else team_ids[1]
                )
            return event_to_check.get_offense_team_id()
        if isinstance(event_to_check, JumpBall):
            if event_to_check.count_as_possession:
                team_ids = list(self.current_players.keys())
                return (
                    team_ids[0]
                    if team_ids[1] == event_to_check.get_offense_team_id()
                    else team_ids[1]
                )
            return event_to_check.get_offense_team_id()

    @property
    def is_possession_ending_event(self):
        """
        returns True if event ends a possession, False otherwise
        """
        if self.next_event is None:
            return True

        if self.possession_changing_override:
            return True

        if self.non_possession_changing_override:
            return False

        if isinstance(self, Rebound) and self.is_real_rebound and not self.oreb:
            return True

        if isinstance(self, Turnover) and not self.is_no_turnover:
            return True

        if isinstance(self, FieldGoal) and self.is_made:
            # no possession change on flagrant foul
            next_event_is_flagrant_drawn = (
                isinstance(self.next_event, Foul)
                and self.next_event.is_flagrant
                and self.team_id != self.next_event.team_id
                and self.clock == self.next_event.clock
            )
            if (
                not self.is_make_that_does_not_end_possession
                and not next_event_is_flagrant_drawn
            ):
                return True

        if isinstance(self, FreeThrow) and self.is_made and self.is_end_ft:
            next_event_is_foul_drawn_at_ft_time = (
                isinstance(self.next_event, Foul)
                and self.clock == self.next_event.clock
                and self.team_id != self.next_event.team_id
                and (
                    self.next_event.is_loose_ball_foul
                    or self.next_event.is_personal_foul
                    or self.next_event.is_away_from_play_foul
                    or self.next_event.is_flagrant
                )
            )
            if (
                not self.is_away_from_play_ft
                and not self.is_inbound_foul_ft
                and not next_event_is_foul_drawn_at_ft_time
            ):
                return True

        if not isinstance(self.previous_event, StartOfPeriod) and isinstance(
            self, JumpBall
        ):
            return self._is_jump_ball_possession_ending_event()

        return False

    def _is_jump_ball_possession_ending_event(self):
        """
        need to check for rare case where possession changes on jump ball but there is no turnover/rebound
        """
        if (
            isinstance(self.next_event, Turnover)
            and not self.next_event.is_no_turnover
            and self.next_event.clock == self.clock
        ):
            # if next event is steal at same time of pbp don't need to change possession since steal takes care of it
            return False
        elif (
            isinstance(self.previous_event, Turnover)
            and not self.previous_event.is_no_turnover
            and self.previous_event.clock == self.clock
        ):
            # if previous event is steal at same time of pbp don't need to change possession since steal takes care of it
            return False
        elif (
            isinstance(self.next_event, Violation)
            and self.next_event.is_jumpball_violation
        ):
            # jump ball violation - turnover will be possession changing event
            return False
        elif isinstance(self.next_event, Foul) and self.next_event.clock == self.clock:
            next_event = self.next_event.next_event
            if (
                isinstance(next_event, Turnover)
                and not next_event.is_no_turnover
                and next_event.clock == self.clock
            ):
                # foul turnover on jump ball - turnover will trigger change of possession
                return False

        jump_ball_winning_team_id = self.team_id

        prev_event = self.previous_event
        while prev_event is not None and not prev_event.is_possession_ending_event:
            prev_event = prev_event.previous_event

        if prev_event is None:
            return False

        if isinstance(prev_event, Rebound):
            jump_ball_winning_team_started_possession_with_ball = (
                jump_ball_winning_team_id == prev_event.team_id
            )
        else:
            jump_ball_winning_team_started_possession_with_ball = (
                jump_ball_winning_team_id != prev_event.team_id
            )

        next_event_rebound = (
            isinstance(self.next_event, Rebound) and self.next_event.is_real_rebound
        )

        if not jump_ball_winning_team_started_possession_with_ball and not (
            next_event_rebound or isinstance(self.next_event, JumpBall)
        ):
            # ignore jump ball if next event is a rebound or jump ball since that will trigger possession change
            return True
        return False
