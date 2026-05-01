import numpy as np
import pandas as pd


def data_series(l, n):
    result = pd.Series(l)
    # if len(l) > n :
    #     result = result.head(n)

    result[n] = 100

    return result



# function call
l = list(map(int, input("Enter the list of numbers separated by space: ").split(',')))
n = int(input("Enter the number of elements to display: "))
print(data_series(l, n))