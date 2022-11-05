# parsing json files, formating and getting data !
# using webscriptiing
import requests
import json
import time
import pprint

import datetime


def convert(event):
    event=str(event)
    event = event[:len(event) - 7]
    event = event.replace('T', " ");
    return event

def convert_current(event):
    event = str(event)
    l = len(event)
    event = event[:l - 7]
    return event

def parse_json_data(url):
    i=0
    current_date=datetime.date.today()
    events = []
    data = requests.get(url).json()
    event_date = current_date
    next_week_date = current_date + datetime.timedelta(7)
    while current_date <= event_date <= next_week_date:#
        title = (data[i]['title'])
        start = datetime.datetime.fromtimestamp(int(data[i]['field_date_range_value']))
        end = datetime.datetime.fromtimestamp(int(data[i]['field_date_range_end_value']))
        soc = (data[i]['field_event_owner_group'])
        event_date = datetime.date.fromtimestamp(int(data[i]['field_date_range_value']))
        e = Event(title, start, end, soc)
        events.append(e)
        i += 1
    return events


def parse_other_json_data(url):
    i=0
    current_date=datetime.datetime.now()
    events = []
    data = requests.get(url).json()
    cleaned_data = data['response']['resultPacket']['results']
    event_date = convert(current_date)
    next_week_date = current_date + datetime.timedelta(7)
    next_week_date=convert(next_week_date)
    current_date= convert(current_date)
    while str(current_date) <= str(event_date) <= str(next_week_date):
        title = cleaned_data[i]['title']
        start = cleaned_data[i]['metaData']['d']
        end = cleaned_data[i]['metaData']['d']
        soc = cleaned_data[i]['metaData']['UclOrgUnit']
        event_date = convert(start)
        e = Event(title, start, end, soc)
        events.append(e)
        i += 1
    return (events)

def get_external_events(su_url, ucl_url):
    list=[]
    list.append(parse_json_data(su_url))
    list.append(parse_other_json_data(ucl_url))
    return list



class Event:
    def __init__(self, title, start_date, end_date, soc):
        self.title = title
        self.start = start_date
        self.end = end_date
        self.soc = soc


URL = "https://studentsunionucl.org/whats-on/json/1667084400/1667952000/list/12"

URL_2 = 'https://cms-feed.ucl.ac.uk/s/search.json?collection=drupal-meta-events&meta_FeedableSyndication=%22cd6bcf8d-393d-4e80-babb-1c73b2cb6c5f%22&&ge_DateFilter=20221105'

print(get_external_events(URL,URL_2)[0][0].start)
