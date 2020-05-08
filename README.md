[![Build Status](https://travis-ci.org/dblackrun/pbpstats.svg?branch=master)](https://travis-ci.org/dblackrun/pbpstats)
[![PyPI version](https://badge.fury.io/py/pbpstats.svg)](https://badge.fury.io/py/pbpstats)
[![Downloads](https://pepy.tech/badge/pbpstats)](https://pepy.tech/project/pbpstats)

A package to scrape and parse NBA, WNBA and G-League play-by-play data.

# Features
* Adds lineup on floor for all events
* Adds detailed data for each possession including start time, end time, score margin, how the previous possession ended
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

# Resources
[Documentation](https://pbpstats.readthedocs.io/en/latest/)
