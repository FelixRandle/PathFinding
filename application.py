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
                self.iconbitmap(cd+"/assets/maze.ico")

                # Calculate the size of our application based on the users screensize.
                # We ensure this is odd as even numbers can cause rendering issues.
                self.screenSize = int(self.winfo_screenheight() * 0.7)
                if self.screenSize % 2 == 0:
                        self.screenSize += 1
                        
                # Stop the user from resizing the screen.
                self.minsize(width = self.screenSize - 5, height = self.screenSize - 5)
                self.resizable(False, False)

                # Create a dictionary for the screen tabs and populate it.
                self.frames = {}

                # Load in all tabs and put them in our dictionary.
                self.frames[MazeScreen] = MazeScreen(self)
                self.frames[GenerationSettings] = GenerationSettings(self)
                self.frames[SolverSettings] = SolverSettings(self)
                # Load the homescreen
                self.changeFrame(MazeScreen)

        def changeFrame(self, newFrame):
                """
                Internal method for changing the current frame shown on screen.
                Arguments:
                newFrame -- The frame to change to
                """
                #Loop through all frames that are currently on the grid and remove them from the grid
                for frame in self.grid_slaves():
                        frame.grid_forget()
                #Load the new frame
                frame = self.frames[newFrame]
                #Place our new frame onto the grid
                frame.grid(row = 0, column = 0)

class MazeScreen(tk.Frame):
        def __init__(self, parent):
                super().__init__()
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                self.parent = parent

                self.loadTopMenu()
                self.loadMaze(51)


        def loadTopMenu(self):
                """
                Method for loading in the top menu of the screen.
                """
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
                solverMenu.add_command(label = "Solve Current Maze", command = self.solveMaze)
                solverMenu.add_command(label = "Edit Solve Settings", command = lambda: self.parent.changeFrame(SolverSettings))
                menubar.add_cascade(label = "Solve", menu = solverMenu)

                editMenu = tk.Menu(menubar, tearoff = False)
                self.editMode = tk.BooleanVar()
                editMenu.add_checkbutton(label = "Toggle edit mode", onvalue = True, offvalue = False, variable = self.editMode)
                menubar.add_cascade(label = "Edit", menu = editMenu)

        def loadMaze(self, size):
                """
                Load in a blank Maze object.
                Arguments:
                size -- The width and height of the new Maze
                """
                self.maze = maze.Maze(self, canvasSize = self.parent.screenSize, size = size)
                self.maze.canvas.grid(row = 0, column = 1)

        def resetMaze(self, size):
                self.maze.canvas.destroy()
                self.loadMaze(size)

        def generateMaze(self):
                # Copy the GenerationSettings for easier referencing.
                settings = self.parent.frames[GenerationSettings]

                # Get the algorithm choice and load that algorithms Generator.
                algorithm = settings.algorithmChoice.get()

                if algorithm == "Recursive Backtracker":
                        from generators.recursivebacktracker import Generator
                else:
                        print("No item selected")
                        return

                # Load in the size of the maze from settings
                size = int(settings.mazeSize.get())

                # Ask the user for conformation to ensure they don't overwrite a maze they're working on.
                if not (mb.askyesno(self.parent.title, "Are you sure you want to generate a new maze?")):
                        return

                # Reset the current maze and generate a new one from the loaded generator.
                self.resetMaze(size)

                Generator(self.maze)

        def solveMaze(self):
                # Copy the GenerationSettings for easier referencing.
                settings = self.parent.frames[SolverSettings]

                # Get the algorithm choice and load that algorithms Generator.
                algorithm = settings.solverChoice.get()

                if algorithm == "Recursive Backtracker":
                        from solvers.recursivebacktracker import Solver
                else:
                        print("No item selected")
                        return

                Solver(self.maze)

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

                #self.autoStepButton = ttk.Button(self, text = "Enable AutoStep", command = self.toggleAutoStep)

                        
