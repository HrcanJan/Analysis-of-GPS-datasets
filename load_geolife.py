from tqdm import tqdm
import os
import numpy as np
import pandas as pd


def load_geolife(data_path, out_file, out_labels):


    # Create an empty list to store DataFrames
    dataframes = []
    index = 0

    # Traverse through user directories
    for user_folder in tqdm(os.listdir(data_path)):
        user_folder_path = os.path.join(data_path, user_folder)

        # Check if it's a directory
        if os.path.isdir(user_folder_path):
            trajectory_dir = os.path.join(user_folder_path, 'Trajectory')

            # Check if 'Trajectory' directory exists
            if os.path.exists(trajectory_dir) and os.path.isdir(trajectory_dir):
                # Loop through trajectory files for each user
                for trajectory_file in os.listdir(trajectory_dir):
                    if trajectory_file.endswith('.plt'):
                        trajectory_file_path = os.path.join(trajectory_dir, trajectory_file)
                        df = pd.read_csv(trajectory_file_path, header=None, skiprows=6)
                        df.insert(0, 'person', trajectory_file.replace(".plt", ""))
                        df.insert(0, 'file', int(user_folder))
                        dataframes.append(df)
                index += 1

    gps_data = pd.concat(dataframes, ignore_index=True)
    column_names = ['Person ID', 'Trajectory', 'Latitude', 'Longitude', '0', 'Altitude', 'NumDays', 'Date', 'Time']
    gps_data.columns = column_names
    gps_data['Timestamp'] = pd.to_datetime(gps_data['Date'] + ' ' + gps_data['Time'])
    gps_data = gps_data.drop(columns=['NumDays', 'Date', 'Time', '0'])
    gps_data = gps_data[gps_data['Latitude'] >= 39.75]
    gps_data = gps_data[gps_data['Latitude'] <= 40.1]
    gps_data = gps_data[gps_data['Longitude'] >= 116.18]
    gps_data = gps_data[gps_data['Longitude'] <= 116.6]
    gps_data.to_csv(out_file, index=False)

    # Create an empty list to store DataFrames
    dataframes = []

    # Traverse through user directories
    for user_folder in os.listdir(data_path):
        user_folder_path = os.path.join(data_path, user_folder)

        labels_file_path = os.path.join(user_folder_path, 'labels.txt')

        # Check if the labels file exists
        if os.path.exists(labels_file_path):
            labels_df = pd.read_csv(labels_file_path, sep='\t')

            dataframes.append(labels_df)

    data_labels = pd.concat(dataframes, ignore_index=True)
    data_labels.to_csv(out_labels, index=False)
