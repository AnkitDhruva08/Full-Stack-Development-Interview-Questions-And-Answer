import pandas as pd

lst = list(map(int,input("Enter list of values :::: ").split(',')))

pd_series = pd.Series(lst, dtype=float)
print('pd_series ==<<<>>', pd_series)