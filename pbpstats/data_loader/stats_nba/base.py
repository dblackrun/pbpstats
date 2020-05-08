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
