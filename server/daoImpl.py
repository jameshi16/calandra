# daoImpl.py - Implementation for DAO
import sqlite3
from dao import UserDAO

con = sqlite3.connect("data.db")
cur = con.cursor()

class UserDAOImpl(UserDAO):
    def __init__(self):
        self.table_name = "Users"

        res = cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")

        if res.fetchone()[0] == 0:
            cur.execute(f"CREATE TABLE {self.table_name}(userid INTERGER, token TEXT, events BLOB)")

        con.commit()

    def saveEvents(self, studentNumber, events):
        res = cur.execute(f"UPDATE {self.table_name} SET events={events} WHERE userid={studentNumber}")
        con.commit()

    def createNewUser(self, studentNumber):
        res = cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE userid={studentNumber}")
        if res.fetchone()[0] == 0:
            cur.execute(f"INSERT OR IGNORE INTO {self.table_name} VALUES ({studentNumber}, NULL, NULL)")
        else:
            print("createNewUser user already exists, skipping")
        con.commit()

    def deleteUser(self, studentNumber):
        res = cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE userid={studentNumber}")
        if res.fetchone()[0] > 0:
            cur.execute(f"DELETE FROM {self.table_name} WHERE userid={studentNumber}")
        else:
            print("deleteUser: user doesn't already exist, skipping")

    def doesUserExist(self, studentNumber):
        res = cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE userid={studentNumber}")
        return res.fetchone()[0]

    def getUser(self, studentNumber):
        if not self.doesUserExist(studentNumber):
            return ()
        res = cur.execute(f"SELECT * FROM {self.table_name} WHERE userid={studentNumber}")
        return res.fetchone()

    def saveToken(self, token):
        res = cur.execute(f"UPDATE {self.table_name} SET token={token} WHERE userid={studentNumber}")
        con.commit()

    def getToken(self, studentNumber):
        return self.getUser(studentNumber)[1]
