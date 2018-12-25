import sqlite3 as sql

class Database:
    def __init__(self, coloursInfo):
        self.db =  sql.connect("userData.db")
        self.cursor = self.db.cursor()

        self.coloursInfo = coloursInfo

        self.createTables()

        self.updateColours(coloursInfo)

        self.user = 0


    def createTables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            USERS
            (userID INTEGER PRIMARY KEY, username TEXT UNIQUE)
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            COLOURS
            (userID INTEGER UNIQUE)
        """)

        self.db.commit()

    def updateColours(self, coloursInfo):
        for key, item in coloursInfo.items():
                tileName = key.name.upper()
                try:
                    self.cursor.execute("ALTER TABLE COLOURS ADD {} VARCHAR DEFAULT {}".format(tileName, coloursInfo[key]))
                    self.db.commit()
                except sql.OperationalError:
                    print("Duplicate "+tileName)

    def addUser(self, userName):
        try:
            self.cursor.execute("""
                INSERT INTO USERS
                (username)
                VALUES
                (?)
            """, (userName,))

            self.db.commit()
        except sql.IntegrityError:
            pass

        try:
            self.cursor.execute("""
                INSERT INTO
                COLOURS
                (userID)
                VALUES
                (?)
            """, (self.user, ))
        except sql.IntegrityError:
            pass

        self.db.commit()

    def loginUser(self, username):
        self.cursor.execute("""
            SELECT userID FROM
            USERS
            WHERE username = ?
        """, (username,))

        result = self.cursor.fetchone()
        if result != None:
            return result[0]
        else:
            raise Exception("loginUser should return userID, returned {}".format(result))

    def getUserColours(self):
        returnColours = self.coloursInfo

        if self.user == 0:
            return returnColours

        self.cursor.execute("""
            SELECT * FROM
            COLOURS
            WHERE userID = ?
        """, (self.user, ))
        userColours = self.cursor.fetchone()

        #print(userColours)


if __name__ == '__main__':
    from enum import IntEnum

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

    db = Database(tileColours)

    db.addUser("isdg")

    db.loginUser("isdg")

    db.getUserColours()
