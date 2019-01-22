# External Imports
# Tkinter and ttk libraries used for GUI aspects of the program.
import tkinter as tk
import tkinter.ttk as ttk
# Enum library used for different tileTypes.
from enum import IntEnum
# Pickle library used for serializing and deserializing maze objects.
import pickle

# Enum for the different tiles we can have in the maze.
class tileTypes(IntEnum):
    WALL = 0
    PATH = 1
    PATH_VISITED_ONCE = 2
    PATH_VISITED_TWICE = 3
    FOUND_PATH = 5
    START = 10
    END = 11

# Dictionary of colours to use for different tiles, background then foreground
tileColours = { tileTypes.WALL: ["black", "black"],
        tileTypes.PATH: ["light grey", "white"],
        tileTypes.START: ["green", "light green"],
        tileTypes.END: ["pink", "red"],
        tileTypes.PATH_VISITED_ONCE: ["light grey", "#2376fc"],
        tileTypes.PATH_VISITED_TWICE: ["light grey", "#0048bc"],
        tileTypes.FOUND_PATH: ["cyan", "magenta"]
        }

class Maze:
    """Class used to hold maze information."""
    def __init__(self, parent, size = 15, canvasSize = 600):
        """
        Arguments:
            parent -- The parent from tkinter, either Frame or Tk object.
            size -- The width and height of the maze. (Default 5)
            canvasSize -- The size in pixels of the canvas to use to display the maze. (Default 600)
        """
        self.parent = parent
        self.size = size
        self.canvasSize = canvasSize

        """
        Additional Variables:
            start -- The current start point of the maze.
            end -- The current end point of the maze.
            canvas -- The tkinter canvas object that displays the maze.
            tiles -- 2 Dimensional array containing all Tiles for the maze.
        """
        self.start = None
        self.end = None
        self.canvas = tk.Canvas(self.parent, width = canvasSize, height = canvasSize, borderwidth = 0, highlightthickness = 0)

        # Create a 2 Dimensional array of tiles using our given parameters. Default all to WALL.
        self.tiles = [[Tile(self.canvas, self, x, y, self.canvasSize / self.size, tileTypes.WALL) for y in range(0, size)] for x in range(0, size)]
        # Loop through 0 to 1 below the mazes size for an x coordinate.
        for x in range(0, self.size):
            # Loop through 0 to 1 below the mazes size for a y coordinate.
            for y in range(0, self.size):
                # Find the neighbouring tiles. This must be done after all tiles are
                # created otherwise the neighbour may not have been made.
                self.tiles[x][y].findNeighbours()

        self.solving = False

        # Bind buttons to allow for 'drawing' the maze.
        """
        B1/Button-1 | Left Click -- Draw Path.
        B1/Button-3 | Right Click -- Draw Wall.
        Shift+Button-1 | Shift + Left Click -- Set Start.
        Shift+Button-2 | Shift + Right Click -- Set End.
        """
        self.canvas.bind("<B1-Motion>", lambda event: self.setTile(event, tileTypes.PATH))
        self.canvas.bind("<Button-1>", lambda event: self.setTile(event, tileTypes.PATH))
        self.canvas.bind("<B3-Motion>", lambda event: self.setTile(event, tileTypes.WALL))
        self.canvas.bind("<Button-3>", lambda event: self.setTile(event, tileTypes.WALL))
        self.canvas.bind("<Shift-Button-1>", lambda event: self.setTile(event, tileTypes.START))
        self.canvas.bind("<Shift-Button-3>", lambda event: self.setTile(event, tileTypes.END))


    def toFile(self, filePath = "saves/save.p"):
        """
        Method for saving the current maze to a file.
        Arguments:
            filePath -- Path to where to save the file
        """
        # Save data about the maze that we need.
        data = {
            "size": self.size,
            "tiles": {},
            }
        # Loop through each row of tiles.
        for x in range(0, len(self.tiles)):
            # Create an empty dictionary for each row of the maze.
            data["tiles"][x] = {}
            # Loop through each tile of the row.
            for y in range(0, len(self.tiles[x])):
                # Save the string version of the tile to the dictionary.
                data["tiles"][x][y] = self.tiles[x][y].toString()
        # Dump the serialized data to the given filepath.
        pickle.dump(data, open(filePath, "wb"))


    def fromFile(self, filePath):
        """
        Method for loading a maze from a file.
        Arguments:
            filePath -- Path to pull the maze from.
        """
        # Load serialized data from file.
        mazeObj = pickle.load(open(filePath, "rb"))
        # Load in maze size
        self.size = mazeObj["size"]
        # Clear current tiles
        self.tiles = []
        # Delete all current objects drawn so we don't start to lag when loading multiple mazes.
        self.canvas.delete("all")
        # Loop through each list of tiles
        for rowNo, row in mazeObj["tiles"].items():
            # Create an empty list for each list in the saved maze.
            self.tiles.append([])
            # Loop through each tile in the list
            for itemNo, item in row.items():
                # Collect the current item for easier referencing
                currentItem = mazeObj["tiles"][rowNo][itemNo]
                # Add a tile with the saved parameters to the list.
                self.tiles[rowNo].append(Tile(self.canvas, self,
                        currentItem["x"], currentItem["y"],
                        currentItem["size"],
                        currentItem["tileType"]))


    def setTile(self, event, tileType = tileTypes.WALL):
        """
        Internal method for handling mouse click events.
        This allows the user to 'draw' parts of the maze.
        """
        # If edit mode is enabled from top menu, continue.
        x = event.x
        y = event.y
        if self.parent.editMode:
            # Translate the pixel X and Y into values that we can access the list with.
            listX = int(x / (self.canvasSize / self.size))
            listY = int(y / (self.canvasSize / self.size))
            # If the translated coordinates are within the list size.
            if listX >= 0 and listX < self.size and listY >= 0 and listY < self.size:
                # Set the tile to the given tileType
                if tileType == tileTypes.PATH:
                    self.tiles[listX][listY].setPath()
                elif tileType == tileTypes.WALL:
                    self.tiles[listX][listY].setWall()
                # For START and END we must also update the mazes saved start and end point.
                elif tileType == tileTypes.START:
                    self.tiles[listX][listY].setStart()
                    self.start = self.tiles[listX][listY]
                elif tileType == tileTypes.END:
                    self.tiles[listX][listY].setEnd()
                    self.end = self.tiles[listX][listY]


    def unvisitTiles(self):
        """
        Method used to turn all tiles currently marked as visited back to normal paths.
        """
        for tileX in self.tiles:
            for tile in tileX:
                if tile.tileType in (tileTypes.PATH_VISITED_ONCE, tileTypes.PATH_VISITED_TWICE, tileTypes.FOUND_PATH):
                    tile.setPath()


class Tile:
    """Class used for the tiles of a maze."""
    def __init__(self, parent, maze, xPos, yPos, size, tileType, border = 0.1):
        """
        Arguments:
            parent -- the parent canvas that the tile will use.
            xPos -- The x grid coordinate of the tile.
            yPos -- The y grid coordinate of the tile.
            size -- The width and height that the tile should be.
            tileType -- Used to define what the tile should appear as.
            border -- Used to define the percentage of the size that the border should be. (Default 0.1)
        """
        self.parent = parent
        self.maze = maze
        self.x = xPos
        self.y = yPos
        # X and Y are then translated to pixel coordinates.
        self.xPos = xPos * size
        self.yPos = yPos * size
        self.size = size
        self.tileType = tileType
        self.borderSize = int(self.size * border)

        """
        Additional Variables:
            visitCount -- how many times this tile has been visited.
            neighbours --  A list of all neighbours of this tile and information about them.
            backgroundColour -- The background colour of the tile.
            colour -- The foreground colour of the tile. At smaller tile sizes this is the sole colour.
            canvasRect -- The canvas rectangle used to display the Tile on the gui.
        """
        self.visitCount = 0
        self.neighbours = []
        self.backgroundColour = tileColours[tileType][0]
        self.colour = tileColours[tileType][1]
        # Create the canvas rectangle using given parameters
        self.canvasRect = parent.create_rectangle(int(self.xPos + (self.borderSize / 2)), int(self.yPos + (self.borderSize / 2)),
            int(self.xPos + (self.size - self.borderSize / 2)), int(self.yPos + (self.size - self.borderSize / 2)),
            fill = self.colour, outline = self.backgroundColour, width = self.borderSize)

        if self.tileType == tileTypes.START:
            self.maze.start = self
        elif self.tileType == tileTypes.END:
            self.maze.end = self

    def findNeighbours(self, distance = 2, blockVisited = False, blockWalls = False):
        """
        Method for finding the current tiles neighbours.
        Find those two away as all walls are placed on even coordinates
        """
        # List of relative neighbours based on given distances.
        relativeNeighbours = [               [0, distance],
                    [-distance, 0],           [distance, 0],
                             [0, -distance]
        ]

        #Loop through the positions of neighbours if they are on the Maze
        self.neighbours = []
        for coords in relativeNeighbours:
            # If inside the maze
            if (self.x + coords[0] >= 0) and (self.y + coords[1] >= 0) and (self.x + coords[0] < self.maze.size) and (self.y + coords[1] < self.maze.size):
                # If not visited
                if (blockVisited and self.maze.tiles[self.x + coords[0]][self.y + coords[1]].visitCount < 1) or (not blockVisited):
                    # If not a wall
                    if (blockWalls and self.maze.tiles[self.x + coords[0]][self.y + coords[1]].tileType != tileTypes.WALL) or (not blockWalls):
                        self.neighbours.append(self.maze.tiles[self.x + coords[0]][self.y + coords[1]])

        return self.neighbours

    def toString(self):
        """
        Method for translating our Tile object to a string so that it can be stored in a file.
        """
        data = {
            "x": self.x,
            "y": self.y,
            "size": self.size,
            "tileType": self.tileType,
            }
        return data

    def updateColour(self):
        fill = tileColours[self.tileType][1]
        outline = tileColours[self.tileType][0]

        self.parent.itemconfig(self.canvasRect, fill = fill)
        self.parent.itemconfig(self.canvasRect, outline = outline)

    def changeType(self, newType = tileTypes.PATH):
        """
        Internal method for changing the tile type. This should not be used by generators or solvers.
        Arguments:
            newType -- The new tileType that it should be changed to. Defaults to PATH.
        """
        tileBuffer = None
        if self.tileType == tileTypes.START:
            tileBuffer = self.maze.start
            self.maze.start = None
        elif self.tileType == tileTypes.END:
            tileBuffer = self.maze.end
            self.maze.end = None

        # Change the tileType of the tile.
        self.tileType = newType
        # Change the tile colours to reflect the newly desired tile.
        self.updateColour()

        if tileBuffer != None:
            print(tileBuffer)
            tileBuffer.setWall()

    def setWall(self):
        """
        Set the current tile to a WALL tile.
        """
        self.changeType(newType = tileTypes.WALL)

    def setPath(self):
        """
        Set the current tile to a PATH tile
        """
        self.changeType(newType = tileTypes.PATH)

    def setVisited(self):
        """
        Set the current tile to a PATH_VISITED_* tile.
        """

        if self.tileType not in (tileTypes.START, tileTypes.END):
            if self.visitCount > 0:
                tileType = tileTypes.PATH_VISITED_TWICE
            else:
                tileType = tileTypes.PATH_VISITED_ONCE
        else:
            return

        self.changeType(newType = tileType)

        self.visitCount += 1

    def setRoute(self):
        """
        Set the current tile to a FOUND_PATH tile.
        """
        if self.tileType not in (tileTypes.START, tileTypes.END):
            self.changeType(newType = tileTypes.FOUND_PATH)

    def setStart(self):
        """
        Set the current tile to a START tile.
        """
        # Change the mazes start point.
        self.changeType(newType = tileTypes.START)
        self.maze.start = self

    def setEnd(self):
        """
        Set the current tile to an END tile.
        """
        # Change the mazes end point.
        self.changeType(newType = tileTypes.END)
        self.maze.end = self
