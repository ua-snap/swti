"""
Responsible for fetching, preprocessing
and caching community data.
"""
# pylint: disable=C0103, E0401

import urllib.parse
import os
import datetime
import logging
import pandas as pd
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import scipy.stats
import luts

DASH_LOG_LEVEL = os.getenv("DASH_LOG_LEVEL", default="info")
logging.basicConfig(level=getattr(logging, DASH_LOG_LEVEL.upper(), logging.INFO))

MULTI_API_URL = os.getenv("MULTI_ACIS_API_URL", default="http://data.rcc-acis.org/MultiStnData?")
logging.info("Using ACIS API url %s", MULTI_API_URL)

# Set up cache.
CACHE_EXPIRE = int(os.getenv("DASH_CACHE_EXPIRE", default="43200"))
logging.info("Cache expire set to %s seconds", CACHE_EXPIRE)
cache_opts = {"cache.type": "memory"}

cache = CacheManager(**parse_cache_config_options(cache_opts))
data_cache = cache.get_cache("api_data", type="memory", expire=CACHE_EXPIRE)

"""
List of Station IDs to Location:
USW00026451=ANCHORAGE
USW00027502=BARROW
USW00026615=BETHEL
USW00026533=BETTLES
USW00025624=COLD
USW00026410=CORDOVA
USW00027406=DEADHORSE
USW00026422=EAGLE
USW00026411=FAIRBANKS
USW00026425=GULKANA
USW00025323=HAINES
USW00025507=HOMER
USW00025506=ILIAMNA
USW00025309=JUNEAU
USW00026502=KALTAG
USW00025325=KETCHIKAN
USW00025503=KING
USW00025501=KODIAK
USW00026616=KOTZEBUE
USW00026510=MCGRATH
USW00026617=NOME
USW00026412=NORTHWAY
USW00026528=TALKEETNA
USW00026529=TANANA
USW00025339=YAKUTAT
"""
MULTI_STATION_IDS = os.getenv("ACIS_STATION_IDS",
                        default="USW00026451,USW00027502,USW00026615,USW00026533,USW00025624,USW00026410,"
                                "USW00027406,USW00026422,USW00026411,USW00026425,USW00025323,USW00025507,"
                                "USW00025506,USW00025309,USW00026502,USW00025325,USW00025503,USW00025501,"
                                "USW00026616,USW00026510,USW00026617,USW00026412,USW00026528,USW00026529,"
                                "USW00025339")


def build_daily_index(sd):
    # Remove any missing rows.
    sd = sd.dropna()
    stations = pd.read_csv("data/StationsList.txt")
    daily_index = pd.DataFrame(columns=["date", "daily_index"])

    grouped = sd.groupby(["date"])
    for day, group in grouped:

        # Add weights.
        joined = group.set_index("usw").join(stations.set_index("usw"))
        weighted_departure_sd_daily_mean = (
                joined["depart_sd"] * joined["weight"]
        ).mean()
        count = joined.shape[0]

        ww = scipy.stats.norm(0, 0.71074).cdf(weighted_departure_sd_daily_mean)
        if ww < 0.5:
            prob = round(0 - (20 * (0.5 - ww)), 3)
        if ww >= 0.5:
            prob = round(20 * (ww - 0.5), 3)

        # Compute daily index.
        daily_index = daily_index.append(
            {
                "date": day,
                "count": count,
                "daily_index": prob,
            },
            ignore_index=True,
        )
    daily_index["count"] = daily_index["count"].astype("int")
    return daily_index

def fetch_api_data():
    """
    Reads data from ACIS API for selected community.
    """
    if os.getenv("FLASK_DEBUG", default=None):
        logging.info("Using debug mode & local data")
        daily_index = pd.read_csv("data/test-daily-index.csv", index_col=0)
    else:

        # Normals CSV for each station + date
        normals = pd.read_csv("data/normals.csv", index_col=0)
        normals["date"] = pd.to_datetime(normals["date"])

        # Start date of two years ago
        start_date = (datetime.date.today() + datetime.timedelta(days=-732)).strftime("%Y-%m-%d")

        # End date yesterday
        end_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

        logging.info("Sending upstream data API request")

        import time
        st = time.time()
        all_stations = pd.DataFrame()
        query = urllib.parse.urlencode(
            {
                "sids": MULTI_STATION_IDS,
                "sdate": start_date,
                "edate": end_date,
                "elems": "1,2",  # Max temp, min temp
                "output": "json",  # CSV now allowed for multi-day with multi-station
            }
        )
        query = MULTI_API_URL + query

        all_std = pd.read_json(query)
        print("----%.2f seconds----" % (time.time() - st))

        # Date Range indexing for 732 days for 2 years worth of data
        # TODO make the amount of periods dynamic
        daterange = pd.date_range(start_date, periods=732, freq='D')
        for row in all_std["data"]:
            # MultiStnData returns metadata in an indeterminate way from the JSON output.
            # This code searches the metadata list for the USW* station ID.
            matching = [s for s in row['meta']['sids'] if "USW" in s]
            usw = matching[0].split(" ")[0]
            std = pd.DataFrame({"date": daterange, "usw": usw})
            data_df = pd.DataFrame(row['data'], columns=['maxt','mint'])
            std = pd.concat([std,data_df], axis=1)

            # drop missing temperature values
            std = std.loc[(std["maxt"] != "M") & (std["mint"] != "M")]

            std["date"] = pd.to_datetime(std["date"])
            std["maxt"] = std["maxt"].astype("float")
            std["mint"] = std["mint"].astype("float")

            std = std.assign(current_average=std[["maxt", "mint"]].mean(axis=1))

            # Subset for current location
            nd = normals.loc[normals["StationName"] == usw]

            # Make an all-2020 date column to join with normals data properly
            std = std.assign(key_date=std["date"].apply(lambda dt: dt.replace(year=2020)))
            jd = std.set_index("key_date").join(nd.set_index("date"))

            # Departure standard deviation (SD) =
            # (current average - normal average) / normal SD
            jd = jd.assign(
                depart_sd=((jd["current_average"] - jd["AveTemp"]) / jd["AveTempSD"]).round(
                    3
                )
            )
            jd = jd.drop(columns=["StationName"])
            all_stations = all_stations.append(jd)

        daily_index = build_daily_index(all_stations)

    # Assign colors for easy display
    daily_index["color"] = daily_index["daily_index"].apply(lambda x: luts.colors[0] if x <= 0 else luts.colors[1])

    return daily_index

def fetch_data():
    """
    Fetches preprocessed data from cache,
    or triggers an API request + preprocessing.
    """
    return data_cache.get(key="statewide_temp_index", createfunc=fetch_api_data)
