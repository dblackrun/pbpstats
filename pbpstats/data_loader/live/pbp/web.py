import json
import os

from pbpstats.data_loader.live.web_loader import LiveWebLoader


class LivePbpWebLoader(LiveWebLoader):
    """
    A ``LivePbpWebLoader`` object should be instantiated and passed into ``LivePbpLoader`` when loading data directly from the NBA Stats API

    :param str file_directory: (optional, use it if you want to store the response data on disk)
        Directory in which data should be either stored.
        The specific file location will be `live_<game_id>.json` in the `/pbp` subdirectory.
        If not provided response data will not be saved on disk.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    def load_data(self, game_id):
        self.game_id = game_id
        league = self.league.upper()
        self.url = f"https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/{league}/liveData/playbyplay/playbyplay_{self.game_id}.json"
        return self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f"{self.file_directory}/pbp/live_{self.game_id}.json"
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)

