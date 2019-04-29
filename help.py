import tkinter as tk
from utils import getResourcePath


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
        self.backImage = tk.PhotoImage(
            file=getResourcePath("assets/help/back.png")).subsample(13, 13)
        tk.Button(self, image=self.backImage, borderwidth=0,
                  command=self.previousPage).grid(row=0, column=0)
        self.nextImage = tk.PhotoImage(
            file=getResourcePath("assets/help/next.png")).subsample(13, 13)
        tk.Button(self, image=self.nextImage, borderwidth=0,
                  command=self.nextPage).grid(row=0, column=2)

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


class Page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.createWidgets()

    def addPhoto(self, path):
        self.image = tk.PhotoImage(
            file=getResourcePath(path)).zoom(2, 2).subsample(5, 5)
        self.imageShown = tk.Label(self, image=self.image)
        self.imageShown.grid(row=0, column=0, pady=10)

    def addDescription(self, text):
        self.desc = tk.Label(self, text=text)
        self.desc.grid(row=10, column=0, pady=10)

    def addTitle(self, text):
        self.title = tk.Label(self, text=text, font=(12,))
        self.title.grid(row=5, column=0, pady=10)


class Page1(Page):
    def __init__(self, parent):
        super().__init__(parent)

    def createWidgets(self):
        self.addTitle("Welcome to the PathFinding Visualiser")
        self.addDescription("Please read the help guide thoroughly\nfor the best results")


class Page2(Page):
    def __init__(self, parent):
        super().__init__(parent)

    def createWidgets(self):
        self.addDescription("Hello from page 2")


class Page3(Page):
    def __init__(self, parent):
        super().__init__(parent)

    def createWidgets(self):
        self.addDescription("Hello from page 3")


class Page4(Page):
    def __init__(self, parent):
        super().__init__(parent)

    def createWidgets(self):
        self.addDescription("Hello from page 4")


class Page5(Page):
    def __init__(self, parent):
        super().__init__(parent)

    def createWidgets(self):
        self.addDescription("Hello from page 5")


class Page6(Page):
    def __init__(self, parent):
        super().__init__(parent)

    def createWidgets(self):
        self.addDescription("Hello from page 6")


if __name__ == "__main__":
    main = tk.Tk()

    help = HelpMenu()

    main.mainloop()
