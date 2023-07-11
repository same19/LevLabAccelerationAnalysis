import matplotlib.pyplot as plt
import numpy as np

def plot(x,y,labelX="x",labelY="y"):
    plt.figure(figsize=(10,5))
    plt.plot(x, y)
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.show()