import pandas as pd
import numpy as np


df1 = pd.DataFrame({'a': ['foo', 'bar'], 'b': [1, 2]})
print(df1)
print("______________________________________")
df2 = pd.DataFrame({'a': ['foo', 'bar'], 'b': [3, 4]})

df_result = df1.merge(df2)
print(df_result)
