from pbpstats.data_loader.stats_nba.enhanced_pbp.file import StatsNbaEnhancedPbpFileLoader


class StatsNbaPossessionFileLoader(object):
    """
    A ``StatsNbaPossessionFileLoader`` object should be instantiated and passed into ``StatsNbaPossessionLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `stats_<game_id>.json` in the `/pbp` subdirectory.
    """
    def __init__(self, file_directory):
        self.file_directory = file_directory
        self.enhanced_pbp_source_loader = StatsNbaEnhancedPbpFileLoader(file_directory)