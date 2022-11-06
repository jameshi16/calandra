# parsing json files, formating and getting data !
# using webscriptiing
import requests
import datetime

from event import Event


def increment_url(url, counter):
    return url[:-len(str(counter)) - 1] + '/' + str(counter)


def convert(event):
    event = str(event)
    event = event[:len(event) - 6]
    event = event.replace('T', " ")
    return event


def convert_current(event):
    event = str(event)
    l = len(event)
    event = event[:l - 7]
    return event


def exception_handling(url):
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()


def parse_su_jsondata(url):
    counter = 0
    current_date = datetime.date.today()
    next_week_date = current_date + datetime.timedelta(7)
    events_su = []
    for counter in range(5):
        data = exception_handling(url)
        for i in range(len(data)):
            event_date = datetime.date.fromtimestamp(int(data[i]['field_date_range_value']))
            if current_date <= event_date <= next_week_date:  # date in correct range
                title = (data[i]['title'])
                start = datetime.datetime.fromtimestamp(int(data[i]['field_date_range_value']))
                end = datetime.datetime.fromtimestamp(int(data[i]['field_date_range_end_value']))
                soc = (data[i]['field_event_owner_group'])
                type = 2
                e = Event(title, start, end, soc, type)
                events_su.append(e)
        url = increment_url(url, counter)
    return events_su


def parse_ucl_jsondata(url):
    current_date = datetime.datetime.now()
    events_ucl = []
    next_week_date = current_date + datetime.timedelta(7)
    next_week_date = convert(next_week_date)
    current_date = convert(current_date)
    counter = 20221104
    for counter in range(20221104, 20221110):
        data = exception_handling(url)
        for i in range(len(data)):
            cleaned_data = data['response']['resultPacket']['results']
            start = cleaned_data[i]['metaData']['d']
            event_date = convert(start)
            if current_date <= event_date <= next_week_date:  # date in correct range
                title = cleaned_data[i]['title']
                end = cleaned_data[i]['metaData']['d']
                soc = cleaned_data[i]['metaData']['UclOrgUnit']
                type = 1
                e = Event(title, start, end, soc, type)
                events_ucl.append(e)
        counter += 1
        increment_url(url, counter)
    return events_ucl


def get_external_events_2(su_url, ucl_url):
    return parse_su_jsondata(su_url) + parse_ucl_jsondata(ucl_url)

# URL = "https://studentsunionucl.org/whats-on/json/1667084400/1667952000/list/0"
# URL_2 = 'https://cms-feed.ucl.ac.uk/s/search.json?collection=drupal-meta-events&meta_FeedableSyndication=%22cd6bcf8d-393d-4e80-babb-1c73b2cb6c5f%22&&ge_DateFilter=20221105'
