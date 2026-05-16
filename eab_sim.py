import numpy as np
import matplotlib.pyplot as plt
import time
import sys


RHO = 0.1 # tree growth rate
# K = 1000000 # tree carrying capacity of forest
# L = 5 # point at which the tree population undergoes catastrophic collapse
ALPHA = 0.05 # beetle destructiveness
DELTA = 1 # beetle saturation effect
# GAMMA = 1 # beetle death
BETA = 3 # beetle reproduction
Q = 9000 # beetle carrying capacity of tree

ETA = 0.1 # inter-node spread rate

if len(sys.argv) > 1:
    HUMAN_SPREAD = float(sys.argv[1])
else:
    HUMAN_SPREAD = 0.01

SIM_LENGTH = 25
SIM_STEP_NUM = 10000

class Node:
    def __init__(self, name, beetle_0, size):
        self.name = name
        self.K = size * 2000 # carrying capacity = 2 kilotrees per km^2
        self.tree_num = [size * 2000]
        self.beetle_num = [beetle_0]
        self.radius = int(np.sqrt(size))
        self.diffusion = 0
        self.fully_infected = False
        self.infected = False
        self.infection_time = -1

    def __str__(self):
        result = f"|{self.name}:{self.tree_num[-1]},{self.beetle_num[-1]}|"
        return result
    
    def increment_step(self):

        if not self.infected and self.beetle_num[-1] != 0:
            self.infected = True
            self.infection_time = (len(self.tree_num) - 1) * SIM_LENGTH/SIM_STEP_NUM


        #calculate the beetle and tree differential equation
        x = self.tree_num[-1]
        y = self.beetle_num[-1]

        tprime = SIM_LENGTH/SIM_STEP_NUM
        xprime = tprime*(RHO*x*(1-x/self.K)-ALPHA*x*np.log(1+DELTA*y)) # + seed
        yprime = tprime*(BETA*y*(1-y/(Q*x))) # - pred*y

        #increase diffusion / calculate spread
        beetle_leave = 0
        if not self.fully_infected and self.beetle_num[-1] > 0:
            temp = np.random.rand()
            if temp < 20 * tprime:
                self.diffusion += 1
            if self.diffusion == self.radius:
                self.fully_infected = True
        elif self.fully_infected:
            beetle_leave = tprime*ETA*y
            yprime -= beetle_leave

        #add beetles/trees
        self.tree_num.append(self.tree_num[-1]+xprime)
        self.beetle_num.append(self.beetle_num[-1]+yprime)

        return beetle_leave
    
    def add_tree(self, num):
        self.tree_num[-1] += num
    
    def add_beetle(self, num):
        self.beetle_num[-1] += num
    
    def get_tree(self):
        return self.tree_num[-1]
    
    def get_beetle(self):
        return self.beetle_num[-1]
    
    def get_sims(self):
        return self.tree_num, self.beetle_num


class Graph:
    def __init__(self):
        self.adjacencies = {}

    def __str__(self):
        result = ""
        for node in self.adjacencies:
            edges = ", ".join(f"{nbr}" for nbr in self.adjacencies[node])
            result += f"{node} -> [{edges}] \n"
        return result

    def add_node(self, node):
        if node not in self.adjacencies:
            self.adjacencies[node] = []

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        self.adjacencies[u].append(v)
        self.adjacencies[v].append(u)

    def increment_step(self):
        source_num = 0
        for node, adj in self.adjacencies.items():
            beetles_left = node.increment_step()
            for n in adj:
                n.add_beetle(beetles_left/len(adj))
            if node.fully_infected == True:
                source_num += 1
        for node in self.adjacencies.keys():
            if node.fully_infected == False:
                temp = np.random.rand()
                if temp < HUMAN_SPREAD * source_num * SIM_LENGTH/SIM_STEP_NUM:
                    node.add_beetle(10)

    def get_sims(self):
        sims = []
        for node in self.adjacencies.keys():
            tree, beetle = node.get_sims()
            sims.append((tree, beetle))
        return sims


    def print_sims_tree(self, filepath):
        skip_amount = int(SIM_STEP_NUM/SIM_LENGTH/2)
        t = [t*SIM_LENGTH/SIM_STEP_NUM for t in range(0,SIM_STEP_NUM+1)]
        out = t[::skip_amount]
        with open(filepath, "w") as f:
            f.write("COUNTY_NAM,INF_T," + ",".join(map(str,out)) + "\n")
            for node in self.adjacencies.keys():
                tree, beetle = node.get_sims()
                tree_max = node.K
                temp = tree[::skip_amount]
                out = [x / tree_max for x in temp]
                f.write(node.name+","+str(node.infection_time)+"," + ",".join(map(str,out)) + "\n")

    def print_sims_beetle(self, filepath):
        skip_amount = int(SIM_STEP_NUM/40)
        t = [t*SIM_LENGTH/SIM_STEP_NUM for t in range(0,SIM_STEP_NUM+1)]
        out = t[::skip_amount]
        with open(filepath, "w") as f:
            f.write("COUNTY_NAM,INF_T," + ",".join(map(str,out)) + "\n")
            for node in self.adjacencies.keys():
                tree, beetle = node.get_sims()
                beetle_max = node.K * Q
                temp = beetle[::skip_amount]
                out = [x / beetle_max for x in temp]
                f.write(node.name+","+str(node.infection_time)+"," + ",".join(map(str,out)) + "\n")


def load_graph(filepath):

    edges = []
    nodes = {}

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # handle first line
            if line.startswith("#"):
                node_l = line.split()
                nodes[node_l[1]] = Node(node_l[1],int(node_l[2]),int(node_l[3]))
                continue
            
            edge_l = line.split()

            if len(edge_l) == 2:
                start, end = edge_l
            else:
                raise ValueError(f"Invalid line: {line}")

            edges.append((start, end))

    graph = Graph()

    for node in nodes.values():
        graph.add_node(node)

    for start, end in edges:
        graph.add_edge(nodes[start], nodes[end])

    return graph


if __name__ == "__main__":
    counties_r = "graph_pa_counties.txt"
    g = load_graph(counties_r)

    # print(g)

    start = time.time()

    for i in range(SIM_STEP_NUM):
        g.increment_step()

    end = time.time()
    print(f"Runtime: {end - start} seconds")
    
    sim_output = "sim_data.csv"
    g.print_sims_tree(sim_output)
    # g.print_sims_beetle(sim_output)

    # t = [t*SIM_LENGTH/SIM_STEP_NUM for t in range(0,SIM_STEP_NUM+1)]
    # result = g.get_sims()
    # fig, ax = plt.subplots(2, 4)
    # for i in range(4):
    #     ax[0,i].plot(t, result[i][0])
    #     ax[0,i].set_title(f"Trees (Node {i})")
    #     ax[1,i].plot(t, result[i][1])
    #     ax[1,i].set_title(f"Beetles (Node {i})")
    #     ax[0,i].grid(True)
    #     ax[1,i].grid(True)
    #     ax[1,i].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    # plt.show()

