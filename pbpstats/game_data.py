from collections import defaultdict

import pbpstats
from pbpstats import utils
from pbpstats.overrides import MISSING_PERIOD_STARTERS, PLAYERS_MISSING_FROM_BOXSCORE


class InvalidNumberOfStartersException(Exception):
    pass


class GameData(object):
    """
    class for methods shared by DataGameData and StatsGameData objects
    """
    def instantiate_team_and_player_data(self, game_summary):
        """
        sets home and visitor team id, game date and players from game summary response json
        """
        self.HomeTeamId = str(game_summary['g']['hls']['tid'])
        self.VisitorTeamId = str(game_summary['g']['vls']['tid'])
        self.HomeTeamAbbreviation = str(game_summary['g']['hls']['ta'])
        self.VisitorTeamAbbreviation = str(game_summary['g']['vls']['ta'])
        self.GameDate = game_summary['g']['gdte']

        self.Players = {
            self.HomeTeamId: {
                str(player['pid']): player['fn'] + ' ' + player['ln']
                for player in game_summary['g']['hls']['pstsg'] if player['totsec'] > 0  # only keep track of stats for players who played
            },
            self.VisitorTeamId: {
                str(player['pid']): player['fn'] + ' ' + player['ln']
                for player in game_summary['g']['vls']['pstsg'] if player['totsec'] > 0  # only keep track of stats for players who played
            },
        }
        if self.GameId in PLAYERS_MISSING_FROM_BOXSCORE.keys():
            for team_id in PLAYERS_MISSING_FROM_BOXSCORE[self.GameId].keys():
                for player_id in PLAYERS_MISSING_FROM_BOXSCORE[self.GameId][team_id].keys():
                    self.Players[team_id][player_id] = PLAYERS_MISSING_FROM_BOXSCORE[self.GameId][team_id][player_id]

    def set_period_starters(self, missing_period_starters=MISSING_PERIOD_STARTERS):
        """
        gets starters for each period by seeing which players appear in events before being subbed out
        """
        for period in self.Periods:
            period.Starters = {self.HomeTeamId: [], self.VisitorTeamId: []}
            subbed_in_players = {self.HomeTeamId: [], self.VisitorTeamId: []}
            for pbp_event in period.Events:
                player_id = pbp_event.player_id
                if player_id in self.Players[self.HomeTeamId]:
                    team_id = self.HomeTeamId
                elif player_id in self.Players[self.VisitorTeamId]:
                    team_id = self.VisitorTeamId
                else:
                    team_id = None

                if team_id is not None and team_id != '0' and player_id != '0':
                    player2_id = pbp_event.player2_id
                    player3_id = pbp_event.player3_id
                    if pbp_event.is_substitution():
                        # player_id is player going out, player2_id is playing coming in
                        if player2_id not in period.Starters[team_id] and player2_id not in subbed_in_players[team_id]:
                            subbed_in_players[team_id].append(player2_id)
                        if player_id not in period.Starters[team_id] and player_id not in subbed_in_players[team_id]:
                            if player_id in self.Players[self.HomeTeamId] or player_id in self.Players[self.VisitorTeamId]:
                                period.Starters[team_id].append(player_id)
                    if player_id != '0':
                        # player_id 0 is team
                        if player_id not in period.Starters[team_id] and player_id not in subbed_in_players[team_id]:
                            if player_id in self.Players[self.HomeTeamId] or player_id in self.Players[self.VisitorTeamId]:
                                if not (
                                    pbp_event.is_technical_foul() or
                                    pbp_event.is_double_technical_foul() or
                                    pbp_event.is_ejection() or
                                    (pbp_event.is_technical_ft() and pbp_event.clock_time == '12:00')  # ignore technical fts at start of period
                                ):
                                    # ignore all techs because a player could get a technical foul when they aren't in the game
                                    period.Starters[team_id].append(player_id)
                        # need player2_id for players who play full period and never appear in an event as player_id - ex assists
                        if (player2_id in self.Players[self.HomeTeamId] or player2_id in self.Players[self.VisitorTeamId]) and not pbp_event.is_substitution():
                            if not (
                                pbp_event.is_technical_foul() or
                                pbp_event.is_double_technical_foul() or
                                pbp_event.is_ejection()
                            ):
                                # ignore all techs because a player could get a technical foul when they aren't in the game
                                if player2_id in self.Players[self.HomeTeamId]:
                                    player2_team_id = self.HomeTeamId
                                if player2_id in self.Players[self.VisitorTeamId]:
                                    player2_team_id = self.VisitorTeamId
                                if player2_id not in period.Starters[player2_team_id] and player2_id not in subbed_in_players[player2_team_id]:
                                    period.Starters[player2_team_id].append(player2_id)
                        if (player3_id in self.Players[self.HomeTeamId] or player3_id in self.Players[self.VisitorTeamId]) and not pbp_event.is_substitution():
                            if not (
                                pbp_event.is_technical_foul() or
                                pbp_event.is_double_technical_foul() or
                                pbp_event.is_ejection()
                            ):
                                # ignore all techs because a player could get a technical foul when they aren't in the game
                                if player3_id in self.Players[self.HomeTeamId]:
                                    player3_team_id = self.HomeTeamId
                                if player3_id in self.Players[self.VisitorTeamId]:
                                    player3_team_id = self.VisitorTeamId
                                if player3_id not in period.Starters[player3_team_id] and player3_id not in subbed_in_players[player3_team_id]:
                                    period.Starters[player3_team_id].append(player3_id)

            if self.GameId in missing_period_starters.keys() and str(period.Number) in missing_period_starters[self.GameId].keys():
                for team_id in missing_period_starters[self.GameId][str(period.Number)].keys():
                    period.Starters[team_id] = missing_period_starters[self.GameId][str(period.Number)][team_id]

            for team_id in period.Starters.keys():
                if len(period.Starters[team_id]) != 5:
                    raise InvalidNumberOfStartersException(f"GameId: {self.GameId}, Period: {period}, TeamId: {team_id}, Players: {period.Starters[team_id]}")

    def add_players_on_floor(self):
        """
        adds players on floor for each pbp event
        """
        for period in self.Periods:
            # set current players to be period starters
            current_players = period.Starters.copy()
            for pbp_event in period.Events:
                if pbp_event.is_substitution():
                    coming_in = pbp_event.player2_id
                    going_out = pbp_event.player_id
                    team_id = pbp_event.team_id
                    current_players[team_id] = [coming_in if player == going_out else player for player in current_players[team_id]]
                pbp_event.current_players = current_players.copy()

    def set_penalty_start_eventnums(self):
        """
        gets event to start counting penalty stats for
        will be from perspective of offensive team
        """
        for period in self.Periods:
            period.PenaltyStartEventNums = {self.HomeTeamId: None, self.VisitorTeamId: None}
            if period.Number <= 4:
                fouls_to_give = {self.HomeTeamId: 4, self.VisitorTeamId: 4}
            else:
                # in overtime periods teams start with 3 fouls to give
                fouls_to_give = {self.HomeTeamId: 3, self.VisitorTeamId: 3}

            for event in period.Events:
                if event.is_foul_that_counts_toward_penalty():
                    foul_team = event.team_id
                    event_time = event.seconds_remaining
                    if event_time <= 120 and fouls_to_give[foul_team] > 1:
                        # only 1 foul to give in final 2 minutes regardless of how many fouls committed up until then
                        fouls_to_give[foul_team] = 1
                    if fouls_to_give[foul_team] > 0:
                        fouls_to_give[foul_team] -= 1
                        if fouls_to_give[foul_team] == 0:
                            # team entered penalty on this foul
                            if 'Shooting' in event.get_foul_type():
                                # shooting foul - start tracking at final ft so we don't count FTs as penalty
                                final_fts_at_time_of_foul = [
                                    pbp_event for pbp_event in period.Events
                                    if pbp_event.seconds_remaining == event_time and
                                    pbp_event.team_id != foul_team and
                                    (pbp_event.is_ft_1_of_1() or pbp_event.is_ft_2_of_2() or pbp_event.is_ft_3_of_3())
                                ]
                                if len(final_fts_at_time_of_foul) == 0:
                                    # Example of when this happens: lane violation
                                    # just use last event that occured at time of foul
                                    events_at_time_of_foul = [
                                        pbp_event for pbp_event in period.Events
                                        if pbp_event.seconds_remaining == event_time
                                    ]
                                    start_event = events_at_time_of_foul[-1].order
                                elif final_fts_at_time_of_foul[-1].is_missed_ft():
                                    # if FT is missed need to see if it was oreb or dreb
                                    rebounds_after_ft = [
                                        pbp_event for pbp_event in period.Events
                                        if pbp_event.order > event.order and
                                        pbp_event.is_rebound()
                                    ]
                                    # use first rebound after missed FT as bonus start event
                                    start_event = rebounds_after_ft[0].order
                                else:
                                    # use last FT as bonus start event
                                    start_event = final_fts_at_time_of_foul[-1].order
                            else:
                                # non shooting foul - start tracking bonus at this event
                                start_event = event.order
                            offense_team = utils.swap_team_id_for_game(foul_team, [self.HomeTeamId, self.VisitorTeamId])
                            period.PenaltyStartEventNums[offense_team] = start_event

    def add_possession_details(self, ignore_rebound_and_shot_order=False, ignore_back_to_back_possessions=False):
        """
        adds possession details to events
        set ignore_rebound_and_shot_order to True to avoid raising possession_details.PbpEventOrderErrorException if rebound is out of order
        set ignore_back_to_back_possessions to True to avoid raising possession_details.TeamHasBackToBackPossessionsException
        """
        self.FoulTracker = defaultdict(int)
        self.set_penalty_start_eventnums()
        for period in self.Periods:
            period_rebounded_shots = []
            period.set_base_possession_details([self.HomeTeamId, self.VisitorTeamId])
            for possession in period.Possessions:
                possession.add_previous_possession_ending_data()
                possession.add_time_on_floor(self.FoulTracker, period.PenaltyStartEventNums)

            # do this after time gets added for all period possessions because time gets added based on previous event and
            # this alters FT event players and results in time getting added to wrong player
            for i, possession in enumerate(period.Possessions):
                possession.fix_players_on_floor_for_fts()
                possession.add_counting_stats(self.HomeTeamId, period.PenaltyStartEventNums, period_rebounded_shots, ignore_rebound_and_shot_order=ignore_rebound_and_shot_order)
                if i == 0:
                    possession.add_possessions(period.PenaltyStartEventNums, ignore_back_to_back_possessions=ignore_back_to_back_possessions)
                else:
                    possession.add_possessions(period.PenaltyStartEventNums, previous_possession_details=period.Possessions[i - 1], ignore_back_to_back_possessions=ignore_back_to_back_possessions)

    def get_aggregated_possession_stats_for_entity_type(self, entity_type):
        """
        sums up stats for each possession by given entity type
        valid entity types - team, opponent, player, lineup, lineupopponent

        returns dict with data by team and entity id
        """
        entity_type = entity_type.lower()
        if entity_type not in ['team', 'opponent', 'player', 'lineup', 'lineupopponent']:
            return None
        if entity_type in ['team', 'opponent']:
            aggregate_stats = {self.HomeTeamId: defaultdict(int), self.VisitorTeamId: defaultdict(int)}
        else:
            aggregate_stats = {self.HomeTeamId: defaultdict(lambda: defaultdict(int)), self.VisitorTeamId: defaultdict(lambda: defaultdict(int))}
        for period in self.Periods:
            for possession in period.Possessions:
                for team_id in possession.PlayerStats.keys():
                    for lineup_id in possession.PlayerStats[team_id].keys():
                        for opponent_lineup_id in possession.PlayerStats[team_id][lineup_id].keys():
                            for player_id in possession.PlayerStats[team_id][lineup_id][opponent_lineup_id].keys():
                                for stat_key in possession.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id].keys():
                                    stat_value = possession.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][stat_key]
                                    if entity_type == 'team':
                                        aggregate_stats[team_id][stat_key] += stat_value
                                    elif entity_type == 'opponent':
                                        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.HomeTeamId, self.VisitorTeamId])
                                        aggregate_stats[opponent_team_id][stat_key] += stat_value
                                    elif entity_type == 'player':
                                        aggregate_stats[team_id][player_id][stat_key] += stat_value
                                    elif entity_type == 'lineup':
                                        aggregate_stats[team_id][lineup_id][stat_key] += stat_value
                                    elif entity_type == 'lineupopponent':
                                        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.HomeTeamId, self.VisitorTeamId])
                                        aggregate_stats[opponent_team_id][opponent_lineup_id][stat_key] += stat_value

        # since stat keys are summed up from player stats team and lineup stats will need some stats to be divided by 5
        if entity_type in ['team', 'opponent']:
            for team_id in aggregate_stats.keys():
                for stat_key in aggregate_stats[team_id].keys():
                    if stat_key in pbpstats.KEYS_OFF_BY_FACTOR_OF_5_WHEN_AGGREGATING_FOR_TEAM_AND_LINEUPS:
                        aggregate_stats[team_id][stat_key] = aggregate_stats[team_id][stat_key] / 5

        if entity_type in ['lineup', 'lineupopponent']:
            for team_id in aggregate_stats.keys():
                for lineup_id in aggregate_stats[team_id].keys():
                    for stat_key in aggregate_stats[team_id][lineup_id].keys():
                        if stat_key in pbpstats.KEYS_OFF_BY_FACTOR_OF_5_WHEN_AGGREGATING_FOR_TEAM_AND_LINEUPS:
                            aggregate_stats[team_id][lineup_id][stat_key] = aggregate_stats[team_id][lineup_id][stat_key] / 5

        return aggregate_stats
