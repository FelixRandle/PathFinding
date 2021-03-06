from solvers.solver import SolverTemplate
import tkinter.messagebox as mb
import math


class Solver(SolverTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if setup failed
        if not self.maze.solving:
            return
            
        # Set the starting tile to the mazes start.
        self.currentTile = self.start

        # Push the tile to the stack.
        self.stack.push(self.start)

        self.cost = {}
        self.dist = {}
        self.previous = {}
        self.tiles = []

        self.start.setVisited()

        for tileX in self.maze.tiles:
            for tile in tileX:
                self.cost.update({tile: float("inf")})
                self.dist.update({tile: float("inf")})
                self.previous.update({tile: None})
                tile.findNeighbours(distance=1, blockVisited=True,
                                    blockWalls=True)
                self.tiles.append(tile)

        self.dist[self.start] = 0
        self.cost[self.start] = 0

        # If we are autorunning, call the step function.
        if self.autorun:
            self.maze.parent.after(100, self.step)

    def step(self, force=False):
        if (not self.autorun and not force):
            return
        if len(self.tiles) > 0:
            tile = self.smallestDistance()

            try:
                self.tiles.remove(tile)
            except ValueError:
                mb.showerror("ERROR", "Cannot solve maze")
                self.maze.solving = False
                return

            tileNeighbours = tile.neighbours

            if self.end in tileNeighbours:
                self.maze.solving = False
                self.solved = True

                target = tile
                if self.previous[target] is not None:
                    while target is not None:
                        target.setRoute()

                        target = self.previous[target]
                # Return to stop function from executing.
                return

            for neighbour in tileNeighbours:
                if neighbour.visitCount > 0:
                    continue

                alt = self.dist[tile] + self.distance(tile, neighbour) + \
                    (self.distance(tile, self.end) * 2)
                neighbour.write(int(alt))
                if alt < self.cost[neighbour]:
                    neighbour.setVisited()
                    self.dist[neighbour] = self.dist[tile] + \
                        self.distance(tile, neighbour)
                    self.previous[neighbour] = tile
                    self.cost[neighbour] = alt

        self.steps += 1
        self.updateSteps()

        if self.autorun:
            self.maze.parent.after(int(self.delay * 1000), self.step)

    def smallestDistance(self):
        returnTile = None
        dist = float("inf")
        for tile in self.tiles:
            tileDist = self.cost[tile]

            if tileDist < dist:
                dist = tileDist
                returnTile = tile

        return returnTile

    def distance(self, tile1, tile2):
        return (math.fabs(tile1.x - tile2.x) + math.fabs(tile1.y - tile2.y))
