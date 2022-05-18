import sys
import time
from resource import *
import psutil

mismatch = {
    "A": {"A": 0, "C": 110, "G": 48, "T": 94},
    "C": {"A": 110, "C": 0, "G": 118, "T": 48},
    "G": {"A": 48, "C": 118, "G": 0, "T": 110},
    "T": {"A": 94, "C": 48, "G": 110, "T": 0},
}


def readInput(file):
    """
    Reads input from file.
    """
    with open(file, "r") as f:
        lines = f.readlines()
        base1 = lines[0].strip()

        indices1 = []
        for i, line in enumerate(lines[1:]):
            try:
                indices1.append(int(line.strip()))
            except ValueError:
                base2 = line.strip()
                saveIndex = i
                break

        indices2 = []
        for i in range(saveIndex + 2, len(lines)):
            indices2.append(int(lines[i].strip()))

    return base1, indices1, base2, indices2


def createSequence(base, indices, current):
    """
    Creates input using base and insert indices.
    Pass current as 0 initially.
    """
    result = ""
    for i in range(0, indices[current] + 1):
        result += base[i]
    result += base
    for i in range(indices[current] + 1, len(base)):
        result += base[i]

    if len(indices) - 1 == current:
        return result
    else:
        return createSequence(result, indices, current + 1)


def writeOutput(file, cost, s1, s2, time, memory):
    """
    Writes output to file.
    """
    if len(file) == 0:
        file = "output.txt"

    with open(file, "w") as f:
        f.write(str(cost) + "\n")
        f.write(s1 + "\n")
        f.write(s2 + "\n")
        f.write(str(time) + "\n")
        f.write(str(memory) + "\n")


def procMemory():
    """
    Returns memory usage in MB.
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def sequenceAlignment(s1, s2, gap):
    # Initialize the matrix
    m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]

    # Fill the first row and column
    for i in range(1, len(s1) + 1):
        m[i][0] = m[i - 1][0] + gap
    for j in range(1, len(s2) + 1):
        m[0][j] = m[0][j - 1] + gap

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                m[i][j] = m[i - 1][j - 1]
            else:
                m[i][j] = min(
                    m[i - 1][j - 1] + mismatch[s1[i - 1]][s2[j - 1]],
                    m[i - 1][j] + gap,
                    m[i][j - 1] + gap,
                )

    return m


def align(s1, s2, gap):
    cols = [[0] * 2 for _ in range(len(s1) + 1)]

    for i in range(len(s1) + 1):
        cols[i][0] = i * gap

    cols[0][1] = gap

    j = 0

    while j < len(s2):
        for i in range(1, len(s1) + 1):
            cols[i][1] = min(
                cols[i - 1][1] + gap,
                cols[i][0] + gap,
                cols[i - 1][0] + mismatch[s1[i - 1]][s2[j]],
            )

        j += 1

        for _ in range(len(cols)):
            cols[_][0] = cols[_][1]

        for _ in range(len(cols)):
            cols[_][1] = 0

        cols[0][1] = (j + 1) * gap

    return cols


def backtrack(s1, s2, m, gap, cost):

    i = len(s1)
    j = len(s2)
    alignment1 = ""
    alignment2 = ""
    while i > 0 and j > 0:
        if m[i][j] == m[i - 1][j - 1] + mismatch[s1[i - 1]][s2[j - 1]]:
            alignment1 = s1[i - 1] + alignment1
            alignment2 = s2[j - 1] + alignment2
            i -= 1
            j -= 1
        elif m[i][j] == m[i][j - 1] + gap:
            alignment1 = "_" + alignment1
            alignment2 = s2[j - 1] + alignment2
            j -= 1
        elif m[i][j] == m[i - 1][j] + gap:
            alignment1 = s1[i - 1] + alignment1
            alignment2 = "_" + alignment2
            i -= 1

    while i > 0:
        alignment1 = s1[i - 1] + alignment1
        alignment2 = "_" + alignment2
        i -= 1
    while j > 0:
        alignment1 = "_" + alignment1
        alignment2 = s2[j - 1] + alignment2
        j -= 1

    return alignment1, alignment2, cost


def divideConquer(s1, s2, gap, minSum):
    m = len(s1)
    n = len(s2)

    if m <= 2 or n <= 2:
        matrix = sequenceAlignment(s1, s2, gap)
        return backtrack(s1, s2, matrix, gap, minSum)

    minIndex = float("inf")
    minSum = float("inf")

    c1 = align(s1, s2[: n // 2], gap)
    c2 = align(s1[::-1], s2[n // 2 :][::-1], gap)

    # Reverse the string
    c2 = c2[::-1]

    for idx in range(len(c2)):
        s = c1[idx][0] + c2[idx][0]
        if s < minSum:
            minSum = s
            minIndex = idx

    l1, l2, i1 = divideConquer(s1[:minIndex], s2[: n // 2], gap, minSum)
    r1, r2, i2 = divideConquer(s1[minIndex:], s2[n // 2 :], gap, minSum)

    return l1 + r1, l2 + r2, minSum


if __name__ == "__main__":
    base1, indices1, base2, indices2 = readInput(sys.argv[1])
    s1 = createSequence(base1, indices1, 0)
    s2 = createSequence(base2, indices2, 0)

    startTime = time.time()
    a, b, cost = divideConquer(s1, s2, 30, 0)
    endTime = time.time()
    timeTaken = (endTime - startTime) * 1000

    memory = procMemory()

    writeOutput(sys.argv[2], cost, a, b, timeTaken, memory)
