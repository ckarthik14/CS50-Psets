#!usr/bin/env python3
from cs50 import get_float


# gets the minimum count of change
def getChange(n):
    count = 0

    if n >= 25:
        count += n // 25
        n %= 25

    if n >= 10:
        count += n // 10
        n %= 10

    if n >= 5:
        count += n // 5
        n %= 5

    if n >= 1:
        count += n

    return count


print("O hai! How much change is owed?")

# gets the amount to be given back
number = get_float()
number *= 100

print(number)

number = int(number)

# prints minimum coins to return
print(getChange(number))