class StatsNbaLoaderBase(object):
    """
    base class for parsing stats.nba.com api responses
    should not be called directly
    """
    def make_list_of_dicts(self, results_set_index=0):
        """
        creates list of dicts from data
        """
        headers = self.source_data['resultSets'][results_set_index]['headers']
        rows = self.source_data['resultSets'][results_set_index]['rowSet']
        deduped_rows = self.dedupe_events_row_set(rows)
        return [dict(zip(headers, row)) for row in deduped_rows]

    @staticmethod
    def dedupe_events_row_set(events_row_set):
        """
        dedupes list of list while preserving order
        used to dedupe events rowSets pbp response because some games have duplicate events
        """
        deduped_events_row_set = []
        for sublist in events_row_set:
            if sublist not in deduped_events_row_set:
                deduped_events_row_set.append(sublist)
        return deduped_events_row_set
