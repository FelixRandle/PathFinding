import sqlite3 as sql


class Database:
    def __init__(self, databasePath, coloursInfo):
        self.db = sql.connect(databasePath)
        self.db.row_factory = sql.Row
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
                self.cursor.execute(
                    "ALTER TABLE COLOURS ADD {} VARCHAR DEFAULT {}".format(
                        tileName, coloursInfo[key]))
                self.db.commit()
            except sql.OperationalError:
                pass

    def getUserID(self, username):
        self.cursor.execute("""
            SELECT userID FROM
            USERS
            WHERE username = ?
        """, (username,))

        result = self.cursor.fetchone()
        if result is not None:
            return result[0]

    def addUser(self, username):
        try:
            self.cursor.execute("""
                INSERT INTO USERS
                (username)
                VALUES
                (?)
            """, (username,))

            self.db.commit()
        except sql.IntegrityError:
            pass

        UID = self.getUserID(username)

        try:
            self.cursor.execute("""
                INSERT INTO
                COLOURS
                (userID)
                VALUES
                (?)
            """, (UID, ))
            self.db.commit()
        except sql.IntegrityError:
            pass

        return UID

    def loginUser(self, username):
        UID = self.getUserID(username)
        if UID is None:
            UID = self.addUser(username)
        colours = self.getUserColours(UID)
        return UID, colours

    def getUserColours(self, userID=0):
        returnColours = self.coloursInfo

        if userID == 0:
            return returnColours

        self.cursor.execute("""
            SELECT * FROM
            COLOURS
            WHERE userID = ?
        """, (userID, ))
        userColours = self.cursor.fetchone()
        # Loop through columns from database and keys from colours dictionary.
        for column in userColours.keys():
            for key in returnColours:
                if key.name == column:
                    # Recreate string array
                    coloursArr = ("".join(c for c in userColours[column] if c
                                          not in "[]' ").split(","))
                    returnColours.update({key: coloursArr})

        return returnColours

    def updateUserColours(self, userID, fieldName, index, newColour):
        self.cursor.execute("""
                            SELECT {} FROM
                            COLOURS
                            WHERE userID = ?
                            """.format(fieldName), (userID, ))

        result = self.cursor.fetchone()
        # Recreate string as an array after removing all []' characters.
        coloursArr = ("".join(c for c in result[0] if c
                              not in "[]' ").split(","))
        coloursArr[index] = newColour

        self.cursor.execute("""
                            UPDATE COLOURS
                            SET {} = ?
                            WHERE userID = ?
                            """.format(fieldName), (str(coloursArr)[1:-1],
                                                    userID,))

        self.db.commit()

        self.cursor.execute("""
                            SELECT {} FROM
                            COLOURS
                            WHERE userID = ?
                            """.format(fieldName), (userID, ))

        result = self.cursor.fetchone()


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

    # Dictionary of colours to use for different tiles, background
    # then foreground
    tileColours = {
        tileTypes.WALL: ["black", "black"],
        tileTypes.PATH: ["light grey", "white"],
        tileTypes.START: ["green", "light green"],
        tileTypes.END: ["pink", "red"],
        tileTypes.PATH_VISITED_ONCE: ["light grey", "#2376fc"],
        tileTypes.PATH_VISITED_TWICE: ["light grey", "#0048bc"],
        tileTypes.FOUND_PATH: ["cyan", "magenta"]
            }

    db = Database(tileColours)

    user, colours = db.loginUser("sadfjkfds")
    print(user, colours)
