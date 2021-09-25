from pbpstats import (
    NBA_STRING,
    G_LEAGUE_STRING,
    WNBA_STRING,
    PLAYOFFS_STRING,
    REGULAR_SEASON_STRING,
    PLAY_IN_STRING,
    NBA_GAME_ID_PREFIX,
    G_LEAGUE_GAME_ID_PREFIX,
    WNBA_GAME_ID_PREFIX,
)


class StatsNbaLoaderBase(object):
    """
    Base Class for all stats.nba.com data loaders

    This class should not be instantiated directly
    """

    def make_list_of_dicts(self, results_set_index=0):
        """
        Creates list of dicts from source data

        :param int results_set_index: Index results are in. Default is 0
        :returns: list of dicts with data for results
        """
        headers = self.source_data["resultSets"][results_set_index]["headers"]
        rows = self.source_data["resultSets"][results_set_index]["rowSet"]
        deduped_rows = self.dedupe_events_row_set(rows)
        return [dict(zip(headers, row)) for row in deduped_rows]

    @staticmethod
    def dedupe_events_row_set(events_row_set):
        """
        Dedupes list of results while preserving order

        Used to dedupe events rowSets pbp response because some games have duplicate events

        :param list events_row_set: List of results from API Response
        :returns: deduped list of results
        """
        deduped_events_row_set = []
        for sublist in events_row_set:
            if sublist not in deduped_events_row_set:
                deduped_events_row_set.append(sublist)
        return deduped_events_row_set

    @property
    def data(self):
        """
        returns data from response JSON as a list of dicts
        """
        return self.make_list_of_dicts()

    @property
    def league(self):
        """
        Returns League for game id.

        First 2 in game id represent league - 00 for nba, 10 for wnba, 20 for g-league
        """
        if self.game_id[0:2] == NBA_GAME_ID_PREFIX:
            return NBA_STRING
        elif self.game_id[0:2] == G_LEAGUE_GAME_ID_PREFIX:
            return G_LEAGUE_STRING
        elif self.game_id[0:2] == WNBA_GAME_ID_PREFIX:
            return WNBA_STRING

    @property
    def season(self):
        """
        Returns season for game id

        4th and 5th characters in game id represent season year
        ex. for 2016-17 season 4th and 5th characters would be 16 and season should return 2016-17
        For WNBA just returns season year
        """
        digit4 = int(self.game_id[3])
        digit5 = int(self.game_id[4])
        if digit4 == 9:
            if digit5 == 9:
                return "1999" if self.league == WNBA_STRING else "1999-00"
            else:
                return (
                    f"19{digit4}{digit5}"
                    if self.league == WNBA_STRING
                    else f"19{digit4}{digit5}-{digit4}{digit5 + 1}"
                )
        elif digit5 == 9:
            return (
                f"20{digit4}{digit5}"
                if self.league == WNBA_STRING
                else f"20{digit4}{digit5}-{digit4 + 1}0"
            )
        else:
            return (
                f"20{digit4}{digit5}"
                if self.league == WNBA_STRING
                else f"20{digit4}{digit5}-{digit4}{digit5 + 1}"
            )

    @property
    def season_type(self):
        """
        Returns season type for game id

        3rd character in game id represent season type - 2 for reg season, 4 for playoffs, 5 for play in
        """
        if self.game_id[2] == "4":
            return PLAYOFFS_STRING
        elif self.game_id[2] == "2":
            return REGULAR_SEASON_STRING
        elif self.game_id[2] == "5":
            return PLAY_IN_STRING

    @property
    def league_id(self):
        """
        Returns League Id for league.

        00 for nba, 10 for wnba, 20 for g-league
        """
        if self.league_string == NBA_STRING:
            return NBA_GAME_ID_PREFIX
        elif self.league_string == WNBA_STRING:
            return WNBA_GAME_ID_PREFIX
        elif self.league_string == G_LEAGUE_STRING:
            return G_LEAGUE_GAME_ID_PREFIX