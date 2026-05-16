import matplotlib.pyplot as plt
import numpy as np

tms = [t/500 for t in range(10)]
means = []
stds = []

with open("montecarlo_sim_results.txt", "r") as f:
    for i in range(10):
        line = f.readline()
        results = line.split(",")
        results.remove("\n")
        results = [float(x) for x in results]
        means.append(np.mean(results))
        stds.append(np.std(results))

print(len(results))

fig, ax = plt.subplots()

ax.errorbar(tms,means,yerr=stds,fmt='o-', capsize=6)

ax.set_xlabel("Transport chance")
ax.set_ylabel("Average time of first infection")
ax.set_xticks(np.arange(0, 0.02, 0.002))


plt.show()