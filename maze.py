# External Imports
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum 

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

# Class for the maze tiles.
class Tile:
	# Initialisation function
	def __init__(self, parent, xPos, yPos, size, tileType, border = 0.1):
		self.xPos = xPos
		self.yPos = yPos
		self.parent = parent
		self.size = size
		self.tileType = tileType
		self.borderSize = int(self.size * border)

		self.backgroundColour = tileColours[tileType][0]
		self.colour = tileColours[tileType][1]		

		self.background = parent.create_rectangle(self.xPos, self.yPos, 
			self.xPos + self.size, self.yPos + self.size, 
			fill = self.backgroundColour, outline = "")

		self.foreground = parent.create_rectangle(self.xPos + self.borderSize, self.yPos + self.borderSize, 
			self.xPos + (self.size - self.borderSize), self.yPos + (self.size - self.borderSize), 
			fill = self.colour, outline = "")

class Maze:
	
	def __init__(self, parent, size = 5, canvasSize = 600):
		self.parentWindow = parent
		self.size = size
		self.canvasSize = canvasSize

		self.canvas = tk.Canvas(self.parentWindow, width = canvasSize, height = canvasSize, background = "blue")

		self.tile = Tile(self.canvas, 0, 0, 50, tileTypes.END)

