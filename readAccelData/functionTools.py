import matplotlib.pyplot as plt
import numpy as np

def plot(x,y,labelX="x",labelY="y"):
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.plot(x, y)
    ax.set_xlabel(labelX)
    ax.set_ylabel(labelY)
    plt.show()