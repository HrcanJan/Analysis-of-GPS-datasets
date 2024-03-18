from tqdm import tqdm
import os
import numpy as np
import pandas as pd
import geohash2 as gh


def create_geohash(lat, lon):
    return gh.encode(lat, lon, precision=8)


def add_geohash():
    gps_data = pd.read_csv('data/geolife_gps_data.csv')
    codes = []
    columns = gps_data.columns.to_list()
    lat = columns.index('Latitude')
    lon = columns.index('Longitude')
    for i in tqdm(range(len(gps_data))):
        codes.append(create_geohash(gps_data.iat[i, lat], gps_data.iat[i, lon]))

    geohash_data = gps_data.copy(deep=True)
    geohash_data['Geohash'] = codes

    geohash_data.to_csv('data/geolife_geohash_size_8.csv', index=False)
