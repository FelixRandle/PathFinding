from solvers.solver import SolverTemplate, Stack
import random


class Solver(SolverTemplate):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.autorun:
			self.maze.parent.after(int(self.delay * 1000), self.step)

		self.stack = Stack()

		self.start = self.maze.start
		self.end = self.maze.end

		if (self.start == None) or (self.end == None):
			print("NO START OR END FOUND WTF WHY")

		self.currentTile = self.start

		self.stack.push(self.start)



	def step(self):
		if self.currentTile == self.end:
			print("REACHED END")
			return True

		try:
			self.currentTile = random.choice(self.currentTile.findNeighbours(distance = 1, blockVisited = True, blockWalls = True))
		except IndexError:
			self.currentTile.setVisited()
			self.currentTile = self.stack.pop()
			self.maze.parent.after(int(self.delay * 1000), self.step)
			return


		self.currentTile.setVisited()

		self.stack.push(self.currentTile)

		self.maze.parent.after(int(self.delay * 1000), self.step)

