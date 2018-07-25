#Internal Imports
import maze

#External imports
import tkinter as tk
import tkinter.ttk as ttk
from fractions import Fraction
from generators.recursivebacktracker import Generator


class Application(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.title("PathFinding")
		self.iconbitmap("assets/maze.ico")

		self.screenSize = int(self.winfo_screenheight() * 0.7)
		self.minsize(width=self.screenSize - 5, height=self.screenSize - 5)
		self.resizable(False, False)

		self.frames = {}

		frame = HomeScreen(self)
		self.frames[HomeScreen] = frame
		self.frames[SettingsMenu] = SettingsMenu(self)
		self.frames[SettingsMenu].grid(row = 0, column = 0)
		frame.grid(row = 0, column = 0)

		self.changeFrame(HomeScreen)

	def changeFrame(self, newFrame):
		for frame in self.grid_slaves():
			frame.grid_forget()
		frame = self.frames[newFrame]
		frame.grid(row = 0, column = 0)

class HomeScreen(tk.Frame):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

		self.loadTopMenu()
		self.loadMaze()


	def loadTopMenu(self):
		menubar = tk.Menu(self.parent)
		self.parent.config(menu = menubar)

		fileMenu = tk.Menu(menubar, tearoff = False)
		fileMenu.add_command(label = "Save Maze", command = lambda: print("Save Maze"))
		fileMenu.add_command(label = "Load Maze", command = lambda: print("Load Maze"))
		fileMenu.add_separator()
		fileMenu.add_command(label = "Save Solve", command = lambda: print("Save Solve"))
		fileMenu.add_command(label = "Load Solve", command = lambda: print("Load Solve"))
		menubar.add_cascade(label = "File", menu = fileMenu)

		generatorMenu = tk.Menu(menubar, tearoff = False)
		generatorMenu.add_command(label = "Generate New Maze", command = lambda: Generator(self.maze))
		generatorMenu.add_command(label = "Edit Generation Settings", command = lambda: print("Edit Generation Settings"))
		menubar.add_cascade(label = "Generate", menu = generatorMenu)

		solverMenu = tk.Menu(menubar, tearoff = False)
		solverMenu.add_command(label = "Solve Current Maze", command = lambda: print("Solve Current Maze"))
		solverMenu.add_command(label = "Edit Solve Settings", command = lambda: self.parent.changeFrame(SettingsMenu))
		menubar.add_cascade(label = "Solve", menu = solverMenu)

		editMenu = tk.Menu(menubar, tearoff = False)
		editMenu.add_command(label = "Toggle edit mode", command = lambda: print("Toggled edit"))
		menubar.add_cascade(label = "Edit", menu = editMenu)

	def loadMaze(self):
		# TODO Load in maze using user defined settings.
		# This includes creating maze then giving to generator before drawing.
		# For now, no generation occurs.

		self.maze = maze.Maze(self, canvasSize = self.parent.screenSize, size = 51)
		self.maze.canvas.grid(row = 0, column = 1)


class SettingsMenu(tk.Frame):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

		self.buttonImage = tk.PhotoImage(file = "assets/home_button.png")

		xScale = Fraction(parent.screenSize / self.buttonImage.width()).limit_denominator(max_denominator=100)
		yScale = Fraction((parent.screenSize / self.buttonImage.height()) * 0.1).limit_denominator(max_denominator=100)

		self.buttonImage = self.buttonImage.zoom(xScale.numerator, yScale.numerator)
		self.buttonImage = self.buttonImage.subsample(xScale.denominator, yScale.denominator)

		self.homeButton = tk.Button(self, image = self.buttonImage, command = lambda: parent.changeFrame(HomeScreen))
		self.homeButton.grid(row = 0, column = 0)
		