#Internal Imports
import maze

#External imports
import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.screenSize = int(self.winfo_screenheight() * 0.7)
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

		fileMenu = tk.Menu(menubar)
		fileMenu.add_command(label = "Save Maze", command = lambda: print("Save Maze"))
		fileMenu.add_command(label = "Load Maze", command = lambda: print("Load Maze"))
		fileMenu.add_separator()
		fileMenu.add_command(label = "Save Solve", command = lambda: print("Save Solve"))
		fileMenu.add_command(label = "Load Solve", command = lambda: print("Load Solve"))
		menubar.add_cascade(label = "File", menu = fileMenu)

		generatorMenu = tk.Menu()
		generatorMenu.add_command(label = "Generate New Maze", command = lambda: print("Generate New Maze"))
		generatorMenu.add_command(label = "Edit Generation Settings", command = lambda: print("Edit Generation Settings"))
		menubar.add_cascade(label = "Generate", menu = generatorMenu)

		solverMenu = tk.Menu()
		solverMenu.add_command(label = "Solve Current Maze", command = lambda: print("Solve Current Maze"))
		solverMenu.add_command(label = "Edit Solve Settings", command = lambda: self.parent.changeFrame(SettingsMenu))
		menubar.add_cascade(label = "Solve", menu = solverMenu)

	def loadMaze(self):
		# TODO Load in maze using user defined settings.
		# This includes creating maze then giving to generator before drawing.
		# For now, no generation occurs.

		self.maze = maze.Maze(self, canvasSize = self.parent.screenSize)
		self.maze.canvas.grid(row = 0, column = 1)

class SettingsMenu(tk.Frame):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

		self.buttonImage = tk.PhotoImage(file = "assets/home_button.png")

		#xScale = self.buttonImage.width() / 

		self.homeButton = tk.Button(self, image = self.buttonImage, command = lambda: parent.changeFrame(HomeScreen))
		self.homeButton.grid(row = 0, column = 0)


	
