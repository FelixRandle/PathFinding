from solvers.solver import SolverTemplate, Stack
import random
import tkinter.messagebox as mb

class Solver(SolverTemplate):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if self.autorun:
                        self.maze.parent.after(int(self.delay * 1000), self.step)

                self.stack = Stack()

                self.start = self.maze.start
                self.end = self.maze.end

                if (self.start == None) or (self.end == None):
                        print("NO START OR END FOUND WTF WHY")

                self.currentTile = self.start

                self.stack.push(self.start)



        def step(self):
                if self.currentTile == self.end:
                        self.stack.push(self.currentTile)
                        while not self.stack.isEmpty():
                                tile = self.stack.pop()
                                tile.setFoundPath()
                        return True

                tileNeighbours = self.currentTile.findNeighbours(distance = 1, blockVisited = True, blockWalls = True)
                
                if len(tileNeighbours) > 0:
                        self.stack.push(self.currentTile)

                        self.currentTile = random.choice(tileNeighbours)
                        self.currentTile.setVisited()
                else:
                        self.currentTile.setVisited()
                        try:
                                self.currentTile = self.stack.pop()
                        except IndexError:
                                mb.showerror("ERROR", "Cannot solve maze")
                                return
                        
                        
                self.maze.parent.after(int(self.delay * 1000), self.step)

