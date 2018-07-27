#!usr/bin/env python3
import sys
from cs50 import get_int


height = int()
while True:
    # prompts user for height in desired range
    height = get_int("Height: ")

    if height >= 0 and height <= 23:
        break


# prints pyramid
for i in range(height):
    for j in range(height - i - 1):
        print(" ", end="")

    for j in range(i + 2):
        print("#", end="")

#    print("  ", end="")

#    for j in range(i + 1):
#        print("#", end="")

    print()