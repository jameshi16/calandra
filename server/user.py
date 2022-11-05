# user.py - User

import json
from dao import UserDAO
from event import Event

class User:
    def __init__(self, dao, studentID, token=None, session=None, events=None):
        self.id = studentID
        self.token = token
        self.session = session
        self.events = events
        self.dao = dao

    def saveDB(self):
        if not self.dao.doesUserExist(self.id):
            self.dao.createNewUser(self.id)

        if self.events != None:
            serialized = [j.toJSON() for j in self.events]
            self.dao.saveEvents(json.dumps(serialized))

        if self.token != None:
            self.dao.saveToken(self.id, self.token)

        if self.session != None:
            self.dao.saveSession(self.session)

    def loadDB(self):
        if not self.dao.doesUserExist(self.id):
            return

        self.token = self.dao.getToken(self.id)
        self.session = self.dao.getSession(self.id)
        events = self.dao.getEvents(self.id)
        if events != None:
            data = json.loads(self.dao.getEvents(self.id))
            self.events = [Event(d['title'], d['start'], d['end'], d['tag'], d['event_type']) for d in data]
