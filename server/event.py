# event.py - Represents an event

class Event:
    def __init__(self, title, start_date, end_date, tag, event_type):
        self.title = title
        self.start = start_date
        self.end = end_date
        self.tag = tag
        self.event_type = 0

    def toJSON(self):
        return self.__dict__
