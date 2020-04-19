import abc

from pbpstats.resources.enhanced_pbp.ejection import Ejection
from pbpstats.resources.enhanced_pbp.end_of_period import EndOfPeriod
from pbpstats.resources.enhanced_pbp.field_goal import FieldGoal
from pbpstats.resources.enhanced_pbp.foul import Foul
from pbpstats.resources.enhanced_pbp.free_throw import FreeThrow
from pbpstats.resources.enhanced_pbp.jump_ball import JumpBall
from pbpstats.resources.enhanced_pbp.substitution import Substitution
from pbpstats.resources.enhanced_pbp.timeout import Timeout
from pbpstats.resources.enhanced_pbp.turnover import Turnover


OVERRIDES = {
    '0021900023': {5: {1610612743: [203924, 203914, 203999, 1627750, 1627736]}},
    '0021900120': {5: {1610612750: [1626157, 203496, 203952, 1629006, 1626203]}},
    '0021900272': {5: {1610612737: [203458, 1629027, 1627761, 203953, 1629631]}},
    '0021900409': {5: {1610612764: [101133, 203078, 202738, 202722, 202397]}},
    '0021900502': {5: {1610612744: [202692, 1627737, 203922, 203110, 1627814]}},
    '0021900550': {5: {1610612760: [203471, 203500, 1628983, 101108, 1628390]}},
    '0021900563': {5: {1610612765: [203083, 1628971, 201565, 1627748, 203503]}},
    '0021900696': {5: {1610612758: [202357, 1628368, 1627741, 203992, 203084]}},
    '0021900787': {5: {1610612737: [203473, 1629027, 1628381, 1628989, 1629631]}},
    '0021900892': {5: {1610612745: [203496, 200782, 201566, 201935, 201569]}},
}


class InvalidNumberOfStartersException(Exception):
    pass


class StartOfPeriod(metaclass=abc.ABCMeta):
    event_type = 12

    @abc.abstractclassmethod
    def get_period_starters(self):
        pass

    @property
    def current_players(self):
        """
        overrides EnhancedPbpItem current_players property
        """
        return self.period_starters

    def get_team_starting_with_ball(self):
        if (self.period == 1 or self.period >= 5) and isinstance(self.next_event, JumpBall):
            # period starts with jump ball - team that wins starts with the ball
            return self.next_event.team_id
        else:
            # find team id on first shot, non technical ft or turnover
            next_event = self.next_event
            while not (isinstance(next_event, (FieldGoal, Turnover)) or (isinstance(next_event, FreeThrow) and not next_event.technical_ft)):
                next_event = next_event.next_event
            return next_event.team_id

    def get_offense_team_id(self):
        """
        overrides EnhancedPbpItem offense_team_id property
        """
        return self.team_starting_with_ball

    def _get_period_starters_from_period_events(self):
        starters = []
        subbed_in_players = []
        player_team_map = {}  # only player1 has team id in event, this is to track team
        event = self
        while event is not None and not isinstance(event, EndOfPeriod):
            if not isinstance(event, Timeout):
                player_id = event.player1_id
                if player_id != 0:
                    if not isinstance(event, JumpBall):
                        # on jump balls team id is winning team, not guaranteed to be player1 team
                        player_team_map[player_id] = event.team_id
                    if isinstance(event, Substitution):
                        player_team_map[event.player2_id] = event.team_id
                        # player_id is player going out, player2_id is playing coming in
                        if event.player2_id not in starters and event.player2_id not in subbed_in_players:
                            subbed_in_players.append(event.player2_id)
                        if player_id not in starters and player_id not in subbed_in_players:
                            starters.append(player_id)

                    is_technical_foul = isinstance(event, Foul) and (event.is_technical or event.is_double_technical)
                    if player_id not in starters and player_id not in subbed_in_players:
                        tech_ft_at_period_start = isinstance(event, FreeThrow) and event.clock == '12:00'
                        if not (is_technical_foul or isinstance(event, Ejection) or tech_ft_at_period_start):
                            # ignore all techs because a player could get a technical foul when they aren't in the game
                            starters.append(player_id)
                    # need player2_id and player3_id for players who play full period and never appear in an event as player_id - ex assists, blocks, steals, foul drawn
                    if not isinstance(event, Substitution) and not (is_technical_foul or isinstance(event, Ejection)):
                        # ignore all techs because a player could get a technical foul when they aren't in the game
                        if hasattr(event, 'player2_id') and event.player2_id not in starters and event.player2_id not in subbed_in_players:
                            starters.append(event.player2_id)
                        if hasattr(event, 'player3_id') and event.player3_id not in starters and event.player3_id not in subbed_in_players:
                            starters.append(event.player3_id)
            event = event.next_event

        # split up starters by team
        starters_by_team = {}
        dangling_starters = []  # for players who don't appear in event as player1 - won't be in player_team_map
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

        if self.game_id in OVERRIDES.keys() and self.period in OVERRIDES[self.game_id].keys():
            for team_id, starters in OVERRIDES[self.game_id][self.period].items():
                starters_by_team[team_id] = starters

        for team_id, starters in starters_by_team.items():
            if len(starters) != 5:
                raise InvalidNumberOfStartersException(f'GameId: {self.game_id}, Period: {self.period}, TeamId: {team_id}, Players: {starters}')

        return starters_by_team

    @property
    def event_stats(self):
        return self.base_stats
