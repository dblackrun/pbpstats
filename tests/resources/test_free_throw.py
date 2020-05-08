from pbpstats.resources.enhanced_pbp.data_nba.free_throw import DataFreeThrow
from pbpstats.resources.enhanced_pbp.stats_nba.free_throw import StatsFreeThrow
from pbpstats.resources.enhanced_pbp.stats_nba.field_goal import StatsFieldGoal
from pbpstats.resources.enhanced_pbp.stats_nba.foul import StatsFoul


def test_data_made_free_throw():
    item = {
        "evt": 110,
        "cl": "01:09",
        "de": "[NYK 17-27] O'Quinn Free Throw 2 of 2 (3 PTS)",
        "locX": 0,
        "locY": -80,
        "mtype": 12,
        "etype": 3,
        "opid": "",
        "tid": 1610612752,
        "pid": 203124,
        "hs": 17,
        "vs": 27,
        "epid": "",
        "oftid": 1610612752,
    }
    period = 1
    game_id = "0021900001"
    event = DataFreeThrow(item, period, game_id)
    assert event.is_made is True


def test_data_missed_free_throw():
    item = {
        "evt": 108,
        "cl": "01:09",
        "de": "[NYK] O'Quinn Free Throw 1 of 2 Missed",
        "locX": 0,
        "locY": -80,
        "mtype": 11,
        "etype": 3,
        "opid": "",
        "tid": 1610612752,
        "pid": 203124,
        "hs": 16,
        "vs": 27,
        "epid": "",
        "oftid": 1610612752,
    }
    period = 1
    game_id = "0021900001"
    event = DataFreeThrow(item, period, game_id)
    assert event.is_made is False


def test_stats_made_free_throw():
    item = {
        "EVENTNUM": 110,
        "PCTIMESTRING": "01:09",
        "HOMEDESCRIPTION": "O'Quinn Free Throw 2 of 2 (3 PTS)",
        "EVENTMSGACTIONTYPE": 12,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203124,
        "PLAYER1_TEAM_ID": 1610612752,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    event = StatsFreeThrow(item, order)
    assert event.is_made is True


def test_stats_missed_free_throw():
    item = {
        "EVENTNUM": 108,
        "PCTIMESTRING": "01:09",
        "HOMEDESCRIPTION": "MISS O'Quinn Free Throw 1 of 2",
        "EVENTMSGACTIONTYPE": 11,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203124,
        "PLAYER1_TEAM_ID": 1610612752,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    event = StatsFreeThrow(item, order)
    assert event.is_made is False


def test_ft_1_of_2():
    item = {
        "EVENTNUM": 108,
        "PCTIMESTRING": "01:09",
        "HOMEDESCRIPTION": "MISS O'Quinn Free Throw 1 of 2",
        "EVENTMSGACTIONTYPE": 11,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203124,
        "PLAYER1_TEAM_ID": 1610612752,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    event = StatsFreeThrow(item, order)
    assert event.is_ft_1_of_2 is True


def test_ft_1_of_3():
    item = {
        "EVENTNUM": 108,
        "PCTIMESTRING": "01:09",
        "HOMEDESCRIPTION": "MISS O'Quinn Free Throw 1 of 3",
        "EVENTMSGACTIONTYPE": 13,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203124,
        "PLAYER1_TEAM_ID": 1610612752,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    event = StatsFreeThrow(item, order)
    assert event.is_ft_1_of_3 is True


def test_ft_2_of_3():
    item = {
        "EVENTNUM": 108,
        "PCTIMESTRING": "01:09",
        "HOMEDESCRIPTION": "MISS O'Quinn Free Throw 2 of 3",
        "EVENTMSGACTIONTYPE": 14,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203124,
        "PLAYER1_TEAM_ID": 1610612752,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    event = StatsFreeThrow(item, order)
    assert event.is_ft_2_of_3 is True


def test_num_ft_for_trip_is_3():
    item = {
        "EVENTNUM": 108,
        "PCTIMESTRING": "01:09",
        "HOMEDESCRIPTION": "MISS O'Quinn Free Throw 1 of 3",
        "EVENTMSGACTIONTYPE": 13,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203124,
        "PLAYER1_TEAM_ID": 1610612752,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    event = StatsFreeThrow(item, order)
    assert event.num_ft_for_trip == 3


def test_away_from_play_true():
    foul = {
        "EVENTMSGTYPE": 6,
        "EVENTMSGACTIONTYPE": 6,
        "VISITORDESCRIPTION": "Away From Play Foul",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
        "PLAYER1_ID": 2,
        "PLAYER2_ID": 1,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    ft = {
        "EVENTMSGTYPE": 3,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Free Throw 1 of 1",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 1,
    }
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    make = {
        "EVENTMSGTYPE": 1,
        "EVENTMSGACTIONTYPE": 10,
        "VISITORDESCRIPTION": "Made Shot by team that got fouled",
        "PCTIMESTRING": "0:35",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 21,
    }
    order = 1
    make_event = StatsFieldGoal(make, order)
    foul_event.previous_event = None
    foul_event.next_event = ft_event
    ft_event.previous_event = foul_event
    ft_event.next_event = make_event
    make_event.previous_event = ft_event
    make_event.next_event = None
    assert ft_event.is_away_from_play_ft is True


def test_foul_on_made_shot_by_team_that_got_fouled_is_not_away_from_play_ft():
    ft = {
        "EVENTMSGTYPE": 3,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Free Throw 1 of 1",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 1,
    }
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    foul = {
        "EVENTMSGTYPE": 6,
        "EVENTMSGACTIONTYPE": 6,
        "VISITORDESCRIPTION": "Away From Play Foul",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
        "PLAYER1_ID": 2,
        "PLAYER2_ID": 1,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    make = {
        "EVENTMSGTYPE": 1,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Made Shot by team that got fouled",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 2,
    }
    order = 1
    make_event = StatsFieldGoal(make, order)
    ft_event.previous_event = None
    ft_event.next_event = foul_event
    foul_event.previous_event = ft_event
    foul_event.next_event = make_event
    make_event.previous_event = foul_event
    make_event.next_event = None
    assert ft_event.is_away_from_play_ft is False


def test_foul_on_made_shot_by_team_that_didnt_get_fouled_is_away_from_play_ft():
    ft = {
        "EVENTMSGTYPE": 3,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Free Throw 1 of 1",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 1,
    }
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    foul = {
        "EVENTMSGTYPE": 6,
        "EVENTMSGACTIONTYPE": 6,
        "VISITORDESCRIPTION": "Away From Play Foul",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
        "PLAYER1_ID": 2,
        "PLAYER2_ID": 1,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    make = {
        "EVENTMSGTYPE": 1,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Made Shot by team that got fouled",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
        "PLAYER1_ID": 3,
    }
    order = 1
    make_event = StatsFieldGoal(make, order)
    ft_event.previous_event = None
    ft_event.next_event = foul_event
    foul_event.previous_event = ft_event
    foul_event.next_event = make_event
    make_event.previous_event = foul_event
    make_event.next_event = None
    assert ft_event.is_away_from_play_ft is True


def test_foul_on_made_ft_by_team_that_didnt_get_fouled_is_away_from_play_ft():
    ft_2_of_2 = {
        "EVENTNUM": 607,
        "PCTIMESTRING": "0:25",
        "VISITORDESCRIPTION": "Jackson Free Throw 2 of 2 (16 PTS)",
        "EVENTMSGACTIONTYPE": 12,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 202704,
        "PLAYER1_TEAM_ID": 1610612765,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    ft_2_of_2_event = StatsFreeThrow(ft_2_of_2, order)
    foul = {
        "EVENTNUM": 609,
        "PCTIMESTRING": "0:25",
        "VISITORDESCRIPTION": "Griffin AWAY.FROM.PLAY.FOUL (P5.PN) (M.Davis)",
        "EVENTMSGACTIONTYPE": 6,
        "EVENTMSGTYPE": 6,
        "PLAYER1_ID": 201933,
        "PLAYER1_TEAM_ID": 1610612765,
        "PLAYER2_ID": 201145,
        "PLAYER2_TEAM_ID": 1610612764,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    ft_1_of_1 = {
        "EVENTNUM": 611,
        "PCTIMESTRING": "0:25",
        "HOMEDESCRIPTION": "Beal Free Throw 1 of 1 (32 PTS)",
        "EVENTMSGACTIONTYPE": 10,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203078,
        "PLAYER1_TEAM_ID": 1610612764,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    ft_1_of_1_event = StatsFreeThrow(ft_1_of_1, order)
    fg = {
        "EVENTNUM": 612,
        "PCTIMESTRING": "0:24",
        "VISITORDESCRIPTION": "MISS Green 27' 3PT Jump Shot",
        "EVENTMSGACTIONTYPE": 1,
        "EVENTMSGTYPE": 2,
        "PLAYER1_ID": 201145,
        "PLAYER1_TEAM_ID": 1610612764,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    fg_event = StatsFieldGoal(fg, order)
    ft_2_of_2_event.previous_event = None
    ft_2_of_2_event.next_event = foul_event
    foul_event.previous_event = ft_2_of_2_event
    foul_event.next_event = ft_1_of_1_event
    ft_1_of_1_event.previous_event = foul_event
    ft_1_of_1_event.next_event = fg_event
    fg_event.previous_event = ft_1_of_1_event
    fg_event.next_event = None
    assert ft_1_of_1_event.is_away_from_play_ft is True


def test_inbound_foul_ft_true():
    foul = {
        "EVENTMSGTYPE": 6,
        "EVENTMSGACTIONTYPE": 5,
        "VISITORDESCRIPTION": "Inbound Foul",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    ft = {
        "EVENTMSGTYPE": 3,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Free Throw 1 of 1",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
    }
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    foul_event.previous_event = None
    foul_event.next_event = ft_event
    ft_event.previous_event = foul_event
    ft_event.next_event = None
    assert ft_event.is_inbound_foul_ft is True


def test_away_from_play_free_throw_type():
    foul = {
        "EVENTMSGTYPE": 6,
        "EVENTMSGACTIONTYPE": 6,
        "VISITORDESCRIPTION": "Away From Play Foul",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
        "PLAYER1_ID": 2,
        "PLAYER2_ID": 1,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    ft = {
        "EVENTMSGTYPE": 3,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Free Throw 1 of 1",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 1,
    }
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    make = {
        "EVENTMSGTYPE": 1,
        "EVENTMSGACTIONTYPE": 10,
        "VISITORDESCRIPTION": "Made Shot by team that got fouled",
        "PCTIMESTRING": "0:35",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 21,
    }
    order = 1
    make_event = StatsFieldGoal(make, order)
    foul_event.previous_event = None
    foul_event.next_event = ft_event
    ft_event.previous_event = foul_event
    ft_event.next_event = make_event
    make_event.previous_event = ft_event
    make_event.next_event = None
    assert ft_event.free_throw_type == "1 Shot Away From Play"


def test_flagrant_free_throw_type():
    foul = {
        "EVENTNUM": 609,
        "PCTIMESTRING": "0:25",
        "VISITORDESCRIPTION": "Griffin Flagrant Foul (P5.PN) (M.Davis)",
        "EVENTMSGACTIONTYPE": 14,
        "EVENTMSGTYPE": 6,
        "PLAYER1_ID": 201933,
        "PLAYER1_TEAM_ID": 1610612765,
        "PLAYER2_ID": 203078,
        "PLAYER2_TEAM_ID": 1610612764,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    foul_event = StatsFoul(foul, order)
    ft_1_of_1 = {
        "EVENTNUM": 611,
        "PCTIMESTRING": "0:25",
        "HOMEDESCRIPTION": "Beal Free Throw Flagrant (32 PTS)",
        "EVENTMSGACTIONTYPE": 11,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203078,
        "PLAYER1_TEAM_ID": 1610612764,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    ft_1_of_1_event = StatsFreeThrow(ft_1_of_1, order)
    ft_2_of_2 = {
        "EVENTNUM": 611,
        "PCTIMESTRING": "0:25",
        "HOMEDESCRIPTION": "Beal Free Throw Flagrant (32 PTS)",
        "EVENTMSGACTIONTYPE": 12,
        "EVENTMSGTYPE": 3,
        "PLAYER1_ID": 203078,
        "PLAYER1_TEAM_ID": 1610612764,
        "PLAYER2_ID": None,
        "PLAYER2_TEAM_ID": None,
        "PLAYER3_ID": None,
        "PLAYER3_TEAM_ID": None,
    }
    order = 1
    ft_2_of_2_event = StatsFreeThrow(ft_2_of_2, order)

    foul_event.previous_event = None
    foul_event.next_event = ft_1_of_1_event
    ft_1_of_1_event.previous_event = foul_event
    ft_1_of_1_event.next_event = ft_2_of_2_event
    ft_2_of_2_event.previous_event = ft_1_of_1_event
    ft_2_of_2_event.next_event = None

    assert ft_1_of_1_event.free_throw_type == "2 Shot Flagrant"


def test_event_for_efficiency_stats_when_events_out_of_order():
    ft = {
        "EVENTMSGTYPE": 3,
        "EVENTMSGACTIONTYPE": 10,
        "HOMEDESCRIPTION": "Free Throw 1 of 1",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 1,
        "PLAYER1_ID": 1,
    }
    order = 1
    ft_event = StatsFreeThrow(ft, order)
    foul = {
        "EVENTMSGTYPE": 6,
        "EVENTMSGACTIONTYPE": 6,
        "VISITORDESCRIPTION": "Away From Play Foul",
        "PCTIMESTRING": "0:45",
        "PLAYER1_TEAM_ID": 2,
        "PLAYER1_ID": 2,
        "PLAYER2_ID": 1,
    }
    order = 1
    foul_event = StatsFoul(foul, order)

    ft_event.previous_event = None
    ft_event.next_event = foul_event
    foul_event.previous_event = ft_event
    foul_event.next_event = None
    assert ft_event.event_for_efficiency_stats == foul_event
