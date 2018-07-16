# Internal Imports
import maze

# External Imports
import tkinter as tk
import tkinter.ttk as ttk

main = tk.Tk()

newMaze = maze.Maze(main, size = 6, canvasSize = 600)
newMaze.canvas.pack()

main.mainloop()

