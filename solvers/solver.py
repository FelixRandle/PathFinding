# Base solver class to import

class SolverTemplate:
	def __init__(self, maze, autorun = False, delay = 0.1):
		self.maze = maze
		for tileX in self.maze.tiles:
			for tile in tileX:
				tile.visited = (False if tile.visited else True)
		self.autorun = autorun
		self.delay = delay

	def autorun(self):
		pass

	def step(self):
		print("Current Solver not functional. Please ensure that your stepping function is called 'step' so it overrides the base function.")

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
