# External Imports
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum 
import random

# Enum for the different tiles we can have in the maze.
class tileTypes(Enum):
	WALL = 0
	PATH = 1
	START = 2
	END = 3

# Dictionary of colours to use for different tiles, background then foreground
tileColours = {	tileTypes.WALL: ["black", "black"],
				tileTypes.PATH: ["grey", "white"],
				tileTypes.START: ["blue", "green"],
				tileTypes.END: ["blue", "red"]
			}

class Tile:
	"""Class used for the tiles of a maze."""
	def __init__(self, parent, xPos, yPos, size, tileType, border = 0.1):
		""" 
		Arguments:
		parent -- the parent canvas that the tile will use.
		xPos -- The x grid coordinate of the tile.
		yPos -- The y grid coordinate of the tile.
		size -- The width and height that the tile should be.
		tileType -- Used to define what the tile should appear as.
		border -- Used to define the percentage of the size that the border should be. (Default 0.1)
		"""
		self.xPos = xPos * size
		self.yPos = yPos * size
		self.parent = parent
		self.size = size
		self.tileType = tileType
		self.borderSize = int(self.size * border)

		self.backgroundColour = tileColours[tileType][0]
		self.colour = tileColours[tileType][1]		

		#Create the background rectangle.
		self.background = parent.create_rectangle(self.xPos, self.yPos, 
			self.xPos + self.size, self.yPos + self.size, 
			fill = self.backgroundColour, outline = "")

		# Create the foreground rectangle.
		self.foreground = parent.create_rectangle(self.xPos + self.borderSize, self.yPos + self.borderSize, 
			self.xPos + (self.size - self.borderSize), self.yPos + (self.size - self.borderSize), 
			fill = self.colour, outline = "")

	def setColour(self, foreground = "Black", background = "Black"):
		"""
		Method for resetting the colour of the tile
		Arguments:
		foreground -- The new colour of the foreground of the tile. (Default "Black")
		background -- The new colour of the background of the tile. (Default "Black")
		"""
		self.parent.itemconfig(self.foreground, fill = foreground)
		self.parent.itemconfig(self.background, fill = background)

class Maze:
	"""Class used to hold maze information."""
	def __init__(self, parent, size = 5, canvasSize = 600):
		""" 
		Arguments:
		parent -- The parent from tkinter, either Frame or Tk object.
		size -- The width and height of the maze. (Default 5)
		canvasSize -- The size in pixels of the canvas to use to display the maze. (Default 600)
		"""
		self.parentWindow = parent
		self.size = size
		self.canvasSize = canvasSize

		self.canvas = tk.Canvas(self.parentWindow, width = canvasSize, height = canvasSize, background = "blue")

		self.tiles = [[Tile(self.canvas, x, y, self.canvasSize / self.size, random.choice(list(tileTypes))) for x in range(0, size)] for y in range(0, size)]

		print(self.tiles)

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

