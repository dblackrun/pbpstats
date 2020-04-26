import os
import json

from pbpstats.overrides import IntDecoder
from pbpstats.data_loader.stats_nba.enhanced_pbp_loader import StatsNbaEnhancedPbpLoader
from pbpstats.data_loader.nba_possession_loader import NbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession
from pbpstats.resources.enhanced_pbp.foul import Foul


class TeamHasBackToBackPossessionsException(Exception):
    pass


class StatsNbaPossessionLoader(NbaPossessionLoader):
    data_provider = 'stats_nba'
    resource = 'Possessions'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory=None):

        self.file_directory = file_directory
        self.game_id = game_id
        pbp_events = StatsNbaEnhancedPbpLoader(game_id, source, file_directory)
        self.events = pbp_events.items
        events_by_possession = self._split_events_by_possession()
        self.items = [Possession(possession_events) for possession_events in events_by_possession]
        self._add_extra_attrs_to_all_possessions()
        self._load_bad_possession_overrides()
        self._check_that_possessions_alternate()

    def _check_that_possessions_alternate(self):
        """
        checks that a team doesn't have back-to-back possessions
        usually caused by pbp events being out of order that can be fixed manually
        """
        for possession in self.items:
            if possession.previous_possession is not None:
                poss = possession
                prev_poss = possession.previous_possession
            elif possession.next_possession is not None:
                poss = possession.next_possession
                prev_poss = possession
            if poss.offense_team_id == prev_poss.offense_team_id:
                if not (
                    self.game_id in self.bad_pbp_cases.keys() and
                    poss.period in self.bad_pbp_cases[self.game_id].keys() and
                    poss.number in self.bad_pbp_cases[self.game_id][poss.period]
                ):
                    ignore_because_of_flagrant = False
                    events_to_check = [event for event in prev_poss.events]
                    if prev_poss.previous_possession is not None:
                        events_to_check += prev_poss.previous_possession.events
                    for event in events_to_check:
                        if isinstance(event, Foul) and event.is_flagrant:
                            ignore_because_of_flagrant = True

                    if not ignore_because_of_flagrant:
                        exception_text = (
                            f'GameId: {poss.game_id}, Period: {poss.period}, '
                            f'Number: {poss.number}, Events: {poss.events}, '
                            f'Previous Events: {prev_poss.events}>'
                        )

                        raise TeamHasBackToBackPossessionsException(exception_text)

    def _load_bad_possession_overrides(self):
        self.bad_pbp_cases = {}
        if self.file_directory is not None:
            bad_pbp_possessions_file_path = f'{self.file_directory}/overrides/bad_pbp_possessions.json'
            if os.path.isfile(bad_pbp_possessions_file_path):
                with open(bad_pbp_possessions_file_path) as f:
                    # bad pbp where event is missing in pbp causing back to back possessions for same team - this will prevent back to back possession exception from being raised
                    # {GameId: {Period:[EventNum]}}
                    self.bad_pbp_cases = json.loads(f.read(), cls=IntDecoder)
