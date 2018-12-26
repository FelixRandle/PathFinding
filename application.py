#Internal Imports
import maze
import tkColourPicker
from customFont import loadFont
from database import Database

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
import sys

"""
BUGS:
        MAJOR - Editing when a maze is loaded in is broken as f-ck.
        MINOR - Slight visual blank area at bottom of maze on occasion.
"""
import pickle

"""
BUGS:
        MAJOR - When solving maze, clicking generate maze will change view but continue to solve maze.
        MINOR - Slight visual blank area at bottom of maze on occasion.
"""

"""
TODO:
        Help Button, HOME PAGE, Top left
        WHEN MAZE LOADED, CHANGE APP Title TO REFLECT FILE
"""

def getResourcePath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativePath)
    return os.path.join(os.path.abspath("."), relativePath)

class Application(tk.Tk):
        """
        Class used to house the GUI aspects of the application.
        """
        def __init__(self, *args, **kwargs):
                super().__init__()

                # Set the Title and icon of our application.
                self.title("PathFinding")
                self.Title = "PathFinding"

                # Set default background and foreground colours for all widgets.
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
                self.frames = dict()

                # Load in all tabs and put them in our dictionary.
                self.frames[HomeScreen] = HomeScreen(self)
                self.frames[MazeScreen] = MazeScreen(self)

                # Load the homescreen
                self.changeFrame(HomeScreen)

                # Create a dictionary for the side menus and populate it.
                self.menus = dict()

                # Load in all menus and put them in our dictionary.
                self.menus[MenuList] = MenuList(self)
                self.menus[GeneralSettings] = GeneralSettings(self)
                self.menus[SolverSettings] = SolverSettings(self)
                self.menus[GenerationSettings] = GenerationSettings(self)
                self.menus[SolverMenu] = SolverMenu(self)

                # Load Maze
                self.loadMaze()

                # Load in Top Menu
                self.loadTopMenu()

                # Load in Database
                self.db = Database(maze.tileColours)

                # Add current user
                self.db.addUser(os.getlogin())

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
                        mb.showinfo(self.Title, u"Found it!\n31.9505\u00B0 S, 115.8605\u00B0 E")
                        self.EEPos = 0


        def loadStyles(self):
                # Load in a custom font
                loadFont("assets/fonts/AlegreyaSansSC-Regular.ttf")
                # Load a style object
                self.style = ttk.Style()

                # Set the default background for all widgets to a specific colour
                self.style.configure(".", background = "#d9d9d9")


                # Load in styles for any situation we need.
                self.style.configure("Header.TLabel", font = ("Helvetica", 15, "italic"))

                # Load in styles for any situation we need.
                self.style.configure("Header.TLabel", font = ("Alegreya Sans SC Regular", 15, "bold italic"))

                self.style.configure("Subheading.TLabel", font = ("Alegreya Sans SC Regular", 13))

                self.style.configure("Footer.TLabel", font = ("Alegreya Sans SC Regular", 12, "roman"))

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
                fileMenu.add_command(label = "Save Solve", command = lambda: print("Save Solve"))
                fileMenu.add_command(label = "Load Solve", command = lambda: print("Load Solve"))

                self.menubar.add_cascade(label = "File", menu = fileMenu)

                self.menubar.add_command(label = "Generate Maze", command = self.generateMaze)

                # If we are currently solving a maze, this brings up the Solver Menu, otherwise it solves the Maze.
                self.menubar.add_command(label = "Solve Current Maze", command = lambda: self.changeMenu(SolverMenu) if self.maze.solving else self.solveMaze())

                editMenu = tk.Menu(self.menubar, tearoff = False)
                editMenu.add_checkbutton(label = "Toggle edit mode", onvalue = True, offvalue = False, variable = self.frames[MazeScreen].editMode)

                self.menubar.add_cascade(label = "Edit", menu = editMenu)
                self.menubar.add_command(label = "Settings", command = lambda: self.changeMenu(MenuList))


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
                frame.grid(row = 0, column = 0, sticky = "N")


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
                filePath = asksaveasfilename(initialdir = "./saves/", filetypes = [('MAZ Files', '.maz')], Title = "Where to save file?")
                print(filePath)

                # If the file path fits the form of '*.maz' then save it. Otherwise don't.
                if re.match(".+(?i)(.maz)\\b",filePath) != None:
                        self.maze.toFile(filePath)
                else:
                        self.maze.toFile(filePath+".maz")
                        # mb.showerror(self.Title, "Please ensure the filePath fits the form of '*.maz'")


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
                if re.match(".+(?i)(.maz)\\b",filePath) != None:
                        self.maze.fromFile(filePath)
                        self.changeFrame(MazeScreen)
                        self.title("PathFinding | {}".format(filePath))
                elif filePath != "":
                        mb.showerror(self.Title, "That is not a valid filename.\nPlease ensure the filePath fits the form of '*.maz'")


        def loadMaze(self, size = 51):
                """
                Load in a blank Maze object.
                Arguments:
                        size -- The width and height of the new Maze
                """
                # Load the frame we are going to attach it to.
                frame = self.frames[MazeScreen]
                self.maze = None
                self.maze = maze.Maze(frame, canvasSize = self.screenSize, size = size)
                self.maze.canvas.grid(row = 0, column = 0)


        def generateMaze(self):
                """
                Method used to generate a maze based on current settings from the settings menu.
                Arguments:
                        NONE
                """
                if self.maze.solving:
                        mb.showerror("ERROR", "Maze already being solved")
                        return
                # Copy the GenerationSettings for easier referencing.
                settings = self.menus[GenerationSettings]

                # Get the algorithm choice and load that algorithms Generator.
                algorithm = settings.algorithmChoice.get()

                if algorithm == "Recursive Backtracker":
                        from generators.recursivebacktracker import Generator
                elif algorithm == "Kruskals Algorithm":
                        from generators.kruskals import Generator
                else:
                        print("No item selected")
                        return

                # Load in the size of the maze from settings
                size = int(settings.mazeSize.get())

                # Reset the current maze and generate a new one from the loaded generator.
                self.loadMaze(size)
                Generator(self.maze)

                self.title("PathFinding")


        def solveMaze(self):
                """
                Method used to solve a maze based on current settings from the settings menu.
                Arguments:
                        NONE
                """
                if self.maze.solving:
                        mb.showerror("ERROR", "Maze already being solved")
                        return

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

                delay = 1 / settings.speed.get()


                self.changeMenu(SolverMenu)
                # Use the solver to solve our maze.
                self.maze.unvisitTiles()
                self.maze.solving = True
                self.solver = Solver(self, self.maze, settings, self.menus[SolverMenu])


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
                self.titleImage = tk.PhotoImage(file = getResourcePath("assets/home/title.png"))
                self.title = ttk.Label(self, image = self.titleImage, text = "Path Finding Thing", style = "Title.TLabel")
                self.title.grid(row = 0, column = 0, pady = 50)

                self.settingsImage = tk.PhotoImage(file = getResourcePath("assets/home/settings.png"))
                self.settingsButton = tk.Button(self, image = self.settingsImage, command = lambda: self.parent.changeMenu(GenerationSettings), borderwidth = 0)
                self.settingsButton.grid(row = 0, column = 0, sticky = "NE")

                self.helpImage = tk.PhotoImage(file = getResourcePath("assets/home/help.png"))
                self.helpButton = tk.Button(self, image = self.helpImage, command = lambda: mb.showinfo("INFO", "Not Done Yet"), borderwidth = 0)
                self.helpButton.grid(row = 0, column = 0, sticky = "NW", pady = 5, padx = 5)

                self.loginButton = tk.PhotoImage(file = getResourcePath("assets/home/login.png"))
                self.userStatusButton = tk.Button(self, image = self.loginButton, command = lambda:mb.showerror("NOT DONE", "Not completed yet"), borderwidth = 0)
                self.userStatusButton.grid(row = 0, column = 0, sticky = "N", pady = 5)

                self.generateImage = tk.PhotoImage(file = getResourcePath("assets/home/generate.png"))
                self.generateButton = tk.Button(self, image = self.generateImage, command = self.generateMaze, borderwidth = 0)
                self.generateButton.grid(row = 1, column = 0, pady = 30)

                self.loadImage = tk.PhotoImage(file = getResourcePath("assets/home/load.png"))
                self.loadButton = tk.Button(self, image = self.loadImage, command = self.parent.loadMazeFile, borderwidth = 0)
                self.loadButton.grid(row = 2, column = 0, pady = 30)

                self.grid_rowconfigure(10, weight=100)

                self.footer = ttk.Label(self, text = "Created By Felix J. Randle", style = "Footer.TLabel")
                self.footer.grid(row = 10, column = 0, sticky = "S", pady=(80,0))


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


class MenuList(tk.Frame):
        def __init__(self, parent):
                super().__init__()
                self.parent = parent

                self.loadWidgets()


        def loadWidgets(self):
                self.exitImage = tk.PhotoImage(file = getResourcePath("assets/settings/exit.png"))
                self.exitButton = tk.Button(self, image = self.exitImage, command = lambda: self.parent.changeMenu(None), borderwidth = 0)
                self.exitButton.grid(row = 0, column = 0, sticky = "NE", pady = 5, padx = 5)

                self.GenerationSettingsIco = tk.PhotoImage(file = getResourcePath("assets/settings/generationTitle.png"))
                tk.Button(self, image = self.GenerationSettingsIco, borderwidth = 0, command = lambda: self.parent.changeMenu(GeneralSettings)).grid(row = 0, column = 0, pady = 70, padx = 40)

                self.SolverSettingsIcon = tk.PhotoImage(file = getResourcePath("assets/settings/solverTitle.png"))
                tk.Button(self, image = self.SolverSettingsIcon, borderwidth = 0, command = lambda: self.parent.changeMenu(SolverSettings)).grid(row = 5, column = 0, pady = 70, padx = 40)

                self.GenerationSettingsIcon = tk.PhotoImage(file = getResourcePath("assets/settings/generationTitle.png"))
                tk.Button(self, image = self.GenerationSettingsIcon, borderwidth = 0, command = lambda: self.parent.changeMenu(GenerationSettings)).grid(row = 10, column = 0, pady = 70, padx = 40)


class SettingsMenu(tk.Frame):
        def __init__(self, parent, back = True):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen
                """
                super().__init__()
                self.parent = parent

                self.exitImage = tk.PhotoImage(file = getResourcePath("assets/settings/exit.png"))
                if back:
                        self.backImage = tk.PhotoImage(file = getResourcePath("assets/settings/back.png"))
                        self.backButton = tk.Button(self, image = self.backImage, command = lambda: parent.changeMenu(MenuList), borderwidth = 0)
                        self.backButton.grid(row = 0, column = 0, sticky = "NW", pady = 5, padx = 5)

                self.exitImage = tk.PhotoImage(file = getResourcePath("assets/settings/exit.png"))
                self.exitButton = tk.Button(self, image = self.exitImage, command = lambda: parent.changeMenu(None), borderwidth = 0)
                self.exitButton.grid(row = 0, column = 0, sticky = "NE", pady = 5, padx = 5)


        def loadTitle(self, source):
                """
                Load a Title image from the given source.
                """
                self.titleImage = tk.PhotoImage(file = source)

                tk.Label(self, image = self.titleImage).grid(row = 0, column = 0, pady = 50, padx = 40)


class GeneralSettings(SettingsMenu):
        def __init__(self, parent):
                super().__init__(parent)
                self.parent = parent

                self.loadTitle(getResourcePath("assets/settings/generationTitle.png"))

                self.loadWidgets()


        def loadWidgets(self):
                self.frames = {}
                for key, item in maze.tileColours.items():
                        tileName = key.name.replace("_", " ").title()

                        container = tk.Frame(self, width = 200)
                        container.grid(row = key.value + 1, column = 0, pady = 5)

                        title = ttk.Label(container, style = "Header.TLabel", text = tileName)
                        title.grid(row = 0, column = 0, columnspan = 19)

                        fgTitle = ttk.Label(container, style = "Subheading.TLabel", text = "FG :")
                        fgTitle.grid(row = 1, column = 0)

                        fgColour = tkColourPicker.ColourPicker(container, 2, 1, key = key, command = self.setColour, index = 1)
                        fgColour.grid(row = 1, column = 1)
                        fgColour.set(maze.tileColours[key][1])

                        divider = ttk.Label(container, style = "Subheading.TLabel", text = "          ")
                        divider.grid(row = 1, column = 3)

                        bgTitle = ttk.Label(container, style = "Subheading.TLabel", text = "BG :")
                        bgTitle.grid(row = 1, column = 4)

                        bgColour = tkColourPicker.ColourPicker(container, 2, 1, key = key, command = self.setColour, index = 0)
                        bgColour.grid(row = 1, column = 5)
                        bgColour.set(maze.tileColours[key][0])

                self.reloadButton = tk.Button(self, text = "Reload Colours", command = self.updateColours)
                self.reloadButton.grid(row = 100, column = 0)


        def setColour(self, key, newColour, index):
                maze.tileColours[key][index] = newColour

                with open("colours.pckl", "wb") as fileOut:
                        pickle.dump(maze.tileColours, fileOut)


        def updateColours(self):
                for row in self.parent.maze.tiles:
                        for tile in row:
                                tile.updateColour()


class GenerationSettings(SettingsMenu):
        def __init__(self, parent):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                super().__init__(parent)
                self.parent = parent

                # Load a Title button with the given file
                self.loadTitle(getResourcePath("assets/settings/generationTitle.png"))

                self.container = tk.Frame(self)
                self.container.grid(row = 10, column = 0, sticky = "S")

                ttk.Label(self.container, text = "Generation Algorithm", style = "Header.TLabel").grid(row = 1, column = 0, pady = 20)

                generators = (  "Recursive Backtracker",
                                "Prims Algorithm",
                                "Kruskals Algorithm"
                                        )

                self.algorithmChoice = ttk.Combobox(self.container, values = generators, state = "readonly", width = 20, font = ("arial", 14))
                self.algorithmChoice.current(0)
                self.algorithmChoice.grid(row = 2, column = 0, pady = 20)

                ttk.Label(self.container, text = "Maze Size", style = "Header.TLabel").grid(row = 3, column = 0, pady = 20)

                self.mazeSize = ttk.Scale(self.container, from_ = 21, to = 201, orient = tk.HORIZONTAL, value = 51, command = self.oddOnly, length = 200)
                self.mazeSize.grid(row = 4, column = 0, pady = 20)

                self.mazeSizeLabel = ttk.Label(self.container, text = 51, style = "Header.TLabel")
                self.mazeSizeLabel.grid(row = 5, column = 0, pady = 20)


        def oddOnly(self, event):
                value = self.mazeSize.get()
                if (int(value) != value):
                        if int(value) % 2 == 0:
                                value += 1
                        self.mazeSize.set(int(value))

                self.mazeSizeLabel.config(text = int(value))


class SolverSettings(SettingsMenu):
        def __init__(self, parent):
                """
                Arguments:
                        parent -- The parent tkinter object for this screen.
                """
                super().__init__(parent)

                self.loadTitle(getResourcePath("assets/settings/solverTitle.png"))

                solvers = (
                                "Recursive Backtracker",
                                )

                self.solverChoice = ttk.Combobox(self, values = solvers, state = "readonly", width = 20, font = ("arial", 14))
                self.solverChoice.set(solvers[0])
                self.solverChoice.grid(row = 2, column = 0, pady = 20)

                self.autoStepEnabled = True
                self.autoStepButton = ttk.Button(self, text = "Disable AutoStep", style = "Settings.TButton", command = self.toggleAutoStep)
                self.autoStepButton.grid(row = 3, column = 0, pady = 20)

                self.speedsFrame = tk.Frame(self)
                self.speedsFrame.grid(row = 4, column = 0, pady = 20)

                self.speedDisplay = ttk.Label(self.speedsFrame, text="Current Speed: X1", style="Subheading.TLabel")
                self.speedDisplay.grid(row = 0 , column = 0, columnspan = 1000)

                self.speeds = [1, 2, 5, 10, 50, 100]
                self.speedItems = {}

                for speed in self.speeds:
                        image = tk.PhotoImage(file = getResourcePath("assets/speeds/X{}.png".format(speed)))
                        button = tk.Button(self.speedsFrame, image = image, command = lambda x=speed: self.parent.solver.setSpeed(x), borderwidth = 0)
                        button.grid(row = 1, column = speed)

                        self.speedItems.update({speed: {"image": image, "button": button}})

                self.speed = tk.DoubleVar()
                self.speed.set(1)
                self.speed.trace("w", self.updateLabel)


        def toggleAutoStep(self):
                if self.autoStepEnabled:
                        self.autoStepButton["text"] = "Enable AutoStep"
                        self.autoStepEnabled = False
                else:
                        self.autoStepButton["text"] = "Disable AutoStep"
                        self.autoStepEnabled = True


        def setSpeed(self, newSpeed):
                self.speed.set(newSpeed)


        def updateLabel(self, *args):
                self.speedDisplay.config(text = "Current Speed: X{}".format(int(self.speed.get())))
                self.parent.menus[SolverMenu].speedDisplay.config(text = "Current Speed: X{}".format(int(self.speed.get())))


        def solveMaze(self):
                self.parent.solveMaze()


class SolverMenu(SettingsMenu):
        def __init__(self, parent):
                super().__init__(parent, False)

                self.loadTitle(getResourcePath("assets/settings/solverTitle.png"))

                self.autoStepControls = tk.Frame(self)
                self.autoStepControls.grid(row = 1, column = 0)

                buttons = {"playButton" : self.startAutoStep, "pauseButton" : self.stopAutoStep, "stopButton" : self.stopSolve}

                self.play = tk.PhotoImage(file = getResourcePath("assets/solving/playButton.png"))
                self.playButton = tk.Button(self.autoStepControls, image = self.play, command = self.startAutoStep, borderwidth = 0)
                self.playButton.grid(row = 0, column = 0)

                self.pause = tk.PhotoImage(file = getResourcePath("assets/solving/pauseButton.png"))
                self.pauseButton = tk.Button(self.autoStepControls, image = self.pause, command = self.stopAutoStep, borderwidth = 0)
                self.pauseButton.grid(row = 0, column = 1)

                self.stop = tk.PhotoImage(file = getResourcePath("assets/solving/stopButton.png"))
                self.stopButton = tk.Button(self.autoStepControls, image = self.stop, command = self.stopSolve, borderwidth = 0)
                self.stopButton.grid(row = 0, column = 2)

                self.speedsFrame = tk.Frame(self)
                self.speedsFrame.grid(row = 4, column = 0, pady = 20)

                self.speedDisplay = ttk.Label(self.speedsFrame, text="Current Speed: X1", style="Subheading.TLabel")
                self.speedDisplay.grid(row = 0 , column = 0, columnspan = 1000)

                self.speeds = [1, 2, 5, 10, 50, 100]
                self.speedItems = {}

                for speed in self.speeds:
                        image = tk.PhotoImage(file = getResourcePath("assets/speeds/X{}.png".format(speed)))
                        button = tk.Button(self.speedsFrame, image = image, command = lambda x=speed: self.parent.solver.setSpeed(x), borderwidth = 0)
                        button.grid(row = 1, column = speed)

                        self.speedItems.update({speed: {"image": image, "button": button}})

                self.stepButton = tk.Button(self, width = 10, height = 2, text = "Step", command = self.step)
                self.stepButton.grid(row = 10, column = 0, pady = 5)

                self.advancedInfo = tk.IntVar()
                self.advancedInfoButton = ttk.Checkbutton(self, text = "Show Advanced Information?", variable=self.advancedInfo)
                self.advancedInfoButton.grid(row = 11, column = 0, pady = 5)
                self.advancedInformationFrame = tk.Frame(self)
                self.advancedInformationFrame.grid(row = 15, column = 0, pady = 10)

                self.advancedInformation = ttk.Label(self.advancedInformationFrame, text = "Advanced Solver Information",style = "Subheading.TLabel")
                self.advancedInformation.grid(row = 0, column = 0, pady = 10)

                self.stepCount = tk.Label(self.advancedInformationFrame, text = "Steps: 0", font = ("Helvetica", 12, "bold italic"))
                self.stepCount.grid(row = 1, column = 0)


        def startAutoStep(self):
                self.parent.solver.autorun = True
                self.parent.solver.step()


        def stopAutoStep(self):
                self.parent.solver.autorun = False


        def stopSolve(self):
                if mb.askyesno("End Solve?", "Are you sure you want to stop the current solve?"):
                        self.stopAutoStep()
                        self.parent.maze.solving = False
                        self.parent.solver = None
                        self.parent.changeMenu(None)

                        self.parent.after(1, self.parent.maze.unvisitTiles)


        def step(self):
                self.parent.solver.step() if not self.parent.solver.autorun else mb.showerror("ERROR", "Cannot force step whilst autorunning")
                self.parent.solver.step(force = True) if not self.parent.solver.autorun else mb.showerror("ERROR", "Cannot force step whilst autorunning")


        def updateLabel(self, newValue):
                self.autoStepDelayLabel.config(text = "{:.3f}".format(float(newValue)))
                self.parent.solver.delay = float(newValue)
