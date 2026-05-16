import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import time


RHO = 0.5 # tree growth rate
K = 5000000 # tree carrying capacity of forest
# L = 5 # point at which the tree population undergoes catastrophic collapse
ALPHA = 0.05 # beetle destructiveness
DELTA = 1 # beetle saturation effect
GAMMA = 0 # beetle death
BETA = 3 # beetle reproduction
Q = 9000 # beetle carrying capacity of tree

def beetle_tree(t, z, seed, pred):
    x, y = z
    xprime = RHO*x*(1-x/K)-ALPHA*x*np.log(1+DELTA*y) + seed
    yprime = -GAMMA*y+BETA*y*(1-y/(Q*x)) - pred*y
    return [xprime, yprime]

def sim_node(sim_length, X0, Y0, jumps, jump_amount):

    t_last = 0
    y0_last = [X0, Y0]

    t_all = []
    X_all = []
    Y_all = []

    for i in range(len(jumps)):
        t_span = (t_last, jumps[i])
        y0 = y0_last
        sol = solve_ivp(beetle_tree, t_span, y0, max_step=0.05, args=(0,0))
        t_all.extend(sol.t)
        X_all.extend(sol.y[0])
        Y_all.extend(sol.y[1])
        t_last = jumps[i]
        y0_last = sol.y[:, -1]

        y0_last[1] += jump_amount[i]
        if y0_last[1] < 0:
            y0_last[1] = 0

    t_span = (t_last, sim_length)
    y0 = y0_last
    sol = solve_ivp(beetle_tree, t_span, y0, max_step=0.05, args=(0,0))
    t_all.extend(sol.t)
    X_all.extend(sol.y[0])
    Y_all.extend(sol.y[1])

    return t_all, X_all, Y_all

def sim_node_test():

    sim_length = 10

    beetle_t = [0]
    intro_n = [5]

    start = time.time()

    t_sim, x_sim, y_sim = sim_node(sim_length, K, 0, beetle_t, intro_n)

    end = time.time()
    print(f"Runtime: {end - start} seconds")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    ax1.plot(t_sim, x_sim)
    ax1.set_title('Trees')
    ax2.plot(t_sim, y_sim)
    ax2.set_title('Beetles')

    for t in beetle_t:
        ax1.axvline(t, color='red', linestyle='--', alpha=0.3)
        ax2.axvline(t, color='red', linestyle='--', alpha=0.3)

    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax1.grid(True)
    ax2.grid(True)
    plt.show()

def discrete_sim():

    sim_length = 10
    sim_step_num = 5000

    beetle_t = [0]
    intro_n = [5]

    start = time.time()

    t_sim = [0] #[t*sim_length/sim_step_num for t in range(0,sim_step_num+1)]
    x_sim = [K]
    y_sim = [5]

    for i in range(sim_step_num):

        x = x_sim[-1]
        y = y_sim[-1]

        tprime = sim_length/sim_step_num
        xprime = tprime*(RHO*x*(1-x/K)-ALPHA*x*np.log(1+DELTA*y)) # + seed
        yprime = tprime*(-GAMMA*y+BETA*y*(1-y/(Q*x))) # - pred*y

        t_sim.append(t_sim[-1]+tprime)
        x_sim.append(x_sim[-1]+xprime)
        y_sim.append(y_sim[-1]+yprime)


    end = time.time()
    print(f"Runtime: {end - start} seconds")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    ax1.plot(t_sim, x_sim)
    # ax1.set_title('Trees')
    ax1.set_ylabel("Ash Trees")
    ax1.set_xlabel("Years Since EAB Introduction")
    ax2.semilogy(t_sim, y_sim)
    # ax2.set_title('Beetles')
    ax2.set_ylabel("Emerald Ash Borers")
    ax2.set_xlabel("Years Since EAB Introduction")

    # for t in beetle_t:
    #     ax1.axvline(t, color='red', linestyle='--', alpha=0.3)
    #     ax2.axvline(t, color='red', linestyle='--', alpha=0.3)

    # ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax1.grid(True)
    ax2.grid(True)

    # plt.plot(x_sim, y_sim)

    plt.show()


if __name__ == '__main__':
    # sim_node_test()
    discrete_sim()