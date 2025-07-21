import fastf1
from fastf1 import plotting
from fastf1.ergast import Ergast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Enable cache to reduce rate limit on repeated requests
fastf1.Cache.enable_cache("../f1_cache")

TRACK_KMS = {
    "Spa": 7.004,
    "Baku": 6.003,
    "Silverstone": 5.891,
    "Sochi": 5.848,
    "Paul Ricard": 5.841,
    "Suzuka": 5.807,
    "Monza": 5.793,
    "Yas Marina": 5.554,
    "COTA": 5.513,
    "Shanghai": 5.451,
    "Bahrain": 5.412,
    "Melbourne": 5.303,
    "Singapore": 5.065,
    "Catalunya": 4.655,
    "Hockenheim": 4.574,
    "Hungaroring": 4.381,
    "Montreal": 4.361,
    "Red Bull Ring": 4.318,
    "Interlagos": 4.309,
    "Mexico City": 4.304,
    "Monaco": 3.337
}

years = [2022, 2023, 2024]
race_name = "Belgium"   # Will make this an input variable later
output_path = "../data_store/race_quali_data.csv"
CAN_RAIN = False    # Will make this a input or something to make it easier to change

records = []
for year in years:
    try:
        # do something
        quali = fastf1.get_session(year, race_name, "Q")
        quali.load()

        race = fastf1.get_session(year, race_name, "R")
        race.load()

        weather_data = race.weather_data
        weather_data = weather_data.groupby(["Rainfall"]).mean()
        # Need to change the dictonary key to location instead of track name
        track_length_km = TRACK_KMS["Spa"]

        for drv in quali.drivers:
            try:
                # Do Something
                quali_laps = quali.laps.pick_driver(drv).pick_accurate()
                driver_best = quali_laps[~quali_laps['PitOutTime'].notna(
                ) & ~quali_laps['PitInTime'].notna() & quali_laps['IsPersonalBest'] == True].pick_fastest()
                quali_time = driver_best.LapTime.total_seconds()

                race_laps = race.laps.pick_driver(drv).pick_accurate()
                race_laps = race_laps[~race_laps['PitOutTime'].notna(
                ) & ~race_laps['PitInTime'].notna()]
                if race_laps.empty:
                    continue
                avg_lap_time = race_laps['LapTime'].mean().total_seconds()
                compound_counts = race_laps['Compound'].value_counts(
                ).to_dict()
                compound_used = max(compound_counts, key=compound_counts.get)
                avg_sector_one = race_laps["Sector1Time"].dt.total_seconds(
                ).mean()
                avg_sector_two = race_laps["Sector2Time"].dt.total_seconds(
                ).mean()
                avg_sector_three = race_laps["Sector3Time"].dt.total_seconds(
                ).mean()
                driver_team = race.get_driver(drv)['TeamName']

                records.append({
                    'Year': year,
                    'Race': race_name,
                    'Driver': drv,
                    'Team': driver_team,
                    'QualiTime': quali_time,
                    'RaceTimeAvg': avg_lap_time,
                    'Compound': compound_used,
                    'Sector1Avg': avg_sector_one,
                    'Sector2Avg': avg_sector_two,
                    'Sector3Avg': avg_sector_three,
                    'AirTemp': weather_data.loc[CAN_RAIN]['AirTemp'],
                    'TrackTemp': weather_data.loc[CAN_RAIN]['TrackTemp'],
                    'Humidity': weather_data.loc[CAN_RAIN]['Humidity'],
                    'WindSpeed': weather_data.loc[CAN_RAIN]['WindSpeed'],
                    'TrackLengthKM': track_length_km
                })
            except Exception as ex:
                print(f"Driver {drv} failed: {ex}")

    except Exception as e:
        print(f"Year {year} failed: {e}")

all_data = pd.DataFrame(records)
all_data.dropna(inplace=True)
all_data.to_csv(output_path, index=False)
print(f"✅ Saved dataset with {len(all_data)} rows to {output_path}")
