from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import StartOfPeriod


class LiveStartOfPeriod(StartOfPeriod, LiveEnhancedPbpItem):
    """
    Class for start of period events
    """

    action_type = "period"
    sub_type = "start"

    def __init__(self, *args):
        super().__init__(*args)

    def get_period_starters(self, file_directory=None, ignore_missing_starters=False):
        """
        Gets player ids of players who started the period for each team

        :param str file_directory: directory in which overrides subdirectory exists
            containing period starter overrides when period starters can't be determined
            from parsing pbp events
        :param bool ignore_missing_starters: when True won't reaise missing starters exception
        :returns: dict with list of player ids for each team
            with players on the floor at start of period
        :raises: :obj:`~pbpstats.resources.enhanced_pbp.start_of_period.InvalidNumberOfStartersException`:
            If all 5 players that start the period for a team can't be determined.
        """
        return self._get_period_starters_from_period_events(
            file_directory, ignore_missing_starters=ignore_missing_starters
        )
