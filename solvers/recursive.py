import solver
from solver import Stack

class mazeSolver(solver):
	def __init__(self):
		super().__init__()

		if self.autorun:
			print("Autorunning now.")

		self.stack = Stack()
		self.currentTile = None

		self.start = self.maze.start
		self.end = self.maze.end

		if (self.start == None) or (self.end == None):
			print("NO START OR END FOUND WTF WHY")

		self.stack.push(self.start)



	def step(self):
		if self.currentTile == self.end:
			print("REACHED END")
			return True

		self.currentTile = self.stack.peek()
		self.currentTile.setPath(travelled = True)

