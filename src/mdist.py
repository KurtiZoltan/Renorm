import numpy as np
import matplotlib.pyplot as plt

m431 = np.loadtxt("431.out")
m434 = np.loadtxt("434.out")
m437 = np.loadtxt("437.out")
m441 = np.loadtxt("441.out")

N = 50

n, bins, patches = plt.hist(m431, bins=N)
x431 = (bins[1:] + bins[:-1]) / 2
y431 = n / 1024**2 / (x431[-1] - x431[0]) * N
n, bins, patches = plt.hist(m434, bins=N)
x434 = (bins[1:] + bins[:-1]) / 2
y434 = n / 1024**2 / (x434[-1] - x434[0]) * N
n, bins, patches = plt.hist(m437, bins=N)
x437 = (bins[1:] + bins[:-1]) / 2
y437 = n / 1024**2 / (x437[-1] - x437[0]) * N
n, bins, patches = plt.hist(m441, bins=N)
x441 = (bins[1:] + bins[:-1]) / 2
y441 = n / 1024**2 / (x441[-1] - x441[0]) * N
plt.show()

plt.plot(x431, y431, label=f"$\\beta=0.431$")
plt.plot(x434, y434, label=f"$\\beta=0.434$")
plt.plot(x437, y437, label=f"$\\beta=0.437$")
plt.plot(x441, y441, label=f"$\\beta=0.441$")
plt.legend()
plt.xlabel("m")
plt.ylabel("p")
plt.savefig("./figs/mdistribution.pdf")
plt.show()
