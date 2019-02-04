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

		self.NORTH = [0, 2]
		self.WEST = [2, 0]

				# Set the random seed.
		random.seed(seed)

				# Generate our maze.
		self.generate()

	def generate(self):
		self.edges = []

		self.sets = []

		for y in self.maze.tiles:
			for x in y:
				if self.isOdd(x.x) and self.isOdd(x.y):
					self.sets.append([x])
					x.setPath()
					if x.y > 0 and x.y < self.maze.size - 3:
						self.edges.append([x.x, x.y, self.NORTH])
					if x.x > 0 and x.x < self.maze.size - 3:
						self.edges.append([x.x, x.y, self.WEST])

		random.shuffle(self.edges)

		while len(self.edges) != 0:
			x, y, direction = self.edges.pop()
			newX, newY = x + direction[0], y + direction[1]
			self.xySet = None
			self.newxySet = None
			for i in range(len(self.sets)):
				if self.xySet != None and self.newxySet != None:
					break
				if self.maze.tiles[x][y] in self.sets[i]:
					self.xySet = i
				if self.maze.tiles[newX][newY] in self.sets[i]:
					self.newxySet = i

			if self.xySet == self.newxySet:
				continue
			else:
				self.connectTiles(self.maze.tiles[x][y], direction)
				self.sets[self.xySet] = self.sets[self.xySet] + self.sets[self.newxySet]
				self.sets.remove(self.sets[self.newxySet])

		# Set the top left and bottom right to the start and end respectively.
		self.maze.tiles[0][1].setStart()
		self.maze.tiles[self.maze.size - 1][self.maze.size - 2].setEnd()

	def isOdd(self, num):
		return bool(num % 2)


	def connectTiles(self, tile, direction):
		"""
		Internal method to remove the wall between two tiles
		TODO -- Possibly move this to our maze object so it can be accessed by all generators?
		"""
		self.maze.tiles[tile.x][tile.y].setPath()
		self.maze.tiles[tile.x+(direction[0] // 2)][tile.y+(direction[1] // 2)].setPath()
		self.maze.tiles[tile.x+(direction[0])][tile.y+(direction[1])].setPath()


if __name__ == "__main__":
	print("")
