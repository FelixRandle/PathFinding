# Base solver class to import

class SolverTemplate:
	def __init__(self, maze, settings, advancedInformation):
		self.maze = maze
		for tileX in self.maze.tiles:
			for tile in tileX:
				tile.visitCount = 0
												
		self.settings = settings
		self.advancedInformation = advancedInformation
		self.autorun = settings.autoStepEnabled 
		self.delay = 1 / settings.speed.get()

		self.stack = Stack()

		self.steps = 0

	def autorun(self):
		pass

	def step(self):
		print("Current Solver not functional. Please ensure that your stepping function is called 'step' so it overrides the base function.")

	def getStack(self):
		return self.stack

	def updateSteps(self):
		self.advancedInformation.stepCount.config(text = "Steps: {}".format(self.steps))

	def setSpeed(self, newSpeed):
		self.delay = 1 / newSpeed
		self.settings.speed.set(newSpeed)

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
