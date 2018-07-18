#Internal Imports
import maze

#External imports
import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.frames = {}

		frame = HomeScreen(self)
		self.frames[HomeScreen] = frame
		frame.grid(row = 0, column = 0)

		self.changeFrame(HomeScreen)

	def changeFrame(self, newFrame):
		frame = self.frames[newFrame]
		frame.tkraise()

class HomeScreen(tk.Frame):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

		self.loadTopMenu()


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
		solverMenu.add_command(label = "Edit Solve Settings", command = lambda: print("Edit Solve Settings"))
		menubar.add_cascade(label = "Solve", menu = solverMenu)



	
