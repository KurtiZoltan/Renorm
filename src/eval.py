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

def eval(path):
    data = np.loadtxt(path)

    popt, _ = curve_fit(expplusc, np.arange(len(data)), data)

    x = np.arange(len(data))
    y = expplusc(x, *popt)
    # plt.plot(data)
    # plt.plot(x, y)
    # plt.show()
    
    data = data[int(10/popt[1]):]
    # plt.plot(data)
    # plt.show()

    m = mu(data)
    print(f"mu={mu(data)}")
    slist = []
    while True:
        data, s = block(data)
        if s != s:
            break
        slist.append(s)
    
    s = float("NaN")
    for s1, s2 in zip(slist[:-1], slist[1:]):
        s = s1
        if s2 < s1:
            break
    print(f"          sigma: {s} {(np.abs(0.911319 - m)) / s}")
    return m, s

for i in range(16):
    path = f"./build/L={(i+1)*64}_beta=0.5.txt"
    print(path)
    m, s = eval(path)
    plt.errorbar((i+1)*64, m, s, fmt="rx")

for i in range(16):
    path = f"./build/L={(i+1)*8}_beta=0.5.txt"
    print(path)
    m, s = eval(path)
    plt.errorbar((i+1)*8, m, s, fmt="rx")
m, s = eval("./build/L=1024_beta=0.5.txt")

plt.hlines([m+2*s, m-2*s], 0, 1024, colors="blue")
plt.hlines(0.911319, 0, 1024, colors="black")
plt.grid()
plt.xscale("log")
plt.xlabel("L")
plt.ylabel("m")
plt.savefig("./figs/L.pdf")
plt.show()

