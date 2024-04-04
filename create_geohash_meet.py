import os
import json
from tqdm import tqdm
import numpy as np
import pandas as pd

def createGeohashMeetJsons(in_file, out_dir):
	geohash_data = pd.read_csv(in_file)

	# create pairs of meetings for two persons
	locations_meets = []
	print("loaded")
	geohash_count = len(geohash_data['Geohash'].unique())
	print(geohash_count)
	print("grouping...")
	codes = geohash_data.groupby('Geohash')
	print("grouped")

	t = 0
	k = 0
	tx = 0
	for code, group in codes:
		if t % 1000 == 0:
			print(str(t / float(geohash_count)), t, '/', geohash_count)

		t += 1
		lat = group['Latitude'].mean()
		lon = group['Longitude'].mean()
		meets = {}
		value_indices = group.index.values.tolist()
		column_keys = group.keys().tolist()
		column_keys.append('Index')
		index_i = 0
		for value in group.values:
			vx = value.tolist()
			vx.append(value_indices[index_i])
			index_i+=1
			if value[column_keys.index('Person ID')] in meets.keys():
				meets[value[column_keys.index('Person ID')]].append(vx)
			else:
				meets[value[column_keys.index('Person ID')]] = [vx]
			tx+=1

		locations_meets.append({
			'geohash': code,
			"meets_keys": column_keys,
			"meets": meets,
			'Latitude': lat,
			'Longitude': lon
		})


		if tx >= 10000:
			if not (os.path.isdir(out_dir)):
				os.makedirs(out_dir)

			with open(out_dir + 'geolife_geohash_meet_' + str(k) + '.json', 'w') as json_file:
				json.dump(locations_meets, json_file, indent=4)

			k += 1
			locations_meets = []

	print(str(t / float(geohash_count)), t, '/', geohash_count)

	if len(locations_meets) > 0:
		if not (os.path.isdir(out_dir)):
			os.makedirs(out_dir)

		with open(out_dir + 'geolife_geohash_meet_' + str(k) + '.json', 'w') as json_file:
			json.dump(locations_meets, json_file, indent=4)

		k += 1
	return k

def createGeohashMeetCSV(count_files, in_dir, out_file):
	meets = []
	for i in tqdm(range(count_files)):
		d = pd.read_json(in_dir + 'geolife_geohash_meet_' + str(i) + '.json')
		d['meets'] = d['meets'].apply(json.dumps)
		d['meets_keys'] = d['meets_keys'].apply(json.dumps)
		meets.append(d.copy(deep=True))
	meets = pd.concat(meets)
	meets.to_csv(out_file, index=False)