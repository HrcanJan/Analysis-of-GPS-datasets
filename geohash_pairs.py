import pandas as pd
import json
from tqdm import tqdm

def create_date_pairs(in_file, out_file):
	df = pd.read_csv(in_file)

	df['Start Time'] = pd.to_datetime(df['Start Time'])
	df['End Time'] = pd.to_datetime(df['End Time'])
	df['Date'] = df['Start Time'].dt.date

	grouped = df.groupby(['Geohash', 'Date'])
	meets = []

	for (geohash, date), group in tqdm(grouped):
		user_grouped = group.groupby('Person ID')
		ids = []
		for person, value in user_grouped:
			ids.append(person)
		if len(ids)>1:
			meets.append([geohash, date, ids, len(ids)])

	df = pd.DataFrame(meets, columns=['geohash','date','persons', 'count_persons'])
	df.to_csv(out_file, index=False)


def create_pairs(in_file, out_dir, out_file):
	df = pd.read_csv(in_file)

	df['Start Time'] = pd.to_datetime(df['Start Time'])
	df['End Time'] = pd.to_datetime(df['End Time'])
	df['Date'] = df['Start Time'].dt.date

	grouped = df.groupby(['Geohash', 'Date'])

	file_i = 0
	cx = ['person_a','person_b','start_time','end_time', 'geohash', 'points_a', 'points_b', 'start_index_a','end_index_a','start_index_b','end_index_b']
	meets = []
	for (geohash, date), group in tqdm(grouped):

		user_grouped = group.groupby('Person ID')
		ids = []
		for person, value in user_grouped:
			ids.append(person)
		for a in range(len(ids)):
			user_a = user_grouped.get_group(ids[a])
			for b in range(a + 1, len(ids)):
				user_b = user_grouped.get_group(ids[b])

				for i, row_a in user_a.iterrows():
					for j, row_b in user_b.iterrows():
						start_i, end_i = row_a['Start Time'], row_a['End Time']
						start_j, end_j = row_b['Start Time'], row_b['End Time']
						if (start_i <= end_j) and (end_i >= start_j):
							data = [
								row_a['Person ID'],
								row_b['Person ID'],
								max(start_i, start_j),
								min(end_i,end_j),
								row_a['Geohash'],
								row_a['End Index'] - row_a['Start Index'] + 1,
								row_b['End Index'] - row_b['Start Index'] + 1,
								row_a['Start Index'],
								row_a['End Index'],
								row_b['Start Index'],
								row_b['End Index']
							]
							meets.append(data)

							if len(meets)>5000:
								ds = pd.DataFrame(meets,columns=cx)
								ds.to_csv(out_dir+"pairs_"+str(file_i)+".csv",index=False)
								file_i+=1
								meets = []

	if len(meets) > 0:
		ds = pd.DataFrame(meets, columns=cx)
		ds.to_csv(out_dir + "pairs_" + str(file_i) + ".csv", index=False)
		file_i += 1

	dfs = []
	for i in range(file_i):
		dfs.append(pd.read_csv(out_dir +"pairs_"+str(i)+".csv"))
	dr = pd.concat(dfs, ignore_index=True)
	dr.to_csv(out_file,index=False)

def create_edges(in_file, out_file):
	df = pd.read_csv(in_file)
	df['start_time'] = pd.to_datetime(df['start_time'])
	df['end_time'] = pd.to_datetime(df['end_time'])
	df['duration'] = df['end_time'] - df['start_time']
	aggregated = df.groupby(['person_a','person_b'])['duration'].agg(['sum', 'count','max','min','mean']).reset_index()

	aggregated.columns = ['person_a','person_b','sum', 'count','max','min','mean']

	aggregated.to_csv(out_file, index=False)

def transform_times(in_file, out_folder, out_file):
	df = pd.read_csv(in_file)
	file_i = 0
	cx = []
	meets = []
	cols = json.loads(df.loc[0]['meets_intervals_keys'])
	for index in tqdm(df.index):
		row = df.loc[index]
		intervals = json.loads(row['meets_intervals'])
		intervals_keys = list(intervals.keys())
		for key1 in range(len(intervals_keys)):
			meets.extend(intervals[intervals_keys[key1]])
			if len(meets)>500000:
				ds = pd.DataFrame(meets,columns=cols)
				ds.to_csv(out_folder+"intervals_"+str(file_i)+".csv",index=False)
				file_i+=1
				meets = []

	if len(meets) > 0:
		ds = pd.DataFrame(meets, columns=cols)
		ds.to_csv(out_folder+"intervals_"+str(file_i)+".csv",index=False)
		file_i += 1

	dfs = []
	for i in range(file_i):
		dfs.append(pd.read_csv(out_folder+"intervals_"+str(i)+".csv"))
	dr = pd.concat(dfs, ignore_index=True)
	dr['Start Time'] = pd.to_datetime(dr['Start Time'])
	dr['End Time'] = pd.to_datetime(dr['End Time'])
	dr['interval'] = dr['End Time'] - dr['Start Time']
	dr['date_change'] = dr['Start Time'].dt.date != dr['End Time'].dt.date
	dr.to_csv(out_file,index=False)

def split_to_single_day(in_file, out_file):
	ds = pd.read_csv(in_file)
	df = ds[ds['date_change'] == True].copy(deep=True)

	df['Start Time'] = pd.to_datetime(df['Start Time'])
	df['End Time'] = pd.to_datetime(df['End Time'])

	new_rows = []

	for index, row in tqdm(df.iterrows()):

		start = row['Start Time']
		end = row['End Time']

		if start.date() == end.date():
			new_rows.append(row)
		else:
			end_first_day = start.replace(hour=23, minute=59, second=59)
			row['End Time'] = end_first_day
			new_rows.append(row.copy())

			current = start + pd.Timedelta(days=1)
			current = current.replace(hour=0, minute=0, second=0)
			while current.date() < end.date():
				new_row = row.copy()
				new_row['Start Time'] = current
				new_row['End Time'] = current.replace(hour=23, minute=59, second=59)
				new_rows.append(new_row)
				current += pd.Timedelta(days=1)

			start_last_day = end.replace(hour=0, minute=0, second=0)
			new_row = row.copy()
			new_row['Start Time'] = start_last_day
			new_row['End Time'] = end
			new_rows.append(new_row)

	new_df = pd.DataFrame(new_rows)
	new_df['date_change'] = False

	onedays = ds[ds['date_change'] == False].copy(deep=True)
	to_concat = []
	if len(onedays) > 0 :
		to_concat.append(onedays)
	if len(new_df)>0:
		to_concat.append(new_df)

	new_df = pd.concat(to_concat)

	new_df['Start Time'] = pd.to_datetime(new_df['Start Time'])
	new_df['End Time'] = pd.to_datetime(new_df['End Time'])
	new_df['interval'] = new_df['End Time'] - new_df['Start Time']

	new_df.sort_values(by=['Geohash', 'Person ID', 'Start Time'], ascending=[True, True, True])

	new_df.reset_index(drop=True, inplace=True)
	new_df.to_csv(out_file, index=False)
