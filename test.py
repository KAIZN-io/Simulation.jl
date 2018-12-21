import numpy as np

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

a = np.array([[10234.45, 213223.23], [3234.00, 0.020349], [5324.2222, 21.322223]])

RoundAfterDigitsCound = 5
for (x, y), UnroundedValue in np.ndenumerate(a):

    GetDecimalPointPosition = str(UnroundedValue).find('.')
    TruncateIndex = RoundAfterDigitsCound - GetDecimalPointPosition
    RoundedValue = truncate(UnroundedValue, decimals=TruncateIndex)

    a[x,y] = RoundedValue

