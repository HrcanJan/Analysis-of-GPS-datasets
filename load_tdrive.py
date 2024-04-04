from tqdm import tqdm
import os
import numpy as np
import pandas as pd


def load_tdrive(data_path, out_file):

	dataframes = []
	index = 0
	for file in tqdm(os.listdir(data_path)):
		file_path = os.path.join(data_path, file)

		try:
			column_names = ['Person ID', 'Timestamp', 'Longitude', 'Latitude']
			labels_df = pd.read_csv(file_path, sep=',', names=column_names)

			if labels_df.empty:
				continue

			first_timestamp = pd.to_datetime(labels_df['Timestamp'].iloc[0])
			trajectory_format = first_timestamp.strftime('%Y%m%d%H%M%S')
			labels_df['Trajectory'] = trajectory_format

			dataframes.append(labels_df)
			index += 1
		except pd.errors.EmptyDataError:
			continue

	gps_data = pd.concat(dataframes, ignore_index=True)

	column_names = ['Person ID', 'Timestamp', 'Longitude', 'Latitude', 'Trajectory']
	gps_data.columns = column_names
	gps_data['Timestamp'] = pd.to_datetime(gps_data['Timestamp'])
	gps_data = gps_data[gps_data['Latitude'] >= 39.75]
	gps_data = gps_data[gps_data['Latitude'] <= 40.1]
	gps_data = gps_data[gps_data['Longitude'] >= 116.18]
	gps_data = gps_data[gps_data['Longitude'] <= 116.6]
	gps_data.to_csv(out_file, index=False)
