from matplotlib import pyplot as plt
import numpy as np

def plot(x,y,labelX="x",labelY="y"):
    plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    plt.plot(x, y)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.show()