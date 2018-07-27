from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    same_lines = []

    # creating a list with all the lines in file1
    linesA = a.split("\n")
    linesA = [i.rstrip("\r") for i in linesA]

    # creating a list with all the lines in file2
    linesB = b.split("\n")
    linesB = [i.rstrip("\r") for i in linesB]

    for line in linesA:
        if line in linesB and line not in same_lines:
            same_lines.append(line)

    return same_lines


def sentences(a, b):
    """Return sentences in both a and b"""

    # creating a list with all the sentences using nltk
    sentencesA = sent_tokenize(a)
    sentencesB = sent_tokenize(b)

    same_sentences = []

    for sent in sentencesA:
        if sent in sentencesB and sent not in same_sentences:
            same_sentences.append(sent)

    return same_sentences


# generates substrings of length n
def generator(string, n):
    ret_list = []

    i = 0
    j = n

    for i in range(len(string) - n + 1):
        if string[i:j] not in ret_list:
            ret_list.append(string[i:j])
        j += 1

    return ret_list


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    same_substrings = []

    # adds substrings of length n without duplicates
    substringsA = generator(a, n)
    substringsB = generator(b, n)

    for substr in substringsA:
        if substr in substringsB and substr not in same_substrings:
            same_substrings.append(substr)

    return same_substrings
