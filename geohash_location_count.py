import pandas as pd

def geohash_location_count(in_file, out_file):
	df = pd.read_csv(in_file)

	df.groupby('Geohash').size().sort_values(ascending=False)
	grouped_df = df.groupby('Geohash').size().reset_index(name='Count')

	grouped_df = grouped_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
	grouped_df.to_csv(out_file,index=False)
