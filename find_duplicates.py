import os
import json
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm
from collections import defaultdict


def find_duplicates_by_filename(data_path, out_duplicates_dir):

	dataframes = []
	index = 0
	file_counter = Counter()
	duplicate_files = defaultdict(list)
	file_count = {}

	for user_folder in tqdm(os.listdir(data_path)):
		user_folder_path = os.path.join(data_path, user_folder)
		user_id = os.path.basename(user_folder_path)

		if os.path.isdir(user_folder_path):
			trajectory_dir = os.path.join(user_folder_path, 'Trajectory')

			if os.path.exists(trajectory_dir) and os.path.isdir(trajectory_dir):

				for trajectory_file in os.listdir(trajectory_dir):
					if trajectory_file.endswith('.plt'):
						file_name = trajectory_file
						if user_id in file_count.keys():
							file_count[user_id]+=1
						else:
							file_count[user_id]=1

						if file_name in duplicate_files:
							duplicate_files[file_name].append(user_id)
						else:
							duplicate_files[file_name] = [user_id]

	total_files = []
	for k in file_count.keys():
		total_files.append([str(k), file_count[k]])
	total_files = pd.DataFrame(total_files, columns=['user','total_count'])

	total_files.to_csv(out_duplicates_dir+'geolife_user_trajectories.csv', index=False)

	total_duplicates = []
	for k in duplicate_files.keys():
		total_duplicates.append([str(k), len(duplicate_files[k]), json.dumps(duplicate_files[k])])
	total_duplicates = pd.DataFrame(total_duplicates, columns=['track','user_count','users'])
	total_duplicates.to_csv(out_duplicates_dir+'geolife_track_duplicates_by_name.csv', index=False)
	
	data = []
	count = 0

	for file_name, folders in duplicate_files.items():
		if len(folders) > 1:
			count += 1        
			for i in range(len(folders)):
				data.append({'file_name': file_name, 'user': str(folders[i]), 'duplicates': json.dumps(folders), "num": len(folders)})

	df = pd.DataFrame(data)
	df.to_csv(out_duplicates_dir+'geolife_user_track_duplicates_by_name.csv', index=False)


def files_are_equal(file_path1, file_path2):
	with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
		file1_content = file1.read()
		file2_content = file2.read()
		return file1_content == file2_content
    

def find_duplicates_by_content(data_path, out_duplicates_dir):
	df = pd.read_csv(out_duplicates_dir+'geolife_user_track_duplicates_by_name.csv', dtype={'user': 'str'})
	thesame = []
	for i in range(len(df)):
		x = df.iloc[i]
		f1 = data_path +  str(x['user']) + "/Trajectory/"+x['file_name']
		duplicates = []
		for j in json.loads(x['duplicates']):
			if str(x['user'])==str(j):
				continue
			f2 = data_path + str(j) + "/Trajectory/"+x['file_name']
			if files_are_equal(f1,f2):
				duplicates.append(j)
		if len(duplicates)>0:
			thesame.append([x['file_name'], str(x['user']) , json.dumps(duplicates), len(duplicates)])
	thesame = pd.DataFrame(thesame, columns=df.columns)
	thesame.to_csv(out_duplicates_dir+'geolife_user_track_duplicates_by_content.csv', index=False)