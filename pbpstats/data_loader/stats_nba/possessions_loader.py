import os
import json

from pbpstats.overrides import IntDecoder
from pbpstats.data_loader.stats_nba.enhanced_pbp_loader import StatsNbaEnhancedPbpLoader
from pbpstats.data_loader.nba_possession_loader import NbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession


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
                if possession.offense_team_id == possession.previous_possession.offense_team_id:
                    if not (
                        self.game_id in self.bad_pbp_cases.keys() and
                        possession.period in self.bad_pbp_cases[self.game_id].keys() and
                        possession.number in self.bad_pbp_cases[self.game_id][possession.period]
                    ):
                        exception_text = (
                            f'GameId: {possession.game_id}, Period: {possession.period}, '
                            f'Number: {possession.number}, Events: {possession.events}, '
                            f'Previous Events: {possession.previous_possession.events}>'
                        )

                        raise TeamHasBackToBackPossessionsException(exception_text)
            if possession.next_possession is not None:
                if possession.offense_team_id == possession.next_possession.offense_team_id:
                    if not (
                        self.game_id in self.bad_pbp_cases.keys() and
                        possession.period in self.bad_pbp_cases[self.game_id].keys() and
                        possession.next_possession.number in self.bad_pbp_cases[self.game_id][possession.period]
                    ):
                        exception_text = (
                            f'GameId: {possession.game_id}, Period: {possession.period}, '
                            f'Number: {possession.next_possession.number}, Events: {possession.next_possession.events}, '
                            f'Previous Events: {possession.events}>'
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
