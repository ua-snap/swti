# Script to generate the station normals
# from upstream NCEI data.  This shouldn't
# need to be run on an ongoing basis,
# only if there are corrections in the NCEI
# data (rare).
import pandas as pd

station_ids = [
    "USW00026451", # USW00026451=ANCHORAGE
    "USW00027502", # USW00027502=BARROW
    "USW00026615", # USW00026615=BETHEL
    "USW00026533", # USW00026533=BETTLES
    "USW00025624", # USW00025624=COLD
    "USW00026410", # USW00026410=CORDOVA
    "USW00027406", # USW00027406=DEADHORSE
    "USW00026422", # USW00026422=EAGLE
    "USW00026411", # USW00026411=FAIRBANKS
    "USW00026425", # USW00026425=GULKANA
    "USW00025323", # USW00025323=HAINES
    "USW00025507", # USW00025507=HOMER
    "USW00025506", # USW00025506=ILIAMNA
    "USW00025309", # USW00025309=JUNEAU
    "USW00026502", # USW00026502=KALTAG
    "USW00025325", # USW00025325=KETCHIKAN
    "USW00025503", # USW00025503=KING
    "USW00025501", # USW00025501=KODIAK
    "USW00026616", # USW00026616=KOTZEBUE
    "USW00026510", # USW00026510=MCGRATH
    "USW00026617", # USW00026617=NOME
    "USW00026412", # USW00026412=NORTHWAY
    "USW00026528", # USW00026528=TALKEETNA
    "USW00026529", # USW00026529=TANANA
    "USW00025339", # USW00025339=YAKUTAT
]

normals = pd.DataFrame()
station_csvs = []

for station in station_ids:
    url = f"https://www.ncei.noaa.gov/data/normals-daily/1991-2020/access/{station}.csv"
    print(f"Fetching {url} ...")
    station_data = pd.read_csv(url)

    # Add a synthetic "day" column for grouping / viz w/ Plotly
    station_data["date"] = station_data["DATE"] + "-2020"
    # Reshape to yield StationName,AveTemp,AveTempSD,date
    station_data.drop(
        station_data.columns.difference(
            ["STATION", "DLY-TAVG-NORMAL", "DLY-TAVG-STDDEV", "date"]
        ),
        axis=1,
        inplace=True,
    )
    station_data.rename(columns={"STATION": "StationName", "DLY-TAVG-NORMAL": "AveTemp", "DLY-TAVG-STDDEV": "AveTempSD"}, inplace=True)
    station_csvs.append(station_data)

normals = pd.concat(station_csvs)
normals.to_csv("normals.csv")