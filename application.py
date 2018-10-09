#Internal Imports
import maze

#External imports
# Tkinter, ttk and messagebox libraries used for GUI aspects of the program.
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from tkinter.filedialog import asksaveasfilename, askopenfilename
# Import regex for checking filenames.
import re
# OS library used for file paths and getting current directories.
import os

"""
BUGS:
        MAJOR - Editing when a maze is loaded in is broken as f-ck.
        MINOR - Slight visual blank area at bottom of maze on occasion.    
"""

class Application(tk.Tk):
        """
        Class used to house the GUI aspects of the application.
        """
        def __init__(self, *args, **kwargs):
                super().__init__()

                # Set the title and icon of our application.
                self.title("PathFinding")
                self.title = "PathFinding"

                self.tk_setPalette(background="#D9D9D9", foreground="#000000")
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

                # Create a dictionary for the side menus and populate it.
                self.menus = {}

                # Load in all menus and put them in our dictionary.
                self.menus[SolverSettings] = SolverSettings(self)
                self.menus[GenerationSettings] = GenerationSettings(self)

                # Load Maze 
                self.loadMaze()

                # Load in Top Menu
                self.loadTopMenu()

                # Bind for Easter Egg
                self.EESequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]
                self.EEPos = 0
                self.bind("<Key>", self.keyPress)

        def keyPress(self, event):
                if event.keycode == self.EESequence[self.EEPos]:
                        self.EEPos += 1
                else:
                        self.EEPos = 0

                if self.EEPos == len(self.EESequence):
                        mb.showinfo(self.title, "31.9505° S, 115.8605° E")
                        self.EEPos = 0

        def loadStyles(self):
                # Load a style object
                self.style = ttk.Style()

                # Set the default background for all widgets to a specific colour
                self.style.configure(".", background = "#d9d9d9")
                
                # Load in styles for any situation we need.
                self.style.configure("Header.TLabel", font = ("Helvetica", 15, "italic"))

                self.style.configure("Title.TLabel", font = ("Helvetica", 30, "bold italic"))

                self.style.configure("Footer.TLabel", font = ("Times", 12, "roman"))

                self.style.configure("Settings.TButton", height = 2, width = 20, font = ("arial", 15))


        def loadTopMenu(self):
                """
                Method for loading in the top menu of the screen.
                """
                self.menubar = tk.Menu(self)

                self.menubar.add_command(label = "Home", command = lambda: self.changeFrame(HomeScreen))

                fileMenu = tk.Menu(self.menubar, tearoff = False)
                fileMenu.add_command(label = "Save Maze", command = self.saveMazeFile)
                fileMenu.add_command(label = "Load Maze", command = self.loadMazeFile)
                fileMenu.add_separator()
                fileMenu.add_command(label = "Save Solve", command = lambda: print())
                fileMenu.add_command(label = "Load Solve", command = lambda: print("Load Solve"))
                self.menubar.add_cascade(label = "File", menu = fileMenu)

                self.menubar.add_command(label = "Generate Maze", command = lambda: self.changeMenu(GenerationSettings))

                self.menubar.add_command(label = "Solve Current Maze", command = lambda: self.changeMenu(SolverSettings))

                editMenu = tk.Menu(self.menubar, tearoff = False)
                editMenu.add_checkbutton(label = "Toggle edit mode", onvalue = True, offvalue = False, variable = self.frames[MazeScreen].editMode)
                
                self.menubar.add_cascade(label = "Edit", menu = editMenu)
                

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
                if newFrame == HomeScreen:
                        self.changeMenu(None)
                        emptyMenu = tk.Menu(self)
                        self.config(menu = emptyMenu)
                else:
                        self.config(menu = self.menubar)
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
                        frame.grid(row = 0, column = 1, sticky = "NE")

        def saveMazeFile(self):
                """
                Method used to translate a maze object into a binary file.
                Displays a dialog box for user to select file path and translates object.
                Arguments:
                        NONE
                """
                # Open a file save dialog for the user. 
                filePath = asksaveasfilename(initialdir = "./saves/", filetypes = [('MAZ Files', '.maz')], title = "Where to save file?")
                # If the file path fits the form of '*.maz' then save it. Otherwise don't.
                if re.match(".+(.maz)\\b",filePath) != None:
                        self.maze.toFile(filePath)
                elif filePath != "":
                        mb.showerror(self.title, "Please ensure the filePath fits the form of '*.maz'")

        def loadMazeFile(self):
                """
                Method used to load a maze object from a binary file.
                Displays a dialog box for user to select file path and translates object.
                Arguments:
                        NONE
                """
                # Display a dialog box to get file path.
                filePath = askopenfilename(initialdir = "./saves/", filetypes = [('MAZ Files', '.maz')], title = "Please select a .MAZ file")
                # Ensure the filepath has a .maz suffix and if not, show an error.
                if re.match(".+(.maz)\\b",filePath) != None:
                        self.maze.fromFile(filePath)
                        self.changeFrame(MazeScreen)
                elif filePath != "":
                        mb.showerror(self.title, "That is not a valid filename.\nPlease ensure the filePath fits the form of '*.maz'")

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
                # Destroy the current canvas of the maze then load a new one.
                self.maze = None
                self.loadMaze(size)

        def generateMaze(self):
                """
                Method used to generate a maze based on current settings from the settings menu.
                Arguments:
                        NONE
                """
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
                """
                Method used to solve a maze based on current settings from the settings menu.
                Arguments:
                        NONE
                """
                # Copy the GenerationSettings for easier referencing.
                settings = self.menus[SolverSettings]

                # Get the algorithm choice and load that algorithms Generator.
                algorithm = settings.solverChoice.get()

                if algorithm == "Recursive Backtracker":
                        from solvers.recursivebacktracker import Solver
                else:
                        print("No item selected")
                        return

                autorun = settings.autoStepEnabled

                try:
                        delay = int(settings.autoStepDelay.get())
                except ValueError:
                        mb.showerror(self.title, "Please enter a valid integer in the auto step delay")
                        return

                # Use the solver to solve our maze.
                Solver(self.maze, autorun = autorun, delay = delay)

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
                """
                Method used to load the GUI aspects of the homescreen.
                Arguments:
                        NONE
                """
                self.titleImage = tk.PhotoImage(file = "assets/homeTitle.png")
                self.title = ttk.Label(self, image = self.titleImage, text = "Path Finding Thing", style = "Title.TLabel")
                self.title.grid(row = 0, column = 0, pady = 50)

                self.settingsImage = tk.PhotoImage(file = "assets/homeSettings.png")
                self.settingsButton = tk.Button(self, image = self.settingsImage, command = lambda: self.parent.changeMenu(GenerationSettings), borderwidth = 0)
                self.settingsButton.grid(row = 0, column = 0, sticky = "NE")

                self.generateImage = tk.PhotoImage(file = "assets/homeGenerate.png")
                self.generateButton = tk.Button(self, image = self.generateImage, command = self.generateMaze, borderwidth = 0)
                self.generateButton.grid(row = 1, column = 0, pady = 30)

                self.loadImage = tk.PhotoImage(file = "assets/homeLoad.png")
                self.loadButton = tk.Button(self, image = self.loadImage, command = self.parent.loadMazeFile, borderwidth = 0)
                self.loadButton.grid(row = 2, column = 0, pady = 30)

                self.footer = ttk.Label(self, text = "Created By Felix J. Randle", style = "Footer.TLabel")
                self.footer.grid(row = 10, column = 0, sticky = "S", pady = 50)

        def generateMaze(self):
                """
                Method used to generate a maze and change the screen.
                Arguments:
                        NONE
                """
                self.parent.generateMaze()
                self.parent.changeFrame(MazeScreen)


class MazeScreen(tk.Frame):
        def __init__(self, parent):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                super().__init__()
                self.parent = parent

                self.editMode = tk.BooleanVar()

class SettingsMenu(tk.Frame):
        def __init__(self, parent):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen
                """
                super().__init__()
                self.parent = parent

                self.exitImage = tk.PhotoImage(file = "assets/settingsExit.png")
                self.exitButton = tk.Button(self, image = self.exitImage, command = lambda: parent.changeMenu(None), borderwidth = 0)
                self.exitButton.grid(row = 0, column = 100, sticky = "NE")

        def loadTitle(self, source):
                """
                Load a title image from the given source.
                """
                self.titleImage = tk.PhotoImage(file = source)

                tk.Label(self, image = self.titleImage).grid(row = 0, column = 0, pady = 50, padx = 40)

class GenerationSettings(SettingsMenu):
        def __init__(self, parent):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                super().__init__(parent)
                self.parent = parent

                # Load a title button with the given file
                self.loadTitle("assets/generationTitle.png")

                ttk.Label(self, text = "Generation Algorithm", style = "Header.TLabel").grid(row = 1, column = 0, pady = 20)

                algorithms = (  "Recursive Backtracker",
                                "Prims Algorithm",
                                "Kruskals Algorithm"
                                        )

                self.algorithmChoice = ttk.Combobox(self, values = algorithms, state = "readonly", width = 20, font = ("arial", 14))
                self.algorithmChoice.set(algorithms[0])
                self.algorithmChoice.grid(row = 2, column = 0, pady = 20)

                ttk.Label(self, text = "Maze Size", style = "Header.TLabel").grid(row = 3, column = 0, pady = 20)

                self.mazeSize = ttk.Scale(self, from_ = 21, to = 201, orient = tk.HORIZONTAL, value = 51, command = self.oddOnly, length = 200)
                self.mazeSize.grid(row = 4, column = 0, pady = 20)

                self.mazeSizeLabel = ttk.Label(self, text = 51, style = "Header.TLabel")
                self.mazeSizeLabel.grid(row = 5, column = 0, pady = 20)
                
                self.generationButtonImage = tk.PhotoImage(file = "assets/generationButton.png")
                self.generateButton = tk.Button(self, image = self.generationButtonImage, command = self.generateMaze, borderwidth = 0)
                self.generateButton.grid(row = 100, column = 0, pady = 20)



        def oddOnly(self, event):
                value = self.mazeSize.get()
                if (int(value) != value):
                        if int(value) % 2 == 0:
                                value += 1
                        self.mazeSize.set(int(value))

                self.mazeSizeLabel.config(text = int(value))


        def generateMaze(self):
                self.parent.changeFrame(MazeScreen)
                self.parent.generateMaze()

class SolverSettings(SettingsMenu):
        def __init__(self, parent):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                super().__init__(parent)

                self.loadTitle("assets/solveTitle.png")

                solvers = (     
                                "Recursive Backtracker",
                                )

                self.solverChoice = ttk.Combobox(self, values = solvers, state = "readonly", width = 20, font = ("arial", 14))
                self.solverChoice.set(solvers[0])
                self.solverChoice.grid(row = 2, column = 0, pady = 20)

                self.autoStepEnabled = False
                self.autoStepButton = ttk.Button(self, text = "Enable AutoStep", style = "Settings.TButton", command = self.toggleAutoStep)
                self.autoStepButton.grid(row = 3, column = 0, pady = 20)

                ttk.Label(self, text = "Auto Step Delay (S)", style = "Header.TLabel").grid(row = 4, column = 0, pady = 5)

                self.autoStepDelay = ttk.Entry(self, width = 10, validate = "focusout", validatecommand = self.validateDelayEntry)
                self.autoStepDelay.grid(row = 5, column = 0, pady = 20)

                self.solveButtonImage = tk.PhotoImage(file = "assets/solveButton.png")
                self.solveButton = tk.Button(self, image = self.solveButtonImage, command = self.solveMaze, borderwidth = 0)
                self.solveButton.grid(row = 100, column = 0, pady = 20)

        def toggleAutoStep(self):
                if self.autoStepEnabled:
                        self.autoStepButton["text"] = "Enable AutoStep"
                        self.autoStepEnabled = False
                else:
                        self.autoStepButton["text"] = "Disable AutoStep"
                        self.autoStepEnabled = True

        def validateDelayEntry(self):
                value = self.autoStepDelay.get()
                try:
                        int(value)
                        return True
                except ValueError:
                        return False

        def solveMaze(self):
                self.parent.solveMaze()
                
                        
