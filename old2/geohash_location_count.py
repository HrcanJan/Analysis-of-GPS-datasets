import pandas as pd

def geohash_location_count():
    df = pd.read_csv('data/geolife_geohash_size_8_no_duplicates.csv')

    df.groupby('Geohash').size().sort_values(ascending=False)
    grouped_df = df.groupby('Geohash').size().reset_index(name='Count')

    # Sorting by 'Count' column if needed
    grouped_df = grouped_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
    grouped_df.to_csv('data/geolife_geohash_8_location_counts.csv',index=False)
