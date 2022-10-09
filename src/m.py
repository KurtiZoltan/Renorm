import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def mu(data):
    return np.sum(data) / len(data)

def sigma2(data):
    return mu(data**2) - mu(data)**2

def expplusc(x, a, b, c):
    return a*np.exp(-b*x)+c

def block(data):
    plt.plot(data, ".", markersize=3)
    plt.grid()
    plt.show()
    s = sigma2(data)
    s = np.sqrt(s / (len(data) - 1))
    return (data[:len(data)//2*2:2] + data[1::2])/2, s

def eval(path):
    data = np.loadtxt(path)

    popt, _ = curve_fit(expplusc, np.arange(len(data)), data)

    x = np.arange(len(data))
    y = expplusc(x, *popt)
    plt.plot(data, ".", markersize=2)
    plt.plot(x, y)
    plt.grid()
    plt.show()

    data = data[int(10/popt[1]):]
    plt.plot(data, ".", markersize=2)
    plt.grid()
    plt.show()

    m = mu(data)
    print(f"mu={mu(data)}")
    slist = []
    while True:
        data, s = block(data)
        if s != s:
            break
        slist.append(s)

    s = np.nanmax(np.array(slist))
    return m, s

path = "./build/L=896_beta=0.45.txt"
m, s = eval(path)
print(f"m={m} +/- {s}")

#print(np.abs(0.911319 - m) / s)
