from solvers.solver import SolverTemplate
import tkinter.messagebox as mb
import math


class Solver(SolverTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the starting tile to the mazes start.
        self.currentTile = self.start

        # Create empty dictionaries to use for tile distances and sources.
        self.dist = {}
        self.previous = {}
        self.tiles = []

        # Loop through each tile in the maze.
        for tileX in self.maze.tiles:
            for tile in tileX:
                # Give each tile a distance of infinity and no source.
                self.dist.update({tile: float("inf")})
                self.previous.update({tile: None})
                self.tiles.append(tile)

        # Set the distance of the start to 0.
        self.dist[self.start] = 0

        # If we are autorunning, call the step function.
        if self.autorun:
            self.maze.parent.after(100, self.step)

    def step(self, force=False):
        if not self.autorun and not force:
            return
        # Get the tile from the list with the lowest distance
        tile = self.smallestDistance()

        # If the tile is the end, we have found the shortest path.
        if self.end == tile:
            self.maze.solving = False
            self.solved = True

            target = tile
            if self.previous[target] is not None:
                while target is not None:
                    target.setRoute()

                    target = self.previous[target]
            # Return to stop function from executing.
            return
        # Try and remove this from the list, if we cannot then the maze
        # cannot be solved.
        try:
            self.tiles.remove(tile)
        except ValueError:
            mb.showerror("ERROR", "Cannot solve maze")
            self.maze.solving = False
            return

        # Get adjacent tiles.
        tile.findNeighbours(distance=1, blockVisited=True,
                            blockWalls=True)
        tileNeighbours = tile.neighbours

        # Loop through neighbouring tiles.
        for neighbour in tileNeighbours:
            # Calculate the distance to the neighbour from the starting node.
            neighbourDist = self.dist[tile] + self.distance(tile, neighbour)

            # If this is less than the current distance stored for the
            # neighbour then overwrite the distance and source.
            if neighbourDist < self.dist[neighbour]:
                neighbour.setVisited()
                self.dist[neighbour] = neighbourDist
                self.previous[neighbour] = tile

        # Increment step count.
        self.steps += 1
        self.updateSteps()

        # Run the next step if needed.
        if self.autorun:
            self.maze.parent.after(int(self.delay * 1000), self.step)

    def smallestDistance(self):
        returnTile = None
        dist = float("inf")
        # Loop through all tiles not yet discarded.
        for tile in self.tiles:
            # Get the tiles distance.
            tileDist = self.dist[tile]

            # If this distance is lower than the current lowest, use this tile.
            if tileDist < dist:
                dist = tileDist
                returnTile = tile

        # Return the tile with the lowest distance from the start.
        return returnTile

    def distance(self, tile1, tile2):
        """Return the distance between two tiles."""
        return (math.fabs(tile1.x - tile2.x) + math.fabs(tile1.y - tile2.y))
