import json


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
            return {
                convert_to_int_but_keep_game_id_string(k): self._decode(v)
                for k, v in o.items()
            }
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
