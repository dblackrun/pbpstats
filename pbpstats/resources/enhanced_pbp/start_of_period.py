import abc
import os
import json

from pbpstats import (
    NBA_GAME_ID_PREFIX,
    G_LEAGUE_GAME_ID_PREFIX,
    WNBA_GAME_ID_PREFIX,
    NBA_STRING,
    G_LEAGUE_STRING,
    WNBA_STRING,
)
from pbpstats.overrides import IntDecoder
from pbpstats.resources.enhanced_pbp import (
    Ejection,
    EndOfPeriod,
    FieldGoal,
    Foul,
    FreeThrow,
    JumpBall,
    Substitution,
    Timeout,
    Turnover,
)


class InvalidNumberOfStartersException(Exception):
    """
    Class for exception when a team's 5 period starters can't be determined.

    You can add the correct period starters to
    overrides/missing_period_starters.json in your data directory to fix this.
    """

    pass


class StartOfPeriod(metaclass=abc.ABCMeta):
    """
    Class for start of period events
    """

    @abc.abstractclassmethod
    def get_period_starters(self, file_directory):
        """
        Gets player ids of players who started the period for each team

        :param str file_directory: directory in which overrides subdirectory exists
            containing period starter overrides when period starters can't be determined
            from parsing pbp events
        :returns: dict with list of player ids for each team
            with players on the floor at start of period
        :raises: :obj:`~pbpstats.resources.enhanced_pbp.start_of_period.InvalidNumberOfStartersException`:
            If all 5 players that start the period for a team can't be determined.
        """
        pass

    @property
    def current_players(self):
        """
        returns period starters
        """
        return self.period_starters

    @property
    def league(self):
        """
        Returns League for game id.

        First 2 in game id represent league - 00 for nba, 10 for wnba, 20 for g-league
        """
        if self.game_id[0:2] == NBA_GAME_ID_PREFIX:
            return NBA_STRING
        elif self.game_id[0:2] == G_LEAGUE_GAME_ID_PREFIX:
            return G_LEAGUE_STRING
        elif self.game_id[0:2] == WNBA_GAME_ID_PREFIX:
            return WNBA_STRING

    def get_team_starting_with_ball(self):
        """
        returns team id for team on starting period with the ball
        """
        if (self.period == 1 or self.period >= 5) and isinstance(
            self.next_event, JumpBall
        ):
            # period starts with jump ball - team that wins starts with the ball
            return self.next_event.team_id
        else:
            # find team id on first shot, non technical ft or turnover
            next_event = self.next_event
            while not (
                isinstance(next_event, (FieldGoal, Turnover))
                or (
                    isinstance(next_event, FreeThrow) and not next_event.is_technical_ft
                )
            ):
                next_event = next_event.next_event
            return next_event.team_id

    def get_offense_team_id(self):
        """
        returns team id for team on starting period on offense
        """
        return self.team_starting_with_ball

    def _get_players_who_started_period_with_team_map(self):
        starters = []
        subbed_in_players = []
        player_team_map = {}  # only player1 has team id in event, this is to track team
        event = self
        while event is not None and not isinstance(event, EndOfPeriod):
            if (
                not isinstance(event, Timeout)
                and event.player1_id != 0
                and hasattr(event, "team_id")
            ):
                player_id = event.player1_id
                if not isinstance(event, JumpBall):
                    # on jump balls team id is winning team, not guaranteed to be player1 team
                    player_team_map[player_id] = event.team_id
                if (
                    isinstance(event, Substitution)
                    and event.incoming_player_id is not None
                ):
                    player_team_map[event.incoming_player_id] = event.team_id
                    if (
                        event.incoming_player_id not in starters
                        and event.incoming_player_id not in subbed_in_players
                    ):
                        subbed_in_players.append(event.incoming_player_id)
                    if player_id not in starters and player_id not in subbed_in_players:
                        starters.append(player_id)

                is_technical_foul = isinstance(event, Foul) and (
                    event.is_technical or event.is_double_technical
                )
                if player_id not in starters and player_id not in subbed_in_players:
                    tech_ft_at_period_start = (
                        isinstance(event, FreeThrow) and event.clock == "12:00"
                    )
                    if not (
                        is_technical_foul
                        or isinstance(event, Ejection)
                        or tech_ft_at_period_start
                    ):
                        # ignore all techs because a player could get a technical foul when they aren't in the game
                        starters.append(player_id)
                # need player2_id and player3_id for players who play full period and never appear in an event as player_id - ex assists, blocks, steals, foul drawn
                if not isinstance(event, Substitution) and not (
                    is_technical_foul or isinstance(event, Ejection)
                ):
                    # ignore all techs because a player could get a technical foul when they aren't in the game
                    if (
                        hasattr(event, "player2_id")
                        and event.player2_id not in starters
                        and event.player2_id not in subbed_in_players
                    ):
                        starters.append(event.player2_id)
                    if (
                        hasattr(event, "player3_id")
                        and event.player3_id not in starters
                        and event.player3_id not in subbed_in_players
                    ):
                        starters.append(event.player3_id)
            event = event.next_event
        return starters, player_team_map

    def _split_up_starters_by_team(self, starters, player_team_map):
        starters_by_team = {}
        # for players who don't appear in event as player1 - won't be in player_team_map
        dangling_starters = []
        for player_id in starters:
            team_id = player_team_map.get(player_id)
            if team_id is not None:
                if team_id not in starters_by_team.keys():
                    starters_by_team[team_id] = []
                starters_by_team[team_id].append(player_id)
            else:
                dangling_starters.append(player_id)
        # if there is one dangling starter we can add it to team missing a starter
        if len(dangling_starters) == 1 and len(starters) == 10:
            for _, team_starters in starters_by_team.items():
                if len(team_starters) == 4:
                    team_starters += dangling_starters
        return starters_by_team

    def _check_both_teams_have_5_starters(self, starters_by_team, file_directory):
        """
        raises exception if either team does not have 5 starters
        """
        for team_id, starters in starters_by_team.items():
            if len(starters) != 5:
                # check if game and period are in overrides file
                if file_directory is None:
                    raise InvalidNumberOfStartersException(
                        f"GameId: {self.game_id}, Period: {self.period}, TeamId: {team_id}, Players: {starters}"
                    )

                missing_period_starters_file_path = (
                    f"{file_directory}/overrides/missing_period_starters.json"
                )
                if not os.path.isfile(missing_period_starters_file_path):
                    raise InvalidNumberOfStartersException(
                        f"GameId: {self.game_id}, Period: {self.period}, TeamId: {team_id}, Players: {starters}"
                    )

                with open(missing_period_starters_file_path) as f:
                    # hard code corrections for games with incorrect number of starters exceptions
                    missing_period_starters = json.loads(f.read(), cls=IntDecoder)
                game_id = (
                    self.game_id if self.league == NBA_STRING else int(self.game_id)
                )
                if (
                    self.game_id in missing_period_starters.keys()
                    and self.period in missing_period_starters[game_id].keys()
                    and team_id in missing_period_starters[game_id][self.period].keys()
                ):
                    starters_by_team[team_id] = missing_period_starters[self.game_id][
                        self.period
                    ][team_id]
                else:
                    raise InvalidNumberOfStartersException(
                        f"GameId: {game_id}, Period: {self.period}, TeamId: {team_id}, Players: {starters}"
                    )

    def _get_period_starters_from_period_events(
        self, file_directory, ignore_missing_starters=False
    ):
        starters, player_team_map = self._get_players_who_started_period_with_team_map()

        starters_by_team = self._split_up_starters_by_team(starters, player_team_map)
        if not ignore_missing_starters:
            self._check_both_teams_have_5_starters(starters_by_team, file_directory)

        return starters_by_team

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        return self.base_stats
