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

    fig, ax = plt.subplots(1, 2)
    x = np.arange(len(data))
    y = expplusc(x, *popt)
    ax[0].plot(data[:1024], ".", markersize=2)
    ax[0].plot(x[:1024], y[:1024])
    ax[0].set_ylabel("m")
    ax[0].set_xlabel("Step number")
    ax[0].grid()
    
    print(popt[1])
    print(int(10/popt[1]))
    data = data[int(10/popt[1]):]
    x = x[int(10/popt[1]):]
    ax[1].plot(x[:1024], data[:1024], ".", markersize=2)
    ax[1].set_ylabel("m")
    ax[1].set_xlabel("Step number")
    ax[1].grid()
    plt.savefig("./figs/steps45.pdf")
    plt.show()

    m = mu(data)
    print(f"mu={mu(data)}")
    slist = []
    blocksize = []
    for i in range(10):
        data, s = block(data)
        slist.append(s)
        blocksize.append(2**i)

    s = np.nanmax(np.array(slist))
    print(f"          sigma: {s} {(np.abs(0.911319 - m)) / s}")
    return m, s

path = "./build/L=1024_beta=0.45.txt"
m, s = eval(path)

def eval(path):
    data = np.loadtxt(path)

    popt, _ = curve_fit(expplusc, np.arange(len(data)), data)

    data = data[int(10/popt[1]):]

    m = mu(data)
    print(f"mu={mu(data)}")
    slist = []
    blocksize = []
    i=0
    while True:
        data, s = block(data)
        if s != s:
            break
        slist.append(s)
        blocksize.append(2**i)
        i += 1
    
    #plt.figure(figsize=(8, 6))
    plt.plot(blocksize, slist, "o")
    plt.xscale("log")
    plt.grid()
    plt.xlabel("Block size")
    plt.ylabel("$\\sigma_m$")
    plt.savefig("./figs/sigma45.pdf")
    plt.show()

    s = np.nanmax(np.array(slist))
    print(f"          sigma: {s} {(np.abs(0.911319 - m)) / s}")
    return m, s

m, s = eval(path)
print(m, s)