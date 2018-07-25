# External Imports
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum 
import random

# Enum for the different tiles we can have in the maze.
class tileTypes(Enum):
	WALL = 0
	PATH = 1
	VISITEDPATH = 2
	START = 10
	END = 11

# Dictionary of colours to use for different tiles, background then foreground
tileColours = {	tileTypes.WALL: ["black", "black"],
				tileTypes.PATH: ["light grey", "white"],
				tileTypes.VISITEDPATH: ["light grey", "purple"],
				tileTypes.START: ["green", "light green"],
				tileTypes.END: ["red", "pink"]
			}

class Tile:
	"""Class used for the tiles of a maze."""
	def __init__(self, parent, maze, xPos, yPos, size, tileType, border = 0.1):
		""" 
		Arguments:
			parent -- the parent canvas that the tile will use.
			xPos -- The x grid coordinate of the tile.
			yPos -- The y grid coordinate of the tile.
			size -- The width and height that the tile should be.
			tileType -- Used to define what the tile should appear as.
			border -- Used to define the percentage of the size that the border should be. (Default 0.1)
		"""
		self.parent = parent
		self.maze = maze
		self.x = xPos
		self.y = yPos
		self.xPos = xPos * size
		self.yPos = yPos * size
		self.size = size
		self.tileType = tileType
		self.borderSize = int(self.size * border)

		self.visited = False
		self.neighbours = []
		self.backgroundColour = tileColours[tileType][0]
		self.colour = tileColours[tileType][1]

		# Create the canvas rectangle.
		self.canvasRect = parent.create_rectangle(int(self.xPos + (self.borderSize / 2)), int(self.yPos + (self.borderSize / 2)), 
			int(self.xPos + (self.size - self.borderSize / 2)), int(self.yPos + (self.size - self.borderSize / 2)), 
			fill = self.colour, outline = self.backgroundColour, width = self.borderSize)

	def findNeighbours(self):
		"""
		Method for finding the current tiles neighbours.
		Find those two away as all walls are placed on even coordinates
		"""
		relativeNeighbours = [			[0, 2],
								[-2, 0],       [2, 0],
										[0, -2]
							]

		for coords in relativeNeighbours:
			if (self.x + coords[0] >= 0) and (self.y + coords[1] >= 0):
				try:
					self.neighbours.append(self.maze.tiles[self.x + coords[0]][self.y + coords[1]])

				except IndexError:
					pass
			

	def toString(self):
		return ""

	def fromString(self, source):
		pass

	def changeType(self, newType = tileTypes.PATH):
		"""
		Internal method for changing the tile type. This should not be used by generators or solvers.
		Arguments:
			newType -- The new tileType that it should be changed to.
		"""
		self.tileType = newType
		self.parent.itemconfig(self.canvasRect, fill = tileColours[self.tileType][1])
		self.parent.itemconfig(self.canvasRect, outline = tileColours[self.tileType][0])

	def setPath(self):
		"""
		Set the current tile to a PATH tile
		"""
		self.changeType(newType = tileTypes.PATH)

	def setStart(self):
		"""
		Set the current tile to a START tile.
		TODO - Setting this will overwrite any current START tile.
		"""
		self.changeType(newType = tileTypes.START)

	def setEnd(self):
		"""
		Set the current tile to an END tile.
		TODO - Setting this will overwrite any current END tile.
		"""
		self.changeType(newType = tileTypes.END)

class Maze:
	"""Class used to hold maze information."""
	def __init__(self, parent, size = 15, canvasSize = 600):
		""" 
		Arguments:
			parent -- The parent from tkinter, either Frame or Tk object.
			size -- The width and height of the maze. (Default 5)
			canvasSize -- The size in pixels of the canvas to use to display the maze. (Default 600)
		"""
		self.parent = parent
		self.size = size
		self.canvasSize = canvasSize

		self.canvas = tk.Canvas(self.parent, width = canvasSize, height = canvasSize, background = "blue", borderwidth = 0, highlightthickness = 0)

		self.tiles = [[Tile(self.canvas, self, x, y, self.canvasSize / self.size, tileTypes.WALL) for y in range(0, size)] for x in range(0, size)]
		for x in range(0, self.size):
			for y in range(0, self.size):
				self.tiles[x][y].findNeighbours()

		self.canvas.bind("<B1-Motion>", self.onMouseClick)
		self.canvas.bind("<Button-1>", self.onMouseClick)

	def toFile(self, filePath):
		"""
		Method for saving the current maze to a file.
		Arguments:
			filePath -- Path to where to save the file
		"""
		pass

	def fromFile(self, filePath):
		"""
		Method for loading a maze from a file.
		Arguments:
			filePath -- Path to pull the maze from.
		"""
		pass

	def onMouseClick(self, event):
		"""
		Internal method for handling mouse click events.
		This allows the user to 'draw' parts of the maze.
		"""
		listX = int(event.x / (self.canvasSize / self.size))
		listY = int(event.y / (self.canvasSize / self.size))
		try:
			if listX >= 0 and listY >= 0:
				self.tiles[listX][listY].setPath()
		except IndexError:
			pass
			