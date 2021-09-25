from pbpstats.data_loader.data_nba.pbp.file import DataNbaPbpFileLoader


class DataNbaEnhancedPbpFileLoader(DataNbaPbpFileLoader):
    """
    A ``DataNbaEnhancedPbpFileLoader`` object should be instantiated and passed into ``DataNbaEnhancedPbpLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `data_<game_id>.json` in the `/pbp` subdirectory.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory
