import tkinter as tk


class HelpMenu(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Help Dialog")

        # self.resizable(False, False)
        self.geometry("400x400")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frames = []

        self.frames.append(Page1(self))
        self.frames.append(Page2(self))
        self.frames.append(Page3(self))
        self.frames.append(Page4(self))
        self.frames.append(Page5(self))
        self.frames.append(Page6(self))

        self.frames[0].grid(row=0, column=1)

        self.currentPage = 0

        self.createWidgets()

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

    def createWidgets(self):
        tk.Button(self, text="Forward",
                  command=self.nextPage,
                  height=1).grid(row=0, column=2)
        tk.Button(self, text="Back",
                  command=self.previousPage).grid(row=0, column=0)

    def changeFrame(self, newFrame):
        """
        Internal method for changing the current frame shown on screen.
        Arguments:
                newFrame -- The frame to change to
        """
        # Loop through all frames that are currently on the grid and remove
        # them from the grid
        for frame in self.grid_slaves():
            if frame.grid_info()["column"] == 1:
                frame.grid_forget()
        # Load the new frame
        frame = self.frames[newFrame]
        # Place our new frame onto the grid
        frame.grid(row=0, column=1)

    def nextPage(self):
        if self.currentPage < len(self.frames) - 1:
            self.currentPage += 1
            self.changeFrame(self.currentPage)

    def previousPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.changeFrame(self.currentPage)

    def closeWindow(self):
        self.grab_release()
        self.destroy()


class Page1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Hello from page 1").pack()


class Page2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Hello from page 2").pack()


class Page3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Hello from page 3").pack()


class Page4(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Hello from page 4").pack()


class Page5(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Hello from page 5").pack()


class Page6(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="Hello from page 6").pack()


if __name__ == "__main__":
    main = tk.Tk()

    help = HelpMenu()

    main.mainloop()
