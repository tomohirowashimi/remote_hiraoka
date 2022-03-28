# // 20220212 Ver.hiraoka　→　0301 rest 追加　→　0306 調整/確認

import pandas as pd
import datetime

#file = '/var/tmp/indata_all.pkl'
file = 'indata_all.pkl'
now = datetime.datetime.now()

cols = ["lr", "in_time", "rest"]
df = pd.DataFrame(columns=cols)
df = df.append({"lr": "-", "in_time": now, "rest": 0}, ignore_index=True)
print(df)

df.to_pickle(file)
