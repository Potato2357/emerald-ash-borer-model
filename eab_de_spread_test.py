import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import time


RHO = 0.002 # tree growth rate (really small because of the cubic)
K = 1000 # tree carrying capacity of forest
L = 5 # point at which the tree population undergoes catastrophic collapse
ALPHA = 0.05 # beetle destructiveness
DELTA = 10 # beetle saturation effect
GAMMA = 1 # beetle death
BETA = 0.05 # beetle reproduction
Q = 1000 # beetle carrying capacity of tree

def beetle_tree(t, z):
    x1, y1, x2, y2, x3, y3,  = z
    x1prime = RHO*x1*(1-x1/K)*(x1/L-1)-ALPHA*x1*np.log(1+DELTA*y1)
    y1prime = -GAMMA*y1+BETA*x1*y1*(1-y1/(Q*x1)) - (0.1*y1 - 0.05*y2 - 0.05*y3)*0.001
    x2prime = RHO*x2*(1-x2/K)*(x2/L-1)-ALPHA*x2*np.log(1+DELTA*y2)
    y2prime = -GAMMA*y2+BETA*x2*y2*(1-y2/(Q*x2)) - (0.1*y2 - 0.05*y1 - 0.05*y3)*0.001
    x3prime = RHO*x3*(1-x3/K)*(x3/L-1)-ALPHA*x3*np.log(1+DELTA*y3)
    y3prime = -GAMMA*y3+BETA*x3*y3*(1-y3/(Q*x3)) - (0.1*y3 - 0.05*y1 - 0.05*y2)*0.001
    return [x1prime, y1prime, x2prime, y2prime, x3prime, y3prime]



sim_length = 10

t_span = (0, sim_length)
y0 = [K, 5, K, 0, K, 0]
sol = solve_ivp(beetle_tree, t_span, y0, max_step=0.05)

# plt.plot(sol.t, sol.y[0], label='Trees')
# plt.plot(sol.t, sol.y[1], label='Beetles')
# plt.legend()
# plt.grid(True)
# plt.show()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10,5))
ax1.plot(sol.t, sol.y[1])
ax1.set_title('Beetles 1')
ax2.plot(sol.t, sol.y[3])
ax2.set_title('Beetles 2')
ax3.plot(sol.t, sol.y[5])
ax3.set_title('Beetles 3')

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

plt.show()