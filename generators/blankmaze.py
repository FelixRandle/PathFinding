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

		self.generate()

	def generate(self):
		for column in self.maze.tiles:
			for tile in column:
				tile.setPath()
