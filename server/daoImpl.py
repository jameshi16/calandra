# daoImpl.py - Implementation for DAO
import sqlite3
from dao import UserDAO

class UserDAOImpl(UserDAO):
    def __init__(self):
        self.table_name = "Users"
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

        res = self.cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")

        if res.fetchone()[0] == 0:
            self.cur.execute(f"CREATE TABLE {self.table_name}(userid TEXT PRIMARY KEY, token TEXT, session TEXT, events BLOB)")

        self.con.commit()

    def destroy(self):
        self.cur.close()
        self.con.close()

    def saveEvents(self, studentNumber, events):
        res = self.cur.execute(f"UPDATE {self.table_name} SET events={events} WHERE userid=?", ({studentNumber},))
        self.con.commit()

    def createNewUser(self, studentNumber):
        res = self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE userid=?", (studentNumber,))
        if res.fetchone()[0] == 0:
            self.cur.execute(f"INSERT OR IGNORE INTO {self.table_name} VALUES (?, NULL, NULL, NULL)", (studentNumber, ))
        else:
            print("createNewUser user already exists, skipping")
        self.con.commit()

    def deleteUser(self, studentNumber):
        res = self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE userid=?", (studentNumber,))
        if res.fetchone()[0] > 0:
            self.cur.execute(f"DELETE FROM {self.table_name} WHERE userid=?", (studentNumber,))
        else:
            print("deleteUser: user doesn't already exist, skipping")

    def doesUserExist(self, studentNumber):
        res = self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE userid=?", (studentNumber,))
        return res.fetchone()[0]

    def getUser(self, studentNumber):
        if not self.doesUserExist(studentNumber):
            return ()
        res = self.cur.execute(f"SELECT * FROM {self.table_name} WHERE userid=?", (studentNumber,))
        return res.fetchone()

    def saveSession(self, studentNumber, session):
        res = self.cur.execute(f"UPDATE {self.table_name} SET session={session} WHERE userid=?", (studentNumber,))

    def saveToken(self, studentNumber, token):
        res = self.cur.execute(f"UPDATE {self.table_name} SET token=? WHERE userid=?", (token, studentNumber))
        self.con.commit()

    def getEvents(self, studentNumber):
        return self.getUser(studentNumber)[3]

    def getToken(self, studentNumber):
        # TODO: hacky hack hack
        return self.getUser(studentNumber)[1]

    def getSession(self, studentNumber):
        # TODO: hehexd
        return self.getUser(studentNumber)[2]
