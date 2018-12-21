import numpy as np

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


a = np.array([[1.453198542, 10.00297355791645934]])

RoundAfterDigitsCound = 5
NumbersWithoutZero = list(range(1, 10))
NumbersWithoutZero = [str(x) for x in NumbersWithoutZero]

for (x, y), UnroundedValue in np.ndenumerate(a):

    GetDecimalPointPosition = str(UnroundedValue).find('.')
    for index, i in enumerate(str(UnroundedValue)):
        if i in NumbersWithoutZero:
            FirstOccurenceNaturalNumber = index
            if index > GetDecimalPointPosition:
                FirstOccurenceNaturalNumber -= 1
            break

    TruncateIndex = FirstOccurenceNaturalNumber + RoundAfterDigitsCound - GetDecimalPointPosition

    RoundedValue = truncate(UnroundedValue, decimals=TruncateIndex)

    a[x,y] = RoundedValue

print(a)

