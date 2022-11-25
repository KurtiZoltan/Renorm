import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Ls = [32, 48, 64, 80, 96, 112, 128, 144, 160]
betac = 0.5 * np.log(np.sqrt(2) + 1)

def quad(x, a, b, c):
    return c * (x - b)**2 + a

data = np.loadtxt("points1.txt")

new = np.loadtxt("points2.txt")
data = np.append(data, new, axis=0)

new = np.loadtxt("points3.txt")
data = np.append(data, new, axis=0)

new = np.loadtxt("points4.txt")
data = np.append(data, new, axis=0)


chimaxlist = []
betamaxlist = []

for L in Ls:
    mask = np.abs(data[:, 0] - L) < 0.1
    betas = data[mask, 1]
    chis = data[mask, 2]
    plt.plot(betas, chis, ".", markersize=3)
    
    chimax = np.max(chis)
    betamax = betas[np.argmax(chis)]
    beta1 = np.min(betas[chis > chimax / 2])
    beta2 = np.max(betas[chis > chimax / 2])
    mask = np.logical_and(beta1 < betas, betas < beta2)
    fwhm = beta2 - beta1
    plt.plot(betas[mask], chis[mask], ".", markersize=3)
    
    p = [chimax, betamax, -chimax / fwhm**2]
    popt, pcov = curve_fit(quad, betas[mask], chis[mask], p)
    chimaxlist.append(popt[0])
    betamaxlist.append(popt[1])
    
    x = np.linspace(beta1, beta2, 100)
    plt.plot(x, quad(x, *popt))

    plt.show()


def betafit(L, A, nu):
    return betac - A * np.power(L, -1/nu)
    
plt.plot(Ls, betamaxlist, ".")
popt, pcov = curve_fit(betafit, Ls, betamaxlist)
nu = popt[1]
print(f"betac={popt[2]}")
x = np.linspace(32, 160, 300)
plt.plot(x, betafit(x, *popt))
print(f"nu={nu:.2f}")
plt.show()

def chifit(L, B, gamma):
    return B * np.power(L, gamma / nu)

plt.plot(Ls, chimaxlist, ".")
popt, pcov = curve_fit(chifit, Ls, chimaxlist)
gamma = popt[1]
plt.plot(x, chifit(x, *popt))
print(f"gamma={gamma:.2f}")
plt.show()
