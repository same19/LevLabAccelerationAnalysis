import serial
import time
from serialPorts import serial_ports
import numpy as np
import matplotlib.pyplot as plt
import math
from functionTools import *

circuit_gain = 250

def connect():
    ports = serial_ports()
    # print(ports)
    print("Connecting to "+ports[-1]+"...")
    baud = 4000000
    arduino = serial.Serial(ports[-1], baud)
    print("Connected to "+ports[-1]+" at baud rate " + str(baud) + ".")
    return arduino
def log(arduino, totalTime): #in seconds
    print("Log loading...")
    arduino.write(bytes(int(totalTime)))
    data = []
    start = time.time_ns()
    for i in range(int(totalTime)):
        tdata = arduino.readline().decode().strip("\n").strip("\r").split(" ")
        if i == 0:
            print("Logging...")
        for j in range(len(tdata)):
            tdata[j] = float(tdata[j])/1024.0 * 5.0
        tdata = [i] + tdata
        data.append(tdata)
    print("Log complete.")
    return data, time.time_ns()-start
def main():
    arduino = connect()

    num = 20000
    data, t = np.array(log(arduino, num))
    scale = num * 10**9 / t
    print("Measurement Rate: "+str(scale))

    row0 = [row[0] for row in data]
    row1 = [row[1] for row in data]
    timeX = np.multiply(row0,1/scale)
    plot(timeX, row1,"Time (s)", "Voltage (V)")

    f = np.fft.rfft(row1)
    fabs = np.abs(f)
    freqs = np.multiply(np.fft.fftfreq(f.shape[-1]), scale/2.0)

    minI = 1
    maxI = 2000
    x = freqs[minI:maxI]
    y = fabs[minI:maxI]
    plot(x,y,"Frequency (Hz)","Amplitude  - Acceleration")

    minI = 15
    maxI = 700
    fDoubleInt = [f[i]/(4 * (math.pi ** 2) * (freqs[i]**2)) if freqs[i] != 0 else 0 for i in range(len(f))]
    absDoubleInt = np.abs(fDoubleInt)
    freqs = np.multiply(np.fft.fftfreq(absDoubleInt.shape[-1]), scale/2.0)
    x = freqs[minI:maxI]
    y = absDoubleInt[minI:maxI]
    plot(x,y,"Frequency (Hz)","Amplitude - Displacement")

    singleInt = []
    lastValue = 0
    bias = 0 # -29.702 * scale / len(row1)
    adjustedAcc = np.add(np.multiply(row1, 0.500 * 9.81 / circuit_gain),bias) #2 V * gain = 1 g, 9.81 m/s^2 = 1g
    for i in adjustedAcc:
        lastValue += i/scale
        singleInt.append(lastValue)
    afterBias = -1 * lastValue / len(row1)
    singleInt = [singleInt[i] + afterBias*i for i in range(len(singleInt))]
    plot(timeX, singleInt, "Time (s)", "Velocity (m/s) - Single Integral")
    doubleInt = []
    lastValue = 0
    bias2 = 0
    adjustedSingleInt = np.add(singleInt,bias2)
    for i in adjustedSingleInt:
        lastValue += i/scale
        doubleInt.append(lastValue)
    afterBias = -1 * lastValue / len(row1)
    doubleInt = [doubleInt[i] + afterBias*i for i in range(len(doubleInt))]
    plot(timeX, np.multiply(doubleInt,10**9), "Time (s)", "Displacement (nm) - Double Integral")

    arduino.close()

if __name__ == "__main__":
    main()



