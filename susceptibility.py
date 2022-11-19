import numpy as np
import matplotlib.pyplot as plt
import subprocess
from tqdm import tqdm

betas = np.linspace(0.4, 0.46, 50)
chis = []

for beta in tqdm(betas):
    temp = []
    for i in range(10):
        res=subprocess.run(["./build/cluster", str(beta), "32"], capture_output=True)
        temp.append(float(res.stdout.decode()))
    chis.append(sum(temp)/len(temp))

plt.plot(betas, chis, "o")
plt.show()