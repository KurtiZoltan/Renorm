import numpy as np
import matplotlib.pyplot as plt

path1 = "./build/L=1024_beta=0.5.txt"
path2 = "./build/L=1024_beta=0.45.txt"

data1 = np.loadtxt(path1)
data2 = np.loadtxt(path2)

plt.plot(data1, label="$\\beta=0.5$")
plt.plot(data2, label="$\\beta=0.45$")
plt.xlabel("Step number")
plt.ylabel("$m$")
plt.grid()
plt.legend()
plt.savefig("./figs/extra1.pdf")
plt.show()

path3 = "./build/L=8_beta=0.5.txt"
data3 = np.loadtxt(path3)

plt.plot(data3, label="$\\beta=0.5$ $L=8$")
plt.xlabel("Step number")
plt.ylabel("$m$")
plt.grid()
plt.legend()
plt.savefig("./figs/extra2.pdf")
plt.show()
