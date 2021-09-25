from pbpstats.data_loader.live.pbp.file import LivePbpFileLoader


class LiveEnhancedPbpFileLoader(LivePbpFileLoader):
    """
    A ``LiveEnhancedPbpFileLoader`` object should be instantiated and passed into ``LiveEnhancedPbpLoader`` when loading data from file

    :param str game_id: NBA Stats Game Id
    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `live_<game_id>.json` in the `/pbp` subdirectory.
    """
    def __init__(self, file_directory):
        self.file_directory = file_directory
