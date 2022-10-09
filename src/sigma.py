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
    s = sigma2(data)
    s = np.sqrt(s / (len(data) - 1))
    return (data[:len(data)//2*2:2] + data[1::2])/2, s

def eval(path,nfrac):
    data = np.loadtxt(path)

    popt, _ = curve_fit(expplusc, np.arange(len(data)), data)

    x = np.arange(len(data))
    y = expplusc(x, *popt)

    data = data[int(10/popt[1]):]
    N = int(nfrac * data.shape[0])
    data = data[:N]

    m = mu(data)
    print(f"mu={mu(data)}")
    slist = []
    while True:
        data, s = block(data)
        if s != s:
            break
        slist.append(s)

    s = np.nanmax(np.array(slist))
    return m, s, N

path = "./build/L=256_beta=0.45.txt"
data = np.loadtxt(path)
plt.plot(data)
plt.grid()
plt.show()
N = 100
for i in range(N):
    i += 1
    x = i / N
    m, s, x = eval(path, x)
    plt.plot(x, 1/s**2, ".")
    print(f"m={m} +/- {s}")

plt.grid()
plt.plot(0, 0, ".")
plt.show()
