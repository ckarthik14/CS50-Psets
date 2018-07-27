#!usr/bin/env python3
import sys
import string
from cs50 import get_string


# function for caesar encryption
def encrypt(string, key):
    cipher = ""
    for char in string:
        if char.isupper():
            cipher += chr((ord(char) - 65 + key) % 26 + 65)

        elif char.islower():
            cipher += chr((ord(char) - 97 + key) % 26 + 97)

        else:
            cipher += char

    return cipher


def main():
    # checks for valid key
    if len(sys.argv) != 2:
        print("Usage: {} k".format(sys.argv[0]))
        sys.exit(1)

    key = int(sys.argv[1])

    # prompts user for text
    print("plaintext:  ", end="")

    text = get_string()

    # converts text to cipher
    cipher = encrypt(text, key)

    # display cipher
    print("ciphertext: {}".format(cipher))


if __name__ == "__main__":
    main()