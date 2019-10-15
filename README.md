[![Build Status](https://travis-ci.org/dblackrun/pbpstats.svg?branch=master)](https://travis-ci.org/pbpstats/pbpstats)

A package to scrape and parse NBA, WNBA and G-League play-by-play data.

# Features
* Adds lineup on floor for all events
* Adds detailed data for each possession including start time, end time, score margin, how the previous possession ended, second chance time, offensive rebounds
* Shots, rebounds and assists broken down by shot zone
* Supports both stats.nba.com and data.nba.com endpoints
* Supports NBA, WNBA and G-League stats
* All stats on pbpstats.com are derived from these stats

# Installation
requires Python >=3.6
```
pip install pbpstats
```

# Setup data directory
There will be cases where events may be out of order or incorrect due to human error. If you want to be able to manually edit events you can set up the enivronment variable `PBP_STATS_DATA_DIRECTORY` and all request responses will be saved locally so edits can be made. If a file for a game exists locally it will be used instead of making the request to the NBA API. This directory is also where [override files](https://github.com/dblackrun/pbpstats/wiki/Overrides-to-fix-issues-parsing-pbp) to fix periods starters and handle issues with parsing pbp that can't be fixed by editing pbb file are placed.

# Usage
```
from pbpstats.stats_game_data import StatsGameData

game_data = StatsGameData('0041800406')
game_data.get_game_data()
# to ignore rebound event order
# game_data.get_game_data(ignore_rebound_and_shot_order=True)
# to ignore issues parsing pbp that result in a team having back-to-back possessions
# game_data.get_game_data(ignore_back_to_back_possessions=True)
```
to get player stats for game:
```
player_stats = game_data.get_aggregated_possession_stats_for_entity_type('player')
```

to get team stats for game:
```
team_stats = game_data.get_aggregated_possession_stats_for_entity_type('team')
```
to get opponent stats for game:
```
opponent_stats = game_data.get_aggregated_possession_stats_for_entity_type('opponent')
```
to get lineup stats for game:
```
lineup_stats = game_data.get_aggregated_possession_stats_for_entity_type('lineup')
```
to get lineup opponent stats for game:
```
lineup_opponent_stats = game_data.get_aggregated_possession_stats_for_entity_type('lineupopponent')
```
to see data for specific possession
```
print(game_data.Periods[0].Possessions[14])
```

# Note on Ids
Player and team Ids the same player and team ids used by stats.nba.com. Lineup ids are '-' separated player ids (with player ids sorted as strings).

# Issues with raw play-by-play
If you are editing pbp files locally here are some common exceptions that get raised and how to fix them.

### Missed shot not immediately followed by a rebound event

`pbpstats.possession_details.PbpEventOrderErrorException: Shot And Rebound Out of Order GameId: 0021800001, Period: 2, Event: <DataPbpEvent: Description: Brown REBOUND (Off:2 Def:1), Time: 1:32>, Event Num: 317`

Open up stats_0021800001.json in data/pbp directory and search for event number 317

```
...
["0021800001", 316, 2, 1, 2, "8:56 PM", "1:33", "MISS Irving 25' 3PT Jump Shot", null, null, null, null, 4, 202681, "Kyrie Irving", 1610612738, "Boston", "Celtics", "BOS", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800001", 339, 2, 97, 2, "8:56 PM", "1:32", "MISS Brown 2' Tip Layup Shot", null, null, null, null, 4, 1627759, "Jaylen Brown", 1610612738, "Boston", "Celtics", "BOS", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800001", 340, 4, 0, 2, "8:56 PM", "1:32", "Brown REBOUND (Off:2 Def:1)", null, null, null, null, 4, 1627759, "Jaylen Brown", 1610612738, "Boston", "Celtics", "BOS", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800001", 317, 4, 0, 2, "8:57 PM", "1:32", "Brown REBOUND (Off:3 Def:1)", null, null, null, null, 4, 1627759, "Jaylen Brown", 1610612738, "Boston", "Celtics", "BOS", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
...
```

Move first Brown rebound before Brown 2' Tip Layup Shot


### Time needs to be fixed

`pbpstats.possession_details.TeamHasBackToBackPossessionsException: GameId: 0021800011, Period: 4, Possession Number: 48, Event: Cauley-Stein STEAL (1 STL): Ingles Lost Ball Turnover (P5.T17)`

```
["0021800011", 637, 10, 0, 4, "12:25 AM", "1:12", "Jump Ball Cauley-Stein vs. Ingles: Tip to Fox", null, null, null, null, 4, 1626161, "Willie Cauley-Stein", 1610612758, "Sacramento", "Kings", "SAC", 5, 204060, "Joe Ingles", 1610612762, "Utah", "Jazz", "UTA", 4, 1628368, "De'Aaron Fox", 1610612758, "Sacramento", "Kings", "SAC", 1],
["0021800011", 690, 5, 2, 4, "12:26 AM", "1:11", "Cauley-Stein STEAL (1 STL)", null, "Ingles Lost Ball Turnover (P5.T17)", null, null, 5, 204060, "Joe Ingles", 1610612762, "Utah", "Jazz", "UTA", 4, 1626161, "Willie Cauley-Stein", 1610612758, "Sacramento", "Kings", "SAC", 0, 0, null, null, null, null, null, 1],
```

Time on steal needs to be same as jump ball so that jump ball doesn't trigger possession change.

`pbpstats.possession_details.TeamHasBackToBackPossessionsException: GameId: 0021800015, Period: 3, Possession Number: 8, Event: Smith REBOUND (Off:0 Def:5)`

```
...
["0021800015", 411, 1, 1, 3, "9:41 PM", "10:12", null, null, "Richardson 25' 3PT Jump Shot (12 PTS) (Dragic 7 AST)", "66 - 62", "-4", 5, 1626196, "Josh Richardson", 1610612748, "Miami", "Heat", "MIA", 5, 201609, "Goran Dragic", 1610612748, "Miami", "Heat", "MIA", 0, 0, null, null, null, null, null, 1], 
["0021800015", 413, 6, 6, 3, "9:41 PM", "10:11", "Smith AWAY.FROM.PLAY.FOUL (P4.T3) (S.Wright)", null, null, null, null, 4, 201160, "Jason Smith", 1610612764, "Washington", "Wizards", "WAS", 5, 202355, "Hassan Whiteside", 1610612748, "Miami", "Heat", "MIA", 1, 0, null, null, null, null, null, 1], 
["0021800015", 415, 5, 0, 3, "9:41 PM", "10:11", "Smith No Turnover (P2.T8)", null, null, null, null, 4, 201160, "Jason Smith", 1610612764, "Washington", "Wizards", "WAS", 0, 0, null, null, null, null, null, 1, 0, null, null, null, null, null, 1], 
["0021800015", 416, 3, 10, 3, "9:42 PM", "10:11", null, null, "MISS Whiteside Free Throw 1 of 1", null, null, 5, 202355, "Hassan Whiteside", 1610612748, "Miami", "Heat", "MIA", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
...
```

Richardson shot should have same time as Smith foul so that Richardson shot doesn't trigger possession end, change time on it to 10:11.


### Rebound credited to team committing loose ball foul

`pbpstats.possession_details.TeamHasBackToBackPossessionsException: GameId: 0021800022, Period: 4, Possession Number: 8, Event: Mirotic REBOUND (Off:1 Def:7)`

```
...
["0021800022", 544, 2, 1, 4, "10:00 PM", "10:49", null, null, "MISS Jackson 9' Jump Shot", null, null, 5, 1628382, "Justin Jackson", 1610612758, "Sacramento", "Kings", "SAC", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800022", 545, 4, 0, 4, "10:01 PM", "10:48", "PELICANS Rebound", null, null, null, null, 2, 1610612740, null, null, null, null, null, 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
["0021800022", 546, 6, 3, 4, "10:01 PM", "10:48", "Randle L.B.FOUL (P4.T1) (S.Corbin)", null, null, null, null, 4, 203944, "Julius Randle", 1610612740, "New Orleans", "Pelicans", "NOP", 5, 1628382, "Justin Jackson", 1610612758, "Sacramento", "Kings", "SAC", 1, 0, null, null, null, null, null, 1],
...
```

Change Pelicans Rebound to Kings Rebound (replace 1610612740 with 1610612758)

### Offensive foul creditted as personal foul and no turnover

```
...
["0021800062", 622, 6, 1, 4, "12:46 AM", "4:32", "Bell P.FOUL (P2.PN) (M.Ayotte)", null, null, null, null, 4, 1628395, "Jordan Bell", 1610612744, "Golden State", "Warriors", "GSW", 5, 1628972, "Troy Brown Jr.", 1610612764, "Washington", "Wizards", "WAS", 1, 0, null, null, null, null, null, 1],
["0021800062", 624, 5, 0, 4, "12:46 AM", "4:32", "Bell No Turnover (P1.T16)", null, null, null, null, 4, 1628395, "Jordan Bell", 1610612744, "Golden State", "Warriors", "GSW", 0, 0, null, null, null, null, null, 1, 0, null, null, null, null, null, 1],
...
```

change to:
```
["0021800062", 622, 6, 4, 4, "12:46 AM", "4:32", "Bell OFF.Foul (P2.PN) (M.Ayotte)", null, null, null, null, 4, 1628395, "Jordan Bell", 1610612744, "Golden State", "Warriors", "GSW", 5, 1628972, "Troy Brown Jr.", 1610612764, "Washington", "Wizards", "WAS", 1, 0, null, null, null, null, null, 1],
["0021800062", 624, 5, 37, 4, "12:46 AM", "4:32", "Bell Offensive Foul Turnover (P1.T16)", null, null, null, null, 4, 1628395, "Jordan Bell", 1610612744, "Golden State", "Warriors", "GSW", 0, 0, null, null, null, null, null, 1, 0, null, null, null, null, null, 1],
```

### Non away from play foul creditted as away from play foul

`pbpstats.possession_details.TeamHasBackToBackPossessionsException: GameId: 0021800089, Period: 3, Possession Number: 45, Event: Mason 10' Driving Floating Jump Shot (2 PTS)`

```
...
["0021800089", 491, 1, 1, 3, "9:11 PM", "2:54", null, null, "Hield 24' 3PT Jump Shot (23 PTS) (Jackson 1 AST)", "85 - 69", "-16", 5, 1627741, "Buddy Hield", 1610612758, "Sacramento", "Kings", "SAC", 5, 1628382, "Justin Jackson", 1610612758, "Sacramento", "Kings", "SAC", 0, 0, null, null, null, null, null, 1],
["0021800089", 493, 6, 6, 3, "9:11 PM", "2:48", null, null, "Jackson AWAY.FROM.PLAY.FOUL (P2.PN) (C.Blair)", null, null, 5, 1628382, "Justin Jackson", 1610612758, "Sacramento", "Kings", "SAC", 4, 1626196, "Josh Richardson", 1610612748, "Miami", "Heat", "MIA", 1, 0, null, null, null, null, null, 1],
["0021800089", 495, 3, 11, 3, "9:12 PM", "2:48", "Richardson Free Throw 1 of 2 (21 PTS)", null, null, "85 - 70", "-15", 4, 1626196, "Josh Richardson", 1610612748, "Miami", "Heat", "MIA", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
["0021800089", 496, 3, 12, 3, "9:12 PM", "2:48", "Richardson Free Throw 2 of 2 (22 PTS)", null, null, "85 - 71", "-14", 4, 1626196, "Josh Richardson", 1610612748, "Miami", "Heat", "MIA", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
["0021800089", 497, 1, 101, 3, "9:12 PM", "2:32", null, null, "Mason 10' Driving Floating Jump Shot (2 PTS)", "87 - 71", "-16", 5, 1628412, "Frank Mason", 1610612758, "Sacramento", "Kings", "SAC", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
...
```

change this event:
```
["0021800089", 493, 6, 6, 3, "9:11 PM", "2:48", null, null, "Jackson AWAY.FROM.PLAY.FOUL (P2.PN) (C.Blair)", null, null, 5, 1628382, "Justin Jackson", 1610612758, "Sacramento", "Kings", "SAC", 4, 1626196, "Josh Richardson", 1610612748, "Miami", "Heat", "MIA", 1, 0, null, null, null, null, null, 1],
```

to:
```
["0021800089", 493, 6, 1, 3, "9:11 PM", "2:48", null, null, "Jackson P.FOUL (P2.PN) (C.Blair)", null, null, 5, 1628382, "Justin Jackson", 1610612758, "Sacramento", "Kings", "SAC", 4, 1626196, "Josh Richardson", 1610612748, "Miami", "Heat", "MIA", 1, 0, null, null, null, null, null, 1],
```

### Inbound foul as away from play foul
```
["0021800173", 352, 6, 6, 2, "11:09 PM", "0:00", "Cauley-Stein AWAY.FROM.PLAY.FOUL (P2.PN) (M.Myers)", null, null, null, null, 4, 1626161, "Willie Cauley-Stein", 1610612758, "Sacramento", "Kings", "SAC", 5, 1626157, "Karl-Anthony Towns", 1610612750, "Minnesota", "Timberwolves", "MIN", 1, 0, null, null, null, null, null, 1],
["0021800173", 354, 3, 10, 2, "11:09 PM", "0:00", null, null, "Towns Free Throw 1 of 1 (29 PTS)", "61 - 63", "2", 5, 1626157, "Karl-Anthony Towns", 1610612750, "Minnesota", "Timberwolves", "MIN", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
```

Change to inbound foul (mtype 6 to mtype 5)


### Edit time on events
`pbpstats.possession_details.TeamHasBackToBackPossessionsException: GameId: 0021800256, Period: 3, Possession Number: 3, Event: Nwaba STEAL (1 STL): James Bad Pass Turnover (P3.T10)`

```
...
["0021800256", 310, 1, 47, 3, "9:29 PM", "10:50", "Nwaba 10' Turnaround Jump Shot (2 PTS)", null, null, "51 - 54", "3", 4, 1628021, "David Nwaba", 1610612739, "Cleveland", "Cavaliers", "CLE", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800256", 311, 6, 2, 3, "9:29 PM", "10:50", null, null, "Ingram S.FOUL (P2.T1) (J.DeRosa)", null, null, 5, 1627742, "Brandon Ingram", 1610612747, "Los Angeles", "Lakers", "LAL", 4, 1628021, "David Nwaba", 1610612739, "Cleveland", "Cavaliers", "CLE", 1, 0, null, null, null, null, null, 1],
["0021800256", 313, 3, 10, 3, "9:29 PM", "10:50", "MISS Nwaba Free Throw 1 of 1", null, null, null, null, 4, 1628021, "David Nwaba", 1610612739, "Cleveland", "Cavaliers", "CLE", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
["0021800256", 314, 4, 0, 3, "9:29 PM", "10:50", "Thompson REBOUND (Off:6 Def:3)", null, null, null, null, 4, 202684, "Tristan Thompson", 1610612739, "Cleveland", "Cavaliers", "CLE", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800256", 315, 1, 97, 3, "9:29 PM", "10:50", "Thompson 1' Tip Layup Shot (12 PTS)", null, null, "51 - 56", "5", 4, 202684, "Tristan Thompson", 1610612739, "Cleveland", "Cavaliers", "CLE", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
...
```

To account for shot/foul events sometimes being out of order, only the time is used to check for and 1s which sometimes raises exceptions when another shot is made at the same time. Just change the time by 1 second for the second shot to fix it.


### 6 starters for period - caused by player appearing in pbp before being subbed in

`pbpstats.game_data.InvalidNumberOfStartersException: GameId: 0021800258, Period: 2, TeamId: 1610612745`

```
...
["0021800258", 235, 3, 12, 2, "8:48 PM", "7:05", null, null, "MISS Drummond Free Throw 2 of 2", null, null, 5, 203083, "Andre Drummond", 1610612765, "Detroit", "Pistons", "DET", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 0],
["0021800258", 236, 4, 0, 2, "8:48 PM", "7:05", "Tucker REBOUND (Off:0 Def:3)", null, null, null, null, 4, 200782, "PJ Tucker", 1610612745, "Houston", "Rockets", "HOU", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1],
["0021800258", 227, 8, 0, 2, "8:48 PM", "7:05", "SUB: Tucker FOR Clark", null, null, null, null, 4, 1629109, "Gary Clark", 1610612745, "Houston", "Rockets", "HOU", 4, 200782, "PJ Tucker", 1610612745, "Houston", "Rockets", "HOU", 0, 0, null, null, null, null, null, 0],
...
```

Move sub event to before free throw


### Lane Violation on FT 1 of 2 creditted as a turnover

`pbpstats.possession_details.TeamHasBackToBackPossessionsException: GameId: 0021800546, Period: 2, Possession Number: 36, Event: Towns Free Throw 2 of 2 (6 PTS)`

change:
```
["0021800546", 312, 5, 17, 2, "8:52 PM", "3:46", null, null, "Covington Lane Violation Turnover (P1.T3)", null, null, 5, 203496, "Robert Covington", 1610612750, "Minnesota", "Timberwolves", "MIN", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1]
```

to:
```
["0021800546", 312, 7, 3, 2, "8:52 PM", "3:46", null, null, "Covington Lane Violation", null, null, 5, 203496, "Robert Covington", 1610612750, "Minnesota", "Timberwolves", "MIN", 0, 0, null, null, null, null, null, 0, 0, null, null, null, null, null, 1]
```