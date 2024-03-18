import  pandas as pd
from tqdm import tqdm
import json

def create_geohash_intervals(in_path, out_path):
    df = pd.read_csv(in_path)
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
                if (time[cols.index('Index')] - prev_time[cols.index('Index')] > 1
                        or time[cols.index('Trajectory')] != prev_time[cols.index('Trajectory')]
                        or time[cols.index('Person ID')] != prev_time[cols.index('Person ID')]
                        or pd.to_datetime(time[cols.index('Timestamp')]) < pd.to_datetime(prev_time[cols.index('Timestamp')])
                ):
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
    df.to_csv(out_path,index=False)


def display_meet_intervals(in_file):
    df = pd.read_csv(in_file)
    for index in tqdm(df.index):
        print("============================")
        print()
        meets = json.loads(df.loc[index, 'meets'])
        cols = json.loads(df.loc[index, 'meets_keys'])
        for i in meets.keys():
            print(pd.DataFrame(meets[i],columns=cols))
            print()
        print("----------------------")
        meets = json.loads(df.loc[index, 'meets_intervals'])
        cols = json.loads(df.loc[index, 'meets_intervals_keys'])
        for i in meets.keys():
            print(pd.DataFrame(meets[i],columns=cols))
            print()


def display_meet_times(in_file):
    df = pd.read_csv(in_file)
    for index in tqdm(df.index):
        print("============================")
        print()
        meets = json.loads(df.loc[index, 'meets'])
        cols = json.loads(df.loc[index, 'meets_keys'])
        for i in meets.keys():
            print(pd.DataFrame(meets[i],columns=cols))
            print()

