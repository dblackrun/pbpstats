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
* Fixes order of events for some common cases in which events are out of order

# Installation
requires Python >=3.6
```
pip install pbpstats
```

# Setup data directory (optional but recommended)
To avoid repeating the same requests multiple times, and to allow for manually fixing issues with the raw play-by-play data I recommend setting up a data directory to save the response data. Within this directory you will need to add four subdirectories(game_details, overrides, pbp and schedule). To use the directory, just include it in your settings when initializing the client like in the example below. This directory is also where [override files](https://github.com/dblackrun/pbpstats/wiki/Overrides-to-fix-issues-parsing-pbp) to fix periods starters and handle issues with parsing pbp that can't be fixed by editing pbb file are placed.

# Basic Usage
Within your settings you can set the data directory and set the resources and data source you want.

Options for `source` are 'file' and 'web'. When source is 'file', it will pull data from the `dir` specified in the settings. When source is 'web' it will make an API request to get the data. If you want to save the response data to disk set `dir` within the settings and it will be saved in the appropriate subdirectory.

Options for `data_provider` are 'stats_nba' and 'data_nba'. The NBA site has two different APIs - stats.nba.com and data.nba.com. You can pick which one you want to use.

Resource options are:
* Boxscore - basic boxscore stats
* EnhancedPbp - more detail than the basic play-by-play
* Games - for getting all games for a season or date
* Pbp - raw play-by-play
* Possessions - splits enhanced pbp data up into possessions.
* Shots (stats.nba.com only)
```
from pbpstats.client import Client

settings = {
    'dir': '/response_data',
    'Boxscore': {'source': 'file', 'data_provider': 'stats_nba'},
    'Possessions': {'source': 'file', 'data_provider': 'stats_nba'},
}
client = Client(settings)
game = client.Game('0021900001')

```
Resource data can be accessed by calling game.<snake_case_resource_name>.items
```
for possession in game.possessions.items:
    print(possession)
```

There are also properties to access some basic data

to get player stats for game:
```
player_stats = game.possessions.player_stats
```

to get team stats for game:
```
team_stats = game.possessions.team_stats
```
to get opponent stats for game:
```
opponent_stats = game.possessions.opponent_stats
```
to get lineup stats for game:
```
lineup_stats = game.possessions.lineup_stats
```
to get lineup opponent stats for game:
```
lineup_opponent_stats = game.lineup_opponent_stats
```

to get player name map:
```
game.boxscore.player_name_map
```

to get player team map:
```
game.boxscore.player_team_map
```

to get all shots for enhanced pbp:
```
game.enhanced_pbp.fgas
```

To get all final games for a season
```
from pbpstats.client import Client

settings = {
    'Games': {'source': 'web', 'data_provider': 'data_nba'},
}
client = Client(settings)
season = client.Season('nba', '2019-20', 'Regular Season')

for final_game in season.games.final_games:
    print(final_game)
```

To get all final games for a day
```
from pbpstats.client import Client

settings = {
    'Games': {'source': 'web', 'data_provider': 'stats_nba'},
}
client = Client(settings)
day = client.Day('12/05/2019', 'nba')

for final_game in day.games.final_games:
    print(final_game)
```

# Note on Ids
Player and team Ids the same player and team ids used by stats.nba.com. Lineup ids are '-' separated player ids (with player ids sorted as strings).

# Issues with raw play-by-play
[See here](https://github.com/dblackrun/pbpstats/wiki/Fixing-issues-with-raw-play-by-play) for how to edit and fix common issues with play-by-play data.
