# File to plot the results of the two algorithms

import matplotlib.pyplot as plt

problemSize = [
    16,
    64,
    128,
    256,
    384,
    512,
    768,
    1024,
    1280,
    1536,
    2048,
    2560,
    3072,
    3584,
    3968,
]


def plot_time(cputime, cputime_eff, prbmsize):
    """
    Plot the time taken to run the algorithms
    """
    plt.plot(prbmsize, cputime, label="Basic")
    plt.plot(prbmsize, cputime_eff, label="Efficient")

    plt.xlabel("Problem Size")
    plt.ylabel("CPU Time (ms)")
    plt.title("Problem Size vs CPU Time plot")
    plt.legend()
    plt.savefig("../img/time.png")
    plt.clf()


def plot_memory(memoryuse, memoryuse_eff, prbmsize):
    """
    Plot the memory used by the algorithms
    """
    plt.plot(prbmsize, memoryuse, label="Basic")
    plt.plot(prbmsize, memoryuse_eff, label="Efficient")

    plt.xlabel("Problem Size")
    plt.ylabel("Memory Usage (KB)")
    plt.title("Problem Size vs Memory Usage plot")
    plt.legend()
    plt.savefig("../img/memory.png")
    plt.clf()


def readFiles(filenames):
    """
    Read the data from the output file
    Format:
    Cost of the alignment (Integer) - Ignore
    First string alignment (String) - Ignore
    Second string alignment (String) - Ignore
    Time in Milliseconds (Float) - Read
    Memory in Kilobytes (Float) - Read
    """
    time = []
    mem = []

    for file in filenames:
        with open(file, "r") as f:
            lines = f.readlines()
            mem.append(float(lines[-1]))
            time.append(float(lines[-2]))

    return mem, time


if __name__ == "__main__":
    base = "../dataPoints/"
    fileNames1 = [base + "out" + str(i) + ".txt" for i in range(1, 16)]
    fileNames2 = [base + "out_eff" + str(i) + ".txt" for i in range(1, 16)]

    memBasic, timeBasic = readFiles(fileNames1)
    memEff, timeEff = readFiles(fileNames2)

    plot_time(timeBasic, timeEff, problemSize)
    plot_memory(memBasic, memEff, problemSize)
