"""
``StatsNbaEnhancedPbpLoader`` loads pbp data for a game and
creates :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` objects
for each event

Enhanced data for each event includes current players on floor, score, fouls to give and number of fouls committed by each player,
plus additional data depending on event type

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import StatsNbaEnhancedPbpLoader

    pbp_loader = StatsNbaEnhancedPbpLoader("0021900001", "file", "/data")
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.stats_nba.pbp_loader import StatsNbaPbpLoader
from pbpstats.data_loader.stats_nba.shots_loader import StatsNbaShotsLoader
from pbpstats.data_loader.nba_enhanced_pbp_loader import NbaEnhancedPbpLoader
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_factory import (
    StatsNbaEnhancedPbpFactory,
)
from pbpstats.resources.enhanced_pbp import FieldGoal
from pbpstats.resources.enhanced_pbp.rebound import EventOrderError


class StatsNbaEnhancedPbpLoader(StatsNbaPbpLoader, NbaEnhancedPbpLoader):
    """
    Loads stats.nba.com source enhanced pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `stats_<game_id>.json` in the `/pbp` subdirectory.
        If not provided response data will not be saved on disk.
    :raises: :obj:`~pbpstats.resources.enhanced_pbp.start_of_period.InvalidNumberOfStartersException`:
        If all 5 players that start the period for a team can't be determined.
        You can add the correct period starters to overrides/missing_period_starters.json in your data directory to fix this.
    :raises: :obj:`~pbpstats.resources.enhanced_pbp.rebound.EventOrderError`:
        If rebound event is not immediately following a missed shot event.
        You can manually edit the event order in the pbp file stored on disk to fix this.
    """

    data_provider = "stats_nba"
    resource = "EnhancedPbp"
    parent_object = "Game"

    def __init__(self, game_id, source, file_directory=None):
        super().__init__(game_id, source, file_directory)

    def _make_pbp_items(self):
        self.factory = StatsNbaEnhancedPbpFactory()
        self.items = [
            self.factory.get_event_class(item["EVENTMSGTYPE"])(item, i)
            for i, item in enumerate(self.data)
        ]
        self._add_extra_attrs_to_all_events()
        self._check_rebound_event_order(6)
        self._add_shot_x_y_coords()

    def _add_shot_x_y_coords(self):
        shots_loader = StatsNbaShotsLoader(
            self.game_id, self.source, self.file_directory
        )
        shots_event_num_map = {
            item.game_event_id: {"loc_x": item.loc_x, "loc_y": item.loc_y}
            for item in shots_loader.items
        }
        for item in self.items:
            if (
                isinstance(item, FieldGoal)
                and item.event_num in shots_event_num_map.keys()
            ):
                item.locX = shots_event_num_map[item.event_num]["loc_x"]
                item.locY = shots_event_num_map[item.event_num]["loc_y"]

    def _check_rebound_event_order(self, max_retries):
        """
        checks rebound events to make sure they are ordered correctly
        """
        attempts = 0
        while attempts <= max_retries:
            try:
                for event in self.items:
                    if hasattr(event, "missed_shot"):
                        event.missed_shot
                break
            except EventOrderError as e:
                self._fix_common_event_order_error(e)
                self.items = [
                    self.factory.get_event_class(item["EVENTMSGTYPE"])(item, i)
                    for i, item in enumerate(self.data)
                ]
                self._add_extra_attrs_to_all_events()
                attempts += 1

    def _fix_common_event_order_error(self, exception):
        """
        fixs common cases where events are out of order
        current cases are:
        - subs/timeouts between free throws being between missed second FT and rebound
        - end of period replay events being between missed shot and rebound
        - rebound and shot in reverse order
        - shot, rebound, rebound - first rebound needs to me moved to before shot
        - shot, rebound, rebound - second rebound needs to be moved ahead of shot and first rebound
        """
        event_num = int(str(exception).split("EventNum: ")[-1].split(">")[0])
        headers = self.source_data["resultSets"][0]["headers"]
        rows = self.source_data["resultSets"][0]["rowSet"]
        event_num_index = headers.index("EVENTNUM")
        event_type_index = headers.index("EVENTMSGTYPE")
        for i, row in enumerate(rows):
            if row[event_num_index] == int(event_num):
                issue_event_index = i

        if rows[issue_event_index][event_type_index] in [8, 9]:
            # these are subs/timeouts that are in between missed ft and rebound
            # move all sub/timeout events between ft and rebound to before ft
            row_index = issue_event_index
            while rows[row_index][event_type_index] in [8, 9]:
                row_index -= 1

            # rows[row_index] should be moved to right before rows[issue_event_index]
            new_rows = []
            row_to_move_event_num = rows[row_index][event_num_index]
            for row in rows:
                if row[event_num_index] == row_to_move_event_num:
                    row_to_move = row
                elif row[event_num_index] == int(event_num):
                    new_rows.append(row)
                    new_rows.append(row_to_move)
                else:
                    new_rows.append(row)

            self.source_data["resultSets"][0]["rowSet"] = new_rows
        elif (
            rows[issue_event_index][event_type_index] == 18
            and rows[issue_event_index + 1][event_type_index] == 4
        ):
            # these are replays that are in between missed shot and rebound
            # move replay event after rebound
            replay_event = rows[issue_event_index]
            rebound_event = rows[issue_event_index + 1]

            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index + 1
            ] = replay_event
            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index
            ] = rebound_event

        elif (
            rows[issue_event_index + 1][event_type_index] == 4
            and rows[issue_event_index + 1][event_num_index] == int(event_num) - 1
        ):
            # rebound and shot need to be flipped
            rebound_event = rows[issue_event_index + 1]
            shot_event = rows[issue_event_index]
            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index
            ] = rebound_event
            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index + 1
            ] = shot_event
        elif (
            rows[issue_event_index + 1][event_type_index] == 4
            and rows[issue_event_index + 1][event_num_index] == int(event_num) + 2
            and rows[issue_event_index - 1][event_type_index] == 2
            and rows[issue_event_index - 1][event_num_index] == int(event_num) + 1
        ):
            # shot, rebound, rebound - first rebound need to me moved to before shot
            rebound_event = rows[issue_event_index]
            shot_event = rows[issue_event_index - 1]
            self.source_data["resultSets"][0]["rowSet"][issue_event_index] = shot_event
            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index - 1
            ] = rebound_event
        elif (
            rows[issue_event_index + 1][event_type_index] == 4
            and rows[issue_event_index + 1][event_num_index] == int(event_num) - 2
            and rows[issue_event_index - 1][event_type_index] == 2
            and rows[issue_event_index - 1][event_num_index] == int(event_num) - 1
        ):
            # shot, rebound, rebound - second rebound needs to be moved ahead of shot and first rebound
            first_rebound = rows[issue_event_index + 1]
            second_rebound = rows[issue_event_index]
            shot_event = rows[issue_event_index - 1]
            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index + 1
            ] = second_rebound
            self.source_data["resultSets"][0]["rowSet"][issue_event_index] = shot_event
            self.source_data["resultSets"][0]["rowSet"][
                issue_event_index - 1
            ] = first_rebound

        self._save_data_to_file()
