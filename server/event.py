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

# TODO: merge implementation
# list is not sorted
# list has all the events in the tags
# give two urls
def get_external_events(student_union_url, ucl_url):
    return []
