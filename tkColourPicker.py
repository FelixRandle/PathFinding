import tkinter as tk
import tkinter.colorchooser as colourChooser


class ColourPicker(tk.Frame):
    def __init__(self, parent, width, height, command=None, key=None, index=0):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.command = command
        self.key = key
        self.index = index

        self.currentColour = "#FFFFFF"

        self.clickable = tk.Button(self, width=self.width, height=self.height,
                                   background=self.currentColour,
                                   command=self.chooseColour)
        self.clickable.pack()

    def set(self, newColour):
        self.currentColour = newColour
        self.clickable.config(background=self.currentColour)

    def get(self):
        return self.currentColour

    def chooseColour(self):
        newColour = colourChooser.askcolor()

        if newColour is not None:
            self.set(newColour[1])
            self.command(self.key, newColour[1], self.index)
