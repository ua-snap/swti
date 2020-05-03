"""
Responsible for fetching, preprocessing
and caching community data.
"""
# pylint: disable=C0103, E0401

import urllib.parse
import os
import datetime
import logging
import numpy as np
import pandas as pd
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import luts

DASH_LOG_LEVEL = os.getenv("DASH_LOG_LEVEL", default="info")
logging.basicConfig(level=getattr(logging, DASH_LOG_LEVEL.upper(), logging.INFO))

API_URL = os.getenv("ACIS_API_URL", default="http://data.rcc-acis.org/StnData?")
logging.info("Using ACIS API url %s", API_URL)

# Set up cache.
CACHE_EXPIRE = int(os.getenv("DASH_CACHE_EXPIRE", default="43200"))
logging.info("Cache expire set to %s seconds", CACHE_EXPIRE)
cache_opts = {"cache.type": "memory"}

cache = CacheManager(**parse_cache_config_options(cache_opts))
data_cache = cache.get_cache("api_data", type="memory", expire=CACHE_EXPIRE)


def fetch_api_data():
    """
    Reads data from ACIS API for selected community.
    """
    if os.getenv("FLASK_DEBUG", default=None):
        logging.info("Using debug mode & local data")
        std = pd.read_csv("data/test-daily-index.csv", index_col=0)
    else:
        # TODO implement
        logging.info("Sending upstream data API request")
        raise NotImplementedError("This isn't implemented yet.")

    # Perform some final data prep here
    # Assign fancy colors
    std["color"] = pd.Series(
        np.digitize(std["daily_index"], [-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10])
    ).apply(lambda x: luts.colors[x - 1])

    return std


def fetch_data():
    """
    Fetches preprocessed data from cache,
    or triggers an API request + preprocessing.
    """
    return data_cache.get(key="statewide_temp_index", createfunc=fetch_api_data)
