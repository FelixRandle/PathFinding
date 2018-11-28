import random

class Generator:
	"""Generator class to generate a random maze given a maze object"""
	def __init__(self, maze, seed = None):
		"""
		Arguments:
			maze -- Maze object, should be all walls.
			seed -- Seed for random module.
		"""
		self.maze = maze
		self.size = self.maze.size

		# Create an empty list to be used as a stack.
		self.stack = []

				# Set the random seed.
		random.seed(seed)

				# Generate our maze.
		self.generate()

	def generate(self):
		walls = [[self.maze.tiles[int(x / 2)][int(y / 2)] for y in range(1, self.size)] for x in range(1, self.size)]
		for x in walls:
			for y in x:
				print(y.x, y.y)


	def randomTile(self):
		x = random.randint(1, size - 2)
		if x % 2 == 0:
			x += 1
		y = random.randint(1, size - 2)
		if y % 2 == 0:
			y += 1

		return self.maze.tiles[x][y]


	
	def removeWall(self, tile1, tile2):
		"""
		Internal method to remove the wall between two tiles
		TODO -- Possibly move this to our maze object so it can be accessed by all generators?
		"""
		if tile2.x ==  tile1.x:
			xPos = tile2.x
			yPos = tile2.y - int((tile2.y - tile1.y) / 2)
		else:
			yPos = tile2.y
			xPos = tile2.x - int((tile2.x - tile1.x) / 2)
		self.maze.tiles[xPos][yPos].setPath()


if __name__ == "__main__":
	print("")