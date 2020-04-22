import json
import os

from pbpstats import DATA_DIRECTORY


class IntDecoder(json.JSONDecoder):
    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {convert_to_int_but_keep_game_id_string(k): self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def convert_to_int_but_keep_game_id_string(value):
    try:
        if str(int(value)) == value:
            return int(value)
        else:
            return value
    except ValueError:
        return value


if DATA_DIRECTORY is not None:
    bad_pbp_possessions_file_path = f'{DATA_DIRECTORY}overrides/bad_pbp_possessions.json'
    if os.path.isfile(bad_pbp_possessions_file_path):
        with open(bad_pbp_possessions_file_path) as f:
            # bad pbp where event is missing in pbp causing back to back possessions for same team - this will prevent back to back possession exception from being raised
            # {GameId: {Period:[EventNum]}}
            BAD_PBP_CASES = json.loads(f.read(), cls=IntDecoder)
    else:
        BAD_PBP_CASES = {}
else:
    BAD_PBP_CASES = {}
