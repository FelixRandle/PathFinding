# G COST - Distance from start point
# F COST - Literal Distance from end point
# Total Cost = G COST + F Cost

from solvers.solver import SolverTemplate, Stack
import random
import tkinter.messagebox as mb

class Solver(SolverTemplate):
    def __init__(self *args, **kwargs):
        super().__init__(*args, **kwargs)
