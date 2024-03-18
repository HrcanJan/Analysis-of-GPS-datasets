import  pandas as pd
from tqdm import tqdm
import json

def create_geohash_time_meets():
    df = pd.read_csv('data/geolife_geohash_meet_size_8.csv')
    df['meets_intervals'] = ""

    for index in tqdm(df.index):
        meets = json.loads(df.loc[index, 'meets'])
        cols = json.loads(df.loc[index, 'meets_keys'])
        all_intervals = {}
        for i in meets.keys():
            times = meets[i]
            interval = []
            first_time = [vi for vi in times[0]]
            prev_time = [vi for vi in times[0]]
            for time in times:
                if time[cols.index('Index')] - prev_time[cols.index('Index')] > 1:
                    interval.append([
                        prev_time[cols.index('Person ID')],
                        first_time[cols.index('Timestamp')],
                        prev_time[cols.index('Timestamp')],
                        prev_time[cols.index('Geohash')],
                        first_time[cols.index('Index')],
                        prev_time[cols.index('Index')],
                        ])
                    first_time = [vi for vi in time]
                prev_time = [vi for vi in time]

            interval.append([
                prev_time[cols.index('Person ID')],
                first_time[cols.index('Timestamp')],
                prev_time[cols.index('Timestamp')],
                prev_time[cols.index('Geohash')],
                first_time[cols.index('Index')],
                prev_time[cols.index('Index')],
            ])
            all_intervals[i]=interval
        df.loc[index, 'meets_intervals'] = json.dumps(all_intervals)
        df.loc[index, 'meets_intervals_keys'] = json.dumps(["Person ID", "Start Time", "End Time", "Geohash", "Start Index", "End Index"])
    df.to_csv('data/geolife_geohash_meet_intervals_size_8.csv',index=False)


def display_meet_intervals():
    df = pd.read_csv('data/test.csv')
    for index in tqdm(df.index):
        meets = json.loads(df.loc[index, 'meets'])
        cols = json.loads(df.loc[index, 'meets_keys'])
        for i in meets.keys():
            print(pd.DataFrame(meets[i],columns=cols))
        meets = json.loads(df.loc[index, 'meets_intervals'])
        cols = json.loads(df.loc[index, 'meets_intervals_keys'])
        for i in meets.keys():
            print(pd.DataFrame(meets[i],columns=cols))