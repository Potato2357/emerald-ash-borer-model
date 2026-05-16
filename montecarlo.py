import pandas
import numpy as np
import subprocess

fcontent = []

with open("montecarlo_sim_results.txt", "r") as f:
    for i in range(10):
        line = f.readline()
        fcontent.append(line.strip())

tms = [t/500 for t in range(10)]

f = open("montecarlo_sim_results.txt", "w")

for i in range(10):
    temp = []
    subprocess.run(['python3', 'eab_sim.py', str(tms[i])])
    data = pandas.read_csv("sim_data.csv")
    finish_times = list(data.iloc[:, 1])
    while -1 in finish_times:
        finish_times.remove(-1)
        print("!")
    f.write(fcontent[i] + str(np.mean(finish_times)) + ",\n")

f.close()