#Internal Imports
import maze

#External imports
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from fractions import Fraction

# TOOD -- Add confirmation of reset for maze.


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
		self.frames[GenerationSettings] = GenerationSettings(self)
		self.frames[GenerationSettings].grid(row = 0, column = 0)
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
		self.loadMaze(51)


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
		generatorMenu.add_command(label = "Regenerate Maze", command = self.generateMaze)
		generatorMenu.add_command(label = "Edit Generation Settings", command = lambda: self.parent.changeFrame(GenerationSettings))
		menubar.add_cascade(label = "Generate", menu = generatorMenu)

		solverMenu = tk.Menu(menubar, tearoff = False)
		solverMenu.add_command(label = "Solve Current Maze", command = lambda: print("Solve Current Maze"))
		solverMenu.add_command(label = "Edit Solve Settings", command = lambda: print("Edit Solve Settings"))
		menubar.add_cascade(label = "Solve", menu = solverMenu)

		editMenu = tk.Menu(menubar, tearoff = False)
		self.editMode = tk.BooleanVar()
		editMenu.add_checkbutton(label = "Toggle edit mode", onvalue = True, offvalue = False, variable = self.editMode)
		menubar.add_cascade(label = "Edit", menu = editMenu)

	def loadMaze(self, size):
		"""
		Load in a blank Maze object
		Arguments:
		size -- The width and height of the new Maze
		"""
		self.maze = maze.Maze(self, canvasSize = self.parent.screenSize, size = size)
		self.maze.canvas.grid(row = 0, column = 1)

	def resetMaze(self, size):
		self.maze.canvas.destroy()
		self.loadMaze(size)

	def generateMaze(self):
		settings = self.parent.frames[GenerationSettings]

		algorithm = settings.algorithmChoice.get()

		if algorithm == "Recursive Backtracker":
			from generators.recursivebacktracker import Generator
		else:
			print("No item selected")
			return

		size = int(settings.mazeSize.get())

		if not (mb.askyesno(self.parent.title, "Are you sure you want to generate a new maze?")):
			return

		self.resetMaze(size)

		Generator(self.maze)



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

		self.TitleStyle = ttk.Style()
		self.TitleStyle.configure("Title.TLabel", font = ("Helvetica", 30))
		
class GenerationSettings(SettingsMenu):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		ttk.Label(self, text = "Generation Algorithm", style = "Title.TLabel").grid(row = 1, column = 0, pady = 20)

		algorithms = (	"Recursive Backtracker",
						"Prims Algorithm",
						"Kruskals Algorithm"
					)

		self.algorithmChoice = ttk.Combobox(self, values = algorithms, state = "readonly", width = 20, font = ("arial", 14))
		self.algorithmChoice.set("Recursive Backtracker")
		self.algorithmChoice.grid(row = 2, column = 0)

		ttk.Label(self, text = "Maze Size", style = "Title.TLabel").grid(row = 3, column = 0, pady = 20)

		self.mazeSize = ttk.Scale(self, from_ = 21, to = 201, orient = tk.HORIZONTAL, value = 51, command = self.oddOnly, length = 200)
		self.mazeSize.grid(row = 4, column = 0)

		self.mazeSizeLabel = ttk.Label(self, text = 51, style = "Small.TLabel")
		self.mazeSizeLabel.grid(row = 5, column = 0)

		self.buttonStyle = ttk.Style()
		self.buttonStyle.configure("Big.TButton", height = 2, width = 20, font = ("arial", 15))

		self.generateButton = ttk.Button(self, text = "Generate Maze", command = self.generateMaze)
		self.generateButton.grid(row = 100, column = 0)



	def oddOnly(self, event):
		value = self.mazeSize.get()
		if (int(value) != value):
			if int(value) % 2 == 0:
				value += 1
			self.mazeSize.set(int(value))

		self.mazeSizeLabel.config(text = int(value))


	def generateMaze(self):
		self.parent.changeFrame(HomeScreen)
		self.parent.frames[HomeScreen].generateMaze()