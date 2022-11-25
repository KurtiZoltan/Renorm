import numpy as np
import matplotlib.pyplot as plt
import subprocess
from tqdm import tqdm
from scipy.optimize import curve_fit

def lorentz(x, a, b, c, d):
    return a / (b**2 + (x-c)**2) + d
    

Ls = [32, 48, 64, 80, 96, 112, 128, 144, 160]
betas = np.linspace(0.41, 0.45, 10)

points = []
for L in Ls:
    print(f"L={L}")
    chis = []
    x = []
    curr_betas = betas
    popt = [0, 0.01]
    for _ in range(5):
        for beta in tqdm(curr_betas):
            for i in range(1):
                res=subprocess.run(["./build/cluster", str(beta), str(L)], capture_output=True)
                chi = float(res.stdout.decode())
                chis.append(chi)
                x.append(beta)
                points.append([L, beta, chi])
            np.savetxt("points2.txt", np.array(points))
        chisarray = np.array(chis)
        xarray = np.array(x)
        xmax = xarray[np.argmax(chisarray)]
        chimax = chisarray[np.argmax(chisarray)]
        mask = chisarray > chimax / 2
        xmin = np.min(xarray[mask])
        xmax = np.max(xarray[mask])
        fwhm = max(xmax - xmin, curr_betas[1] - curr_betas[0])
        peak = (xmax + xmin) / 2
        curr_betas = np.linspace(peak - fwhm*0.75, peak + fwhm*0.75, 10)
    plt.plot(xarray, chisarray, ".", label=f"{L}")
plt.yscale("log")
plt.legend()
plt.show()
