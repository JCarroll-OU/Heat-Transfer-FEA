from SquareNodes import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Global variables
M = 25       # Number of nodes along the x-axis
N = 25       # Number of nodes along the y-axis
T_inf = 293 # Temperature of surroundings [K]

# Default node values
def_Egen = 0    # W/(m^2)
def_H = 80      # W/(m^2)
def_K = 15      # W/(m*K)
def_p = 1000    # kg/(m^3)
def_Cp = 4.184  # kJ/(kg*K)
def_T = 400     # K

class Cluster:
    # 2D Map of nodes within the cluster (region of simulation)
    Nodes = [[Node(def_Egen, def_H, def_K, def_p, def_Cp, def_T) for y in range(N)] for x in range(M)]
    Temperatures = np.zeros((NumSteps + 1, M, N)) 
    CurrentStep = 0 # Current step within the simulation

    # Allows certain nodes to have their types changed
    def SetNodeType(self, i, j, type):
        self.Nodes[i][j].nType = type
        if (type == NodeType.Env):
            self.Nodes[i][j].T = T_inf

    # Determine if a node is surrounded by other body nodes
    def isInternal(self, i, j):
        if (i == 0 or j == 0):
            return False
        try:
            left = self.Nodes[i - 1][j]
            bottom = self.Nodes[i][j + 1]
            right = self.Nodes[i + 1][j]
            top = self.Nodes[i][j - 1]
            if ((left.nType == NodeType.Body) and (bottom.nType == NodeType.Body) and (right.nType == NodeType.Body) and (top.nType == NodeType.Body)):
                return True
            else:
                return False
        except: # out-of-range
            return False
        
    # Determine the boundary condition, these can be overriden after a cluster is created
    def getBC(self, this_i, this_j, neighbor_i, neighbor_j):
        cond = BoundaryCondition.Conduction
        if ((neighbor_i < 0) or (neighbor_j < 0) or (neighbor_i >= M) or (neighbor_j >= N)):
            cond = BoundaryCondition.Insulated
        else:
            if ((self.Nodes[this_i][this_j].nType == NodeType.Env) or (self.Nodes[neighbor_i][neighbor_j].nType == NodeType.Env)):
                cond = BoundaryCondition.Convection
            else: 
                cond = BoundaryCondition.Conduction
        return cond
    
    # Convert boundary condition value to a string
    def bc_to_str(self, bCond):
        str = "N/A"
        if (bCond == BoundaryCondition.Insulated):
            str = "Insulated"
        elif (bCond == BoundaryCondition.Convection):
            str = "Convection"
        elif (bCond == BoundaryCondition.Conduction):
            str = "Conduction"
        else:
            str = "Error"
        return str

    # Generates a list of strings to display all boundary conditions within a node
    def bc_str_arr(self, i, j): # line length = 27 characters
        bConds = self.Nodes[i][j].bConditions
        if (self.isInternal(i, j)):
            spacer = "||=======================||"
            top_cond = "||" + self.bc_to_str(bConds[3]).center(23) + "||"
            mid_cond = "||" + self.bc_to_str(bConds[0]).center(10) + "||" + self.bc_to_str(bConds[2]).center(11) + "||"
            bot_cond = "||" + self.bc_to_str(bConds[1]).center(23) + "||"
        elif (self.Nodes[i][j].nType == NodeType.Env):
            spacer = "***************************"
            top_cond = "*" + self.bc_to_str(bConds[3]).center(25) + "*"
            mid_cond = "*" + self.bc_to_str(bConds[0]).center(12) + "*" + self.bc_to_str(bConds[2]).center(12) + "*"
            bot_cond = "*" + self.bc_to_str(bConds[1]).center(25) + "*"
        else:
            spacer = "|-------------------------|"
            top_cond = "|" + self.bc_to_str(bConds[3]).center(25) + "|"
            mid_cond = "|" + self.bc_to_str(bConds[0]).center(12) + "|" + self.bc_to_str(bConds[2]).center(12) + "|"
            bot_cond = "|" + self.bc_to_str(bConds[1]).center(25) + "|"
        return [
                    spacer,
                    top_cond,
                    spacer,
                    mid_cond,
                    spacer,
                    bot_cond,
                    spacer
                ]
    
    # Generates a list of strings to display temperature within a node
    def temp_str_arr(self, i, j): # line length = 12 characters
        if (self.isInternal(i, j)):
            spacer = "||==============||"
            temp = "||" + str(round(self.Nodes[i][j].T, 4)).center(14) + "||"
        elif (self.Nodes[i][j].nType == NodeType.Env):
            spacer = "******************"
            temp = "*" + str(round(self.Nodes[i][j].T, 4)).center(16) + "*"
        else:
            spacer = "|----------------|"
            temp = "|" + str(round(self.Nodes[i][j].T, 4)).center(16) + "|"
        return [
                    spacer,
                    temp,
                    spacer
                ]

    # Print node boundary conditions in the console in an human-readable format
    def print_bc(self):
        for j in range(N):
            nLines = []
            for i in range(M):
                nLines.append(self.bc_str_arr(i, j))
                
            for x in range(0, len(nLines)):
                print(nLines[x][0], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][1], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][2], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][3], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][4], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][5], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][6], end=" ")
            print(" ")

    # Print node temperatures in the console in an human-readable format
    def print_temps(self):
        for j in range(N):
            nLines = []
            for i in range(M):
                nLines.append(self.temp_str_arr(i, j))
                
            for x in range(0, len(nLines)):
                print(nLines[x][0], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][1], end=" ")
            print(" ")
            for x in range(0, len(nLines)):
                print(nLines[x][2], end=" ")
            print(" ")

    def __init__(self):
        for i in range(M):
            for j in range(N):
                self.Nodes[i][j] = Node(def_Egen, def_H, def_K, def_p, def_Cp, def_T)
                self.Temperatures[self.CurrentStep, i, j] = self.Nodes[i][j].T

    def Generate(self):
        for i in range(M):
            for j in range(N):
                # Assign a boudary condition to each node within the cluster
                self.Nodes[i][j].bConditions[0] = self.getBC(i, j, i - 1, j) # Left
                self.Nodes[i][j].bConditions[1] = self.getBC(i, j, i, j + 1) # Bottom
                self.Nodes[i][j].bConditions[2] = self.getBC(i, j, i + 1, j) # Right
                self.Nodes[i][j].bConditions[3] = self.getBC(i, j, i, j - 1) # Top
                self.Temperatures[self.CurrentStep, i, j] = self.Nodes[i][j].T

    def Q_Convection(self, i, j, ni, nj):
        return self.Nodes[ni][nj].h * L * (T_inf - self.Nodes[i][j].T)
    
    def Q_Conduction(self, i, j, ni, nj):
        return self.Nodes[i][j].k * ((self.Nodes[ni][nj].T - self.Nodes[i][j].T) / 2)

    def Q(self, i, j, ni, nj):
        nCondition = self.getBC(i, j, ni, nj)
        if (nCondition == BoundaryCondition.Conduction):
            return self.Q_Conduction(i, j, ni, nj)
        elif (nCondition == BoundaryCondition.Convection):
            return self.Q_Convection(i, j, ni, nj)
        else:
            return 0

    def NodeTimestep(self, i, j):
        cNode = self.Nodes[i][j]
        if (self.isInternal(i, j)):
            lNode = self.Nodes[i - 1][j]
            bNode = self.Nodes[i][j + 1]
            rNode = self.Nodes[i + 1][j]
            tNode = self.Nodes[i][j]
            cNode.T = ((1 - (4 * cNode.Tau)) * cNode.T) + (cNode.Tau * (lNode.T + bNode.T + rNode.T + tNode.T)) + (cNode.Tau * cNode.e_gen * ((L**2) / cNode.k))
        else:
            # this part might be wrong! 
            lQ = self.Q(i, j, i - 1, j)
            bQ = self.Q(i, j, i, j + 1)
            rQ = self.Q(i, j, i + 1, j)
            tQ = self.Q(i, j, i, j - 1)
            eGen = cNode.e_gen * L * (L / 2)
            cNode.T = cNode.T + ((lQ + bQ + rQ + tQ + eGen) / (cNode.p * ((L**2) / 2) * cNode.C_p)) * dT 

    def Update(self):
        self.CurrentStep += 1
        #print("Time = %ss"%(dT*self.CurrentStep))
        for i in range(M):
            for j in range(N):
                self.NodeTimestep(i, j)
                self.Temperatures[self.CurrentStep, i, j] = self.Nodes[i][j].T

# Cluster test
test = Cluster()
for x in range(0, N):
    test.SetNodeType(0, x, NodeType.Env)
    test.SetNodeType(M-1, x, NodeType.Env)
for y in range(0, M):
    test.SetNodeType(y, 0, NodeType.Env)
    test.SetNodeType(y, N-1, NodeType.Env)
test.Generate()
#test.print_bc()

for step in range(NumSteps):
    test.Update()

# Create the figure and axis
fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.2)  # Space for the slider

# Initial plot
heatmap = ax.imshow(test.Temperatures[0, :, :], cmap='viridis', origin='upper', aspect='auto')
colorbar = plt.colorbar(heatmap)
ax.set_title("Heatmap at Time: 0.00s")

# Define slider axis and create slider
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Position: [left, bottom, width, height]
slider = Slider(ax_slider, 'Time Step', 0, NumSteps, valinit=0, valstep=1)

# Update function for the slider
def update(val):
    timestep = int(slider.val)  # Get the slider value as an integer
    heatmap.set_data(test.Temperatures[timestep, :, :])  # Update plot data
    ax.set_title(f"Heatmap at Time: {timestep * dT}s")  # Update title
    fig.canvas.draw_idle()  # Redraw the figure

# Connect slider to update function
slider.on_changed(update)

# Show the interactive plot
plt.show()