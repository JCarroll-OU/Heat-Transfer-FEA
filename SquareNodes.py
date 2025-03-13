from enum import Enum

# Global variables
dT = 0.01      # Time between each step of the simulation
L = 0.01       # dX = dY = l; Length of node in x- and y-directions
NumSteps = 100 # Number of steps to run the simulation for

class NodeType(Enum):
    Env = 0     # Surrounding environment
    Body = 1    # Body to analyze

class BoundaryCondition(Enum):
    Insulated = 0       # Experiences no heat transfer (assigned if out-of-range)
    Convection = 1      # Experiences convection (assigned if Env node is adjacent)
    Conduction = 2      # Experiences conduction (assigned if Body node is adjacent)
    

class Node:
    #-- Name ---#----------------------- Description -----------------------#---- Units ----
    e_gen = 0   # Heat generation within the element                        # W/(m^2)
    h = 1       # Convection heat transfer coefficient                      # W/(m^2 * K)
    k = 1       # Thermal conductivity                                      # W/(m*K)
    p = 1       # (Rho) Density of the element                              # kg/(m^3)
    C_p = 1     # Specific heat capacity (at const. pressure)               # kJ/(kg*K)
    a = 1       # (Alpha) Thermal Diffusivity [Calculated w/ k, p, C_p]     # (m^2)/s
    Tau = 1     # Fourier Number [Calculated w/ a, dT, L]                   # Dimensionless
    T = 1       # Temperature of the node                                   # K

    # Nodes can be considered either part of the element or part of the surroundings.
    # Body nodes at the edge of the simulation will not experience convection.
        # To experience convection around all sides of the element, Env nodes must surround the body nodes.
    nType = NodeType.Body

    bConditions = [BoundaryCondition.Conduction, # Left side
                   BoundaryCondition.Conduction, # Bottom side
                   BoundaryCondition.Conduction, # Right side
                   BoundaryCondition.Conduction] # Top side

    def __init__(self, _e_gen, _h, _k, _p, _cp, _Ti):
        self.e_gen = _e_gen
        self.h = _h
        self.k = _k
        self.p = _p
        self.C_p = _cp
        self.T = _Ti
        self.a = self.k / (self.p * self.C_p)
        self.Tau = (self.a * dT) / (L**2)
        if ((self.Tau < 0.25) or (dT < ((L**2)/(4 * self.a)))):
            print("Unstable simulation parameters!")
        self.bConditions = [BoundaryCondition.Conduction] * 4 # Makes each list of boundary conditions unique