import pandas as pd

def create_nodes(in_file, out_file):
    gps_data = pd.read_csv(in_file)
    unique_taxi_ids = gps_data['Person ID'].unique()
    unique_taxi_ids_df = pd.DataFrame({'Person ID': unique_taxi_ids})
    unique_taxi_ids_df = unique_taxi_ids_df.sort_values(by='Person ID')
    unique_taxi_ids_df = unique_taxi_ids_df.reset_index(drop=True)
    unique_taxi_ids_df.to_csv(out_file, index=False)