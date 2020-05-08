.. _quickstart:

Installation
================

.. code-block:: bash

    $ pip install pbpstats

Setup data directory (optional but recommended)
===============================================
To avoid repeating the same requests multiple times, and to allow for manually fixing issues with
the raw play-by-play data I recommend setting up a data directory to save the response data. This will limit the number
of requests you make to the NBA Stats API and allow you to manually fix issues with the raw data.
Within this directory you will need to add four subdirectories(game_details, overrides, pbp and schedule).
To use the directory, just include it in your settings when initializing the client like in the example below.
This directory is also where `override files <https://github.com/dblackrun/pbpstats/wiki/Overrides-to-fix-issues-parsing-pbp>`_
to fix periods starters and handle issues with parsing pbp that can't be fixed by editing pbp file are placed.

Download data
-------------
If you want data with pbp event order fixed as well as overrides that are up to date as of
this release you can download the files from `here <https://pbpstats.s3.amazonaws.com/data.zip>`_.
Unzip it and use the unzipped directory as your data directory.

data.nba.com vs stats.nba.com
-----------------------------
The data from both these sources is mostly the same but there are a few small differences. The data.nba.com play-by-play
has the offense team id in all events, which makes it easier to track possession changes. The stats.nba.com events do not have
this attribute and to get possession counts the play-by-play needs to be parsed, which makes it more sensitive to events being in
the correct order. The stats.nba.com play-by-play also has lots of shots and rebounds that are out of order that need to be fixed
manually. If you download the data from the link above, I have fixed these for previous seasons, but going forward if you use
this you will have to keep up with fixing them manually yourself. If you don't care if there may be an occasional possession
count being off or you don't want to deal with manually fixing the event order I suggest using data.nba.com for your play-by-play provider.

The stats.nba.com has more older season data available. So it should be used if you want to work with older data.

Another difference is that the data.nba.com play-by-play updates in real time, so if you are looking to do live stats during a game you
can use it for that.

Basic Usage
==============
Within your settings that will be passed into the client when you instantiate it you can set the
data directory and set the resources and data source you want.

Options for ``source`` are 'file' and 'web'. When source is 'file', it will pull data from the ``dir`` specified in the settings.
When source is 'web' it will make an API request to get the data. If you want to save the response data to disk set ``dir`` within
the settings and it will be saved in the appropriate subdirectory.

Options for ``data_provider`` are 'stats_nba' and 'data_nba'.

See the code examples below for some examples settings.

Resource options are:

* Boxscore - basic boxscore stats
* EnhancedPbp - more detail than the basic play-by-play
* Games - for getting all games for a season or date
* Pbp - raw play-by-play
* Possessions - splits enhanced pbp data up into possessions.
* Shots (stats.nba.com only)

Code Examples
================
Game Data
----------
The following code will instantiate the client and instantiate the Game data
object for the given game id with boxscore and possession data.

.. code-block:: python

    from pbpstats.client import Client

    settings = {
        "dir": "/response_data",
        "Boxscore": {"source": "file", "data_provider": "stats_nba"},
        "Possessions": {"source": "file", "data_provider": "stats_nba"},
    }
    client = Client(settings)
    game = client.Game("0021900001")

Resource data can be accessed by calling game.<snake_case_resource_name>.items. In this case,
since 'Boxscore' and 'Possessions' were provided in the settings dict boxscore and possessions data
can be accessed via ``game.boxscore.items`` and ``game.possessions.items``. See
:obj:`~pbpstats.resources.possessions.possessions.Possessions` for properties for working with possessions data. See
:obj:`~pbpstats.resources.boxscore.boxscore.Boxscore` for properties for working with boxscore data.

All Final Games For Season
----------------------------
The following code can be used to get all final games for a season.

.. code-block:: python

    from pbpstats.client import Client

    settings = {
        "Games": {"source": "web", "data_provider": "data_nba"},
    }
    client = Client(settings)
    season = client.Season("nba", "2019-20", "Regular Season")

    for final_game in season.games.final_games:
        print(final_game)

All Final Games For Day
-----------------------
The following code can be used to get all final games for a season.
Note that for day, ``data_provider`` must be ``stats_nba``

.. code-block:: python

    from pbpstats.client import Client

    settings = {
        "Games": {"source": "web", "data_provider": "stats_nba"},
    }
    client = Client(settings)
    day = client.Day("12/05/2019", "nba")

    for final_game in day.games.final_games:
        print(final_game)

Doing Detailed Stuff with Possession Data
------------------------------------------
The following code will get all possessions that start off a missed field goal.

.. code-block:: python

    off_rim_miss = [possession for possession in game.possessions.items if possession.possession_start_type == "OffAtRimMiss"]

For more on what is available for possession data see :obj:`~pbpstats.resources.possessions.possession.Possession` docs

Doing Detailed Stuff with Enhanced PBP Data
---------------------------------------------
The following code will get the average 2pt shot distance on all missed field goals.

.. code-block:: python

    from pbpstats.resources.enhanced_pbp import FieldGoal

    ...

    shot_dists = []
    for possession in game.possessions.items:
        for possession_event in possession.events:
            if isinstance(possession_event, FieldGoal) and not possession_event.is_made and possession_event.shot_value == 2:
                shot_dists.append(possession_event.distance)
    print(sum(shot_dists) / len(shot_dists))

For more on what is available for enhanced pbp data see :mod:`pbpstats.resources.enhanced_pbp` docs

Note on Ids
===============
Player and team Ids the same player and team ids used by stats.nba.com. Lineup ids are '-' separated player ids (with player ids sorted as strings).

Issues with raw play-by-play
============================
If you need to fix event order in the play-by-play file you will need to open the pbp file for the game in your data directory
and change the order of the events list. Each event is a list and searching for the event number (the event number should be
in the exception text somewhere) to find the event is a good place to start to figure out which event needs to be moved around.
