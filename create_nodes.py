import pandas as pd

def create_nodes():
    gps_data = pd.read_csv('data/geolife_geohash_size_8.csv')
    unique_taxi_ids = gps_data['Person ID'].unique()
    unique_taxi_ids_df = pd.DataFrame({'Person ID': unique_taxi_ids})
    unique_taxi_ids_df = unique_taxi_ids_df.sort_values(by='Person ID')
    unique_taxi_ids_df = unique_taxi_ids_df.reset_index(drop=True)
    unique_taxi_ids_df.to_csv('data/geolife_nodes.csv', index=False)