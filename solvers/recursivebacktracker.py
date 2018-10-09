from solvers.solver import SolverTemplate, Stack

class Solver(SolverTemplate):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.autorun:
			self.maze.parent.after(int(self.delay * 1000), self.step)

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

		print("step")
		self.currentTile = self.stack.peek()
		self.currentTile.setVisited()

		self.maze.parent.after(int(self.delay * 1000), self.step)

