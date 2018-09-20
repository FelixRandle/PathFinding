#Internal Imports
import maze

#External imports
# Tkinter, ttk and messagebox libraries used for GUI aspects of the program.
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
# Fraction library used for resizing images in windows to scale nicely.
from fractions import Fraction
# OS library used for file paths and getting current directories.
import os


class Application(tk.Tk):
        """
        Class used to house the GUI aspects of the application.
        """
        def __init__(self, *args, **kwargs):
                super().__init__()

                # Set the title and icon of our application.
                self.title("PathFinding")
                self.title = "PathFinding"
                # Get the current directory.
                cd = os.getcwd()
                # Set our programs icon for the top left.
                # Disabled for Linux development. Re-enable for deployment.
                #self.iconbitmap(cd+"/assets/maze.ico")
                        
                # Stop the user from resizing the screen.
                self.screenSize = 750
                # Take away 5 to account for border of screen so maze fits properly
                self.minsize(width = self.screenSize - 5, height = self.screenSize - 5)
                self.resizable(False, False)

                # Create all styles to be used for our GUI.
                self.loadStyles()

                # Ensure all placed items are centered.
                self.grid_columnconfigure(0, weight = 1)

                # Create a dictionary for the screen tabs and populate it.
                self.frames = {}

                # Load in all tabs and put them in our dictionary.
                self.frames[HomeScreen] = HomeScreen(self)
                self.frames[MazeScreen] = MazeScreen(self)

                # Load the homescreen
                self.changeFrame(HomeScreen)

                self.loadTopMenu()

                # Create a dictionary for the side menus and populate it.
                self.menus = {}

                # Load in all menus and put them in our dictionary.
                #self.menus[GeneratorMenu] = GeneratorMenu(self)
                self.menus[SolverSettings] = SolverSettings(self)
                self.menus[GenerationSettings] = GenerationSettings(self)

                # Load Maze 
                self.loadMaze()

        def loadStyles(self):
                # Load a style object
                self.style = ttk.Style()

                # Load in styles for any situation we need.

                self.style.configure("Title.TLabel", font = ("Helvetica", 30, "bold italic"))

                self.style.configure("Footer.TLabel", font = ("Times", 12, "roman"))

        def loadTopMenu(self):
                """
                Method for loading in the top menu of the screen.
                """
                menubar = tk.Menu(self)
                self.config(menu = menubar)

                fileMenu = tk.Menu(menubar, tearoff = False)
                fileMenu.add_command(label = "Save Maze", command = lambda: print("Save Maze"))
                fileMenu.add_command(label = "Load Maze", command = lambda: print("Load Maze"))
                fileMenu.add_separator()
                fileMenu.add_command(label = "Save Solve", command = lambda: print("Save Solve"))
                fileMenu.add_command(label = "Load Solve", command = lambda: print("Load Solve"))
                menubar.add_cascade(label = "File", menu = fileMenu)

                menubar.add_command(label = "Generate Maze", command = lambda: self.changeMenu(GenerationSettings))

                menubar.add_command(label = "Solve Current Maze", command = lambda: self.changeMenu(SolverSettings))

                editMenu = tk.Menu(menubar, tearoff = False)
                self.editMode = tk.BooleanVar()
                editMenu.add_checkbutton(label = "Toggle edit mode", onvalue = True, offvalue = False, variable = self.editMode)
                menubar.add_cascade(label = "Edit", menu = editMenu)


        def changeFrame(self, newFrame):
                """
                Internal method for changing the current frame shown on screen.
                Arguments:
                        newFrame -- The frame to change to
                """
                #Loop through all frames that are currently on the grid and remove them from the grid
                for frame in self.grid_slaves():
                        if frame.grid_info()["column"] == 0:
                                frame.grid_forget()
                #Load the new frame
                frame = self.frames[newFrame]
                #Place our new frame onto the grid
                frame.grid(row = 0, column = 0)

        def changeMenu(self, newMenu):
                """
                Internal method for changing the current frame shown on screen.
                Arguments:
                        newFrame -- The frame to change to
                """
                #Loop through all frames that are currently on the grid and remove them from the grid
                for frame in self.grid_slaves():
                        if frame.grid_info()["column"] == 1:
                                frame.grid_forget()

                if newMenu != None:
                        #Load the new frame
                        frame = self.menus[newMenu]
                        #Place our new frame onto the grid
                        frame.grid(row = 0, column = 1, sticky = "N")

        def loadMaze(self, size = 51):
                """
                Load in a blank Maze object.
                Arguments:
                        size -- The width and height of the new Maze
                """
                # Load the frame we are going to attach it to.
                frame = self.frames[MazeScreen]
                self.maze = maze.Maze(frame, canvasSize = self.screenSize, size = size)
                self.maze.canvas.grid(row = 0, column = 0)

        def resetMaze(self, size):
                """
                Destroy old maze and load a new maze with the given size
                Arguments:
                        size -- The width and height of the new maze.
                """
                self.maze.canvas.destroy()
                self.loadMaze(size)

        def generateMaze(self):
                # Copy the GenerationSettings for easier referencing.
                settings = self.menus[GenerationSettings]

                # Get the algorithm choice and load that algorithms Generator.
                algorithm = settings.algorithmChoice.get()

                if algorithm == "Recursive Backtracker":
                        from generators.recursivebacktracker import Generator
                else:
                        print("No item selected")
                        return

                # Load in the size of the maze from settings
                size = int(settings.mazeSize.get())

                # Reset the current maze and generate a new one from the loaded generator.
                self.resetMaze(size)

                # Use the generator to create a new maze.
                Generator(self.maze)

        def solveMaze(self):
                # Copy the GenerationSettings for easier referencing.
                settings = self.frames[SolverSettings]

                # Get the algorithm choice and load that algorithms Generator.
                algorithm = settings.solverChoice.get()

                if algorithm == "Recursive Backtracker":
                        from solvers.recursivebacktracker import Solver
                else:
                        print("No item selected")
                        return

                # Use the solver to solve our maze.
                Solver(self.maze)

class HomeScreen(tk.Frame):
        def __init__(self, parent):
                super().__init__()
                """
                Arguments
                        parent -- The parent tkinter object for this screen.
                """
                self.parent = parent

                self.loadGUI()

        def loadGUI(self):
                self.titleImage = tk.PhotoImage(file = "assets/title.png")
                self.title = ttk.Label(self, image = self.titleImage, text = "Path Finding Thing", style = "Title.TLabel")
                self.title.grid(row = 0, column = 0, pady = 50)

                self.settingsImage = tk.PhotoImage(file = "assets/settings.png")
                self.settingsButton = tk.Button(self, image = self.settingsImage, command = lambda: self.parent.changeMenu(GenerationSettings), borderwidth = 0)
                self.settingsButton.grid(row = 0, column = 0, sticky = "NE")

                self.generateImage = tk.PhotoImage(file = "assets/homeGenerate.png")
                self.generateButton = tk.Button(self, image = self.generateImage, command = self.generateMaze, borderwidth = 0)
                self.generateButton.grid(row = 1, column = 0, pady = 30)

                self.loadImage = tk.PhotoImage(file = "assets/homeLoad.png")
                self.loadButton = tk.Button(self, image = self.loadImage, command = lambda: print("Pressed Home"), borderwidth = 0)
                self.loadButton.grid(row = 2, column = 0, pady = 30)

                self.footer = ttk.Label(self, text = "Created By Felix J. Randle", style = "Footer.TLabel")
                self.footer.grid(row = 10, column = 0, sticky = "S", pady = 50)

        def generateMaze(self):
                print("Generating Maze")
                self.parent.generateMaze()
                print("Changing Frame")
                self.parent.changeFrame(MazeScreen)


class MazeScreen(tk.Frame):
        def __init__(self, parent):
                super().__init__()
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                self.parent = parent

class SettingsMenu(tk.Frame):
        def __init__(self, parent):
                super().__init__()
                self.parent = parent

                self.exitImage = tk.PhotoImage(file = "assets/exit.png")
                self.exitButton = tk.Button(self, image = self.exitImage, command = lambda: parent.changeMenu(None), borderwidth = 0)
                self.exitButton.grid(row = 0, column = 0, sticky = "NE")

        def loadTitle(self, source):
                """
                Load a title image from the given source.
                """
                self.titleImage = tk.PhotoImage(file = source)

                tk.Label(self, image = self.titleImage).grid(row = 0, column = 0, pady = 15)

class GenerationSettings(SettingsMenu):
        def __init__(self, parent):
                super().__init__(parent)
                self.parent = parent

                self.loadTitle("assets/generationTitle.png")

                ttk.Label(self, text = "Generation Algorithm", style = "Title.TLabel").grid(row = 1, column = 0, pady = 20)

                algorithms = (  "Recursive Backtracker",
                                "Prims Algorithm",
                                "Kruskals Algorithm"
                                        )

                self.algorithmChoice = ttk.Combobox(self, values = algorithms, state = "readonly", width = 20, font = ("arial", 14))
                self.algorithmChoice.set(algorithms[0])
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

class SolverSettings(SettingsMenu):
        def __init__(self, parent):
                super().__init__(parent)

                ttk.Label(self, text = "Solver Algorithm", style = "Title.TLabel").grid(row = 1, column = 0, pady = 20)

                solvers = (
                                        "Recursive Backtracker",
                                )

                self.solverChoice = ttk.Combobox(self, values = solvers, state = "readonly", width = 20, font = ("arial", 14))
                self.solverChoice.set(solvers[0])
                self.solverChoice.grid(row = 2, column = 0)

                self.autoStepButton = ttk.Button(self, text = "Enable AutoStep", command = lambda: print("TOggle auto"))

                        
