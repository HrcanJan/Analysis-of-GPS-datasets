import json

import pandas as pd

def geohash_user_count(in_file, out_file):
    df = pd.read_csv(in_file)

    data = []
    for key, value in df.groupby('Geohash'):
        users = value['Person ID'].unique().tolist()
        data.append([key,len(users),json.dumps(users)])

    df = pd.DataFrame(data, columns=['Geohash', 'user_count', 'users'])


    df = df.sort_values(by='user_count', ascending=False).reset_index(drop=True)
    df.to_csv(out_file,index=False)
