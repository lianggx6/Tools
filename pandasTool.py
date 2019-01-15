# import numpy as np
import pandas as pd

df = pd.read_json("time.json")
df = df.sort_index()
print(df)
