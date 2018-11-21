from solvers.solver import SolverTemplate, Stack
import random
import tkinter.messagebox as mb

class Solver(SolverTemplate):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                # Create a new stack to store tiles.
                self.stack = Stack()

                # Store the mazes start and end tiles.
                self.start = self.maze.start
                self.end = self.maze.end

                # If the start or end do not exist, the user messed up so we can't start the solver.
                if (self.start == None) or (self.end == None):
                        print("NO START OR END FOUND WTF WHY")

                # Set the starting tile to the mazes start.
                self.currentTile = self.start

                # Push the tile to the stack.
                self.stack.push(self.start)

                # If we are autorunning, call the step function.
                if self.autorun:
                        self.maze.parent.after(100, self.step)



        def step(self):
                if not self.autorun:
                        return
                # Get the current tiles neighbours, not including walls or tiles that have already been visited.
                tileNeighbours = self.currentTile.findNeighbours(distance = 1, blockVisited = True, blockWalls = True)

                # If the end tile is next to us, we have finished.
                if self.end in tileNeighbours:
                        self.stack.push(self.currentTile)
                        self.maze.solving = False
                        # Loop through the remaining stack and change all tiles to the FOUNDPATH type.
                        while not self.stack.isEmpty():
                                tile = self.stack.pop()
                                tile.setRoute()
                        # Return to stop function from executing.
                        return True

                # If there are unvisited neighbours, add the current tile to the stack and move to a random neighbour.
                if len(tileNeighbours) > 0:
                        self.stack.push(self.currentTile)

                        self.currentTile = random.choice(tileNeighbours)
                        self.currentTile.setVisited()
                # If there are no unvisited neighbours, set the current tile as visited and pop the next tile off the stack to go backwards.
                else:
                        self.currentTile.setVisited()
                        try:
                                self.currentTile = self.stack.pop()

                        # If we cannot pop an item then we have gone back to the start of the stack and the maze cannot be solved.
                        except IndexError:
                                mb.showerror("ERROR", "Cannot solve maze")
                                self.maze.solving = False
                                return
                  
                self.maze.parent.after(int(self.delay * 1000), self.step)

