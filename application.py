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
                self.frames = dict()

                # Load in all tabs and put them in our dictionary.
                self.frames[HomeScreen] = HomeScreen(self)
                self.frames[MazeScreen] = MazeScreen(self)

                # Load the homescreen
                self.changeFrame(HomeScreen)

                # Create a dictionary for the side menus and populate it.
                self.menus = dict()

                # Load in all menus and put them in our dictionary.
                self.menus[SolverSettings] = SolverSettings(self)
                self.menus[GenerationSettings] = GenerationSettings(self)
                self.menus[SolverMenu] = SolverMenu(self)

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
                        mb.showinfo(self.title, u"Found it!\n31.9505\u00B0 S, 115.8605\u00B0 E")
                        self.EEPos = 0

        def loadStyles(self):
                # Load a style object
                self.style = ttk.Style()

                # Set the default background for all widgets to a specific colour
                self.style.configure(".", background = "#d9d9d9")
                
                # Load in styles for any situation we need.
                self.style.configure("Header.TLabel", font = ("Helvetica", 15, "italic"))

                self.style.configure("Title.TLabel", font = ("Helvetica", 30, "bold italic"))

                self.style.configure("Subheading.TLabel", font = ("Helvetica", 13))

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
                
                # If we are currently solving a maze, this brings up the Solver Menu, otherwise it brings up the Solver Settings.
                self.menubar.add_command(label = "Solve Current Maze", command = lambda: self.changeMenu(SolverMenu) if self.maze.solving else self.changeMenu(SolverSettings))

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
                if re.match(".+(?i)(.maz)\\b",filePath) != None:
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
                if re.match(".+(?i)(.maz)\\b",filePath) != None:
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
                self.maze = None
                self.maze = maze.Maze(frame, canvasSize = self.screenSize, size = size)
                self.maze.canvas.grid(row = 0, column = 0)

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
                elif algorithm == "Kruskals Algorithm":
                        from generators.kruskals import Generator
                else:
                        print("No item selected")
                        return

                # Load in the size of the maze from settings
                size = int(settings.mazeSize.get())

                # Reset the current maze and generate a new one from the loaded generator.
                self.loadMaze(size)

                # Use the generator to create a new maze.
                Generator(self.maze)

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
                self.solver = Solver(self.maze, settings)

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
                self.exitButton.grid(row = 0, column = 0, sticky = "NE")

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

                generators = (  "Recursive Backtracker",
                                "Prims Algorithm",
                                "Kruskals Algorithm"
                                        )

                self.algorithmChoice = ttk.Combobox(self, values = generators, state = "readonly", width = 20, font = ("arial", 14))
                self.algorithmChoice.current(0)
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

                self.speedsFrame = tk.Frame(self)
                self.speedsFrame.grid(row = 4, column = 0)

                self.speedDisplay = ttk.Label(self.speedsFrame, text="Current Speed: X1", style="Subheading.TLabel")
                self.speedDisplay.grid(row = 0 , column = 0, columnspan = 1000)

                self.X1 = tk.PhotoImage(file = "assets/SpeedX1.png")
                self.X1Button = tk.Button(self.speedsFrame, image = self.X1, command = lambda:self.setSpeed(1), borderwidth = 0)
                self.X1Button.grid(row = 1, column = 1)

                self.X2 = tk.PhotoImage(file = "assets/SpeedX2.png")
                self.X2Button = tk.Button(self.speedsFrame, image = self.X2, command = lambda:self.setSpeed(2), borderwidth = 0)
                self.X2Button.grid(row = 1, column = 2)

                self.X5 = tk.PhotoImage(file = "assets/SpeedX5.png")
                self.X5Button = tk.Button(self.speedsFrame, image = self.X5, command = lambda:self.setSpeed(5), borderwidth = 0)
                self.X5Button.grid(row = 1, column = 5)

                self.X10 = tk.PhotoImage(file = "assets/SpeedX10.png")
                self.X10Button = tk.Button(self.speedsFrame, image = self.X10, command = lambda:self.setSpeed(10), borderwidth = 0)
                self.X10Button.grid(row = 1, column = 10)

                self.X50 = tk.PhotoImage(file = "assets/SpeedX50.png")
                self.X50Button = tk.Button(self.speedsFrame, image = self.X50, command = lambda:self.setSpeed(50), borderwidth = 0)
                self.X50Button.grid(row = 1, column = 50)

                self.X100 = tk.PhotoImage(file = "assets/SpeedX100.png")
                self.X100Button = tk.Button(self.speedsFrame, image = self.X100, command = lambda:self.setSpeed(100), borderwidth = 0)
                self.X100Button.grid(row = 1, column = 100)

                self.speed = tk.DoubleVar()
                self.speed.set(1)
                self.speed.trace("w", self.updateLabel)

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

        def setSpeed(self, newSpeed):
                self.speed.set(newSpeed)

        def updateLabel(self, *args):
                self.speedDisplay.config(text = "Current Speed: X{}".format(int(self.speed.get())))
                self.parent.menus[SolverMenu].speedDisplay.config(text = "Current Speed: X{}".format(int(self.speed.get())))

        def solveMaze(self):
                self.parent.solveMaze()
                
                        
class SolverMenu(SettingsMenu):
        def __init__(self, parent):
                super().__init__(parent)

                self.loadTitle("assets/solveTitle.png")

                self.autoStepControls = tk.Frame(self)
                self.autoStepControls.grid(row = 1, column = 0)

                buttons = {"playButton" : self.startAutoStep, "pauseButton" : self.stopAutoStep, "stopButton" : self.stopSolve}
                
                self.play = tk.PhotoImage(file = "assets/playButton.png")
                self.playButton = tk.Button(self.autoStepControls, image = self.play, command = self.startAutoStep, borderwidth = 0)
                self.playButton.grid(row = 0, column = 0)

                self.pause = tk.PhotoImage(file = "assets/pauseButton.png")
                self.pauseButton = tk.Button(self.autoStepControls, image = self.pause, command = self.stopAutoStep, borderwidth = 0)
                self.pauseButton.grid(row = 0, column = 1)

                self.stop = tk.PhotoImage(file = "assets/stopButton.png")
                self.stopButton = tk.Button(self.autoStepControls, image = self.stop, command = self.stopSolve, borderwidth = 0)
                self.stopButton.grid(row = 0, column = 2)

                self.speedsFrame = tk.Frame(self)
                self.speedsFrame.grid(row = 4, column = 0)

                self.speedDisplay = ttk.Label(self.speedsFrame, text="Current Speed: X1", style="Subheading.TLabel")
                self.speedDisplay.grid(row = 0 , column = 0, columnspan = 1000)

                self.X1 = tk.PhotoImage(file = "assets/SpeedX1.png")
                self.X1Button = tk.Button(self.speedsFrame, image = self.X1, command = lambda:self.parent.solver.setSpeed(1), borderwidth = 0)
                self.X1Button.grid(row = 1, column = 1)

                self.X2 = tk.PhotoImage(file = "assets/SpeedX2.png")
                self.X2Button = tk.Button(self.speedsFrame, image = self.X2, command = lambda:self.parent.solver.setSpeed(2), borderwidth = 0)
                self.X2Button.grid(row = 1, column = 2)

                self.X5 = tk.PhotoImage(file = "assets/SpeedX5.png")
                self.X5Button = tk.Button(self.speedsFrame, image = self.X5, command = lambda:self.parent.solver.setSpeed(5), borderwidth = 0)
                self.X5Button.grid(row = 1, column = 5)

                self.X10 = tk.PhotoImage(file = "assets/SpeedX10.png")
                self.X10Button = tk.Button(self.speedsFrame, image = self.X10, command = lambda:self.parent.solver.setSpeed(10), borderwidth = 0)
                self.X10Button.grid(row = 1, column = 10)

                self.X50 = tk.PhotoImage(file = "assets/SpeedX50.png")
                self.X50Button = tk.Button(self.speedsFrame, image = self.X50, command = lambda:self.parent.solver.setSpeed(50), borderwidth = 0)
                self.X50Button.grid(row = 1, column = 50)

                self.X100 = tk.PhotoImage(file = "assets/SpeedX100.png")
                self.X100Button = tk.Button(self.speedsFrame, image = self.X100, command = lambda:self.parent.solver.setSpeed(100), borderwidth = 0)
                self.X100Button.grid(row = 1, column = 100)

                self.stepButton = tk.Button(self, width = 10, height = 2, text = "Step", command = self.step)
                self.stepButton.grid(row = 10, column = 0, pady = 5)

                self.advancedInfo = tk.IntVar()
                self.advancedInfoButton = ttk.Checkbutton(self, text = "Show Advanced Information?", variable=self.advancedInfo)                
                self.advancedInfoButton.grid(row = 11, column = 0, pady = 5)        

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

                        self.parent.after(1000, self.parent.maze.unvisitTiles)

        def step(self):
                self.parent.solver.step() if not self.parent.solver.autorun else mb.showerror("ERROR", "Cannot force step whilst autorunning")
                
        def updateLabel(self, newValue):
                self.autoStepDelayLabel.config(text = "{:.3f}".format(float(newValue)))
                self.parent.solver.delay = float(newValue)
