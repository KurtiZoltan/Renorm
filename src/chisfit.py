import numpy as np
import matplotlib.pyplot as plt
cm = 1 / 2.54
plt.rcParams['figure.constrained_layout.use'] = True
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

new = np.loadtxt("points5.txt")
data = np.append(data, new, axis=0)

data5 = np.loadtxt("points5.txt")


chimaxlist = []
betamaxlist = []

fig, axs = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(16*cm, 16*cm))

for i in range(3):
    for j in range(3):
        L = Ls[i*3+j]
        mask = (np.abs(data[:, 0] - L) < 0.1) * (0.41 < data[:, 1]) * (data[:, 1] < 0.447)
        mask5 = (np.abs(data5[:, 0] - L) < 0.1) * (0.41 < data5[:, 1]) * (data5[:, 1] < 0.447)
        betas = data[mask, 1]
        chis = data[mask, 2]
        
        betas5 = data5[mask5, 1]
        chis5 = data5[mask5, 2]
        
        chimax = np.max(chis)
        betamax = betas[np.argmax(chis)]
        beta1 = np.min(betas[chis > chimax / 2])
        beta2 = np.max(betas[chis > chimax / 2])
        mask = np.logical_and(beta1 < betas, betas < beta2)
        fwhm = beta2 - beta1
        
        p = [chimax, betamax, -chimax / fwhm**2]
        popt, pcov = curve_fit(quad, betas[mask], chis[mask], p)
        chimaxlist.append(popt[0])
        betamaxlist.append(popt[1])
        
        axs[i][j].plot(betas, chis, ".", markersize=2)
        axs[i][j].plot(betas[mask], chis[mask], ".", markersize=2)
        x = np.linspace(beta1, beta2, 100)
        axs[i][j].plot(x, quad(x, *popt))
        axs[i][j].plot(betas5, chis5, "+", markersize=1)
        axs[i][j].set_title(f"$L={L}$")
        if i == 2:
            axs[i][j].set_xlabel("$\\beta$")
        if j == 0:
            axs[i][j].set_ylabel("$\chi$")
        axs[i][j].set_yscale("log")
plt.savefig("figs/chibeta.pdf")
plt.show()


def betafit(L, A, nu):
    return betac - A * np.power(L, -1/nu)

fig, axs = plt.subplots(1, 2, figsize=(16*cm, 8*cm))
axs = axs.flatten()
popt, pcov = curve_fit(betafit, Ls, betamaxlist)
print(f"A={popt[0]:.2f}")
print(f"nu={popt[1]:.2f}")
nu = popt[1]
x = np.linspace(32, 160, 300)
axs[0].plot(Ls, betamaxlist, ".")
axs[0].plot(x, betafit(x, *popt))
axs[0].set_xlabel("L")
axs[0].set_ylabel("$\\beta_{max}$")

def chifit(L, B, gamma):
    return B * np.power(L, gamma / nu)

popt, pcov = curve_fit(chifit, Ls, chimaxlist)
print(f"B={popt[0]:.2f}")
print(f"gamma={popt[1]:.2f}")
gamma = popt[1]
axs[1].plot(Ls, chimaxlist, ".")
axs[1].plot(x, chifit(x, *popt))
axs[1].set_xlabel("L")
axs[1].set_ylabel("$\\chi_{max}$")
plt.savefig("figs/maxfits.pdf")
plt.show()

print(gamma/nu)
