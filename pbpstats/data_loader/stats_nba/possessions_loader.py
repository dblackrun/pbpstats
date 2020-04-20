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
        pbp_events = StatsNbaEnhancedPbpLoader(game_id, source, file_directory)
        self.events = pbp_events.items
        events_by_possession = self._split_events_by_possession()
        self.items = [Possession(possession_events) for possession_events in events_by_possession]
        self._add_extra_attrs_to_all_possessions()
        self._check_that_possessions_alternate()

    def _check_that_possessions_alternate(self):
        """
        checks that a team doesn't have back-to-back possessions
        usually caused by pbp events being out of order that can be fixed manually
        """
        for possession in self.items:
            if possession.previous_possession is not None:
                if possession.offense_team_id == possession.previous_possession.offense_team_id:
                    exception_text = (
                        f'GameId: {possession.game_id}, Period: {possession.period}, '
                        f'Number: {possession.number}, Events: {possession.events}, '
                        f'Previous Events: {possession.previous_possession.events}>'
                    )

                    raise TeamHasBackToBackPossessionsException(exception_text)
            if possession.next_possession is not None:
                if possession.offense_team_id == possession.next_possession.offense_team_id:
                    exception_text = (
                        f'GameId: {possession.game_id}, Period: {possession.period}, '
                        f'Number: {possession.next_possession.number}, Events: {possession.next_possession.events}, '
                        f'Previous Events: {possession.events}>'
                    )

                    raise TeamHasBackToBackPossessionsException(exception_text)
