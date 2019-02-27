import random


class Generator:
    """Generator class to generate a random maze given a maze object"""
    def __init__(self, maze, seed=None):
        """
        Arguments:
            maze -- Maze object, should be all walls.
            seed -- Seed for random module.
        """
        self.maze = maze

        # Create an empty list to be used as a stack.
        self.stack = []

        # Set the random seed.
        random.seed(seed)

        # Generate our maze.
        self.generate()

    def generate(self):
        """
        Implementation of a simple recursive backtracker algorithm
        """
        # Put the starting tile at the top of the stack.
        # Pick a random x and y to start at. Ensuring that they are
        # on odd rows/columns.
        size = self.maze.size
        x = random.randint(1, size - 2)
        if x % 2 == 0:
            x += 1
        y = random.randint(1, size - 2)
        if y % 2 == 0:
            y += 1

        self.stack.insert(0, self.maze.tiles[x][y])

        # While there are items in the stack, the maze cannot be complete.
        while len(self.stack) > 0:
            # Set the current tile to the top of the stack.
            self.currentTile = self.stack[0]

            # Set the current tile as visited
            self.currentTile.visitCount += 1

            # Get the unvisited neighbours of the current tile.
            neighbours = self.currentTile.findNeighbours(blockVisited=True)

            # If the current tile has any unvisited neighbours, carry on.
            if len(neighbours) > 0:
                # Pick a random neighbour
                newTile = random.choice(neighbours)

                # Put the current tile in the stack.
                self.stack.insert(0, self.currentTile)

                # Put a path inbetween our current tile and the randomly
                # chosen neighbour.
                self.removeWall(self.currentTile, newTile)

                # Change both our current tile and newly chosen tile to a path.
                self.currentTile.setPath()
                newTile.setPath()

                # Put the new tile in the stack
                self.stack.insert(0, newTile)

            # If there are no unvisited neighbours, remove the top of the
            # stack to go backwards down the visited path.
            else:
                self.stack.pop(0)

        # Set the top left and bottom right to the start and end respectively.
        self.maze.tiles[0][1].setStart()
        self.maze.tiles[self.maze.size - 1][self.maze.size - 2].setEnd()

    def removeWall(self, tile1, tile2):
        """
        Internal method to remove the wall between two tiles
        """
        if tile2.x == tile1.x:
            xPos = tile2.x
            yPos = tile2.y - int((tile2.y - tile1.y) / 2)
        else:
            yPos = tile2.y
            xPos = tile2.x - int((tile2.x - tile1.x) / 2)
        self.maze.tiles[xPos][yPos].setPath()
