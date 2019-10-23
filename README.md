[![Build Status](https://travis-ci.org/dblackrun/pbpstats.svg?branch=master)](https://travis-ci.org/dblackrun/pbpstats)
[![PyPI version](https://badge.fury.io/py/pbpstats.svg)](https://badge.fury.io/py/pbpstats)
[![Downloads](https://pepy.tech/badge/pbpstats)](https://pepy.tech/project/pbpstats)

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
[See here](https://github.com/dblackrun/pbpstats/wiki/Fixing-issues-with-raw-play-by-play) for how to edit and fix common issues with play-by-play data.