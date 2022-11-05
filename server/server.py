from flask import Flask, redirect, request
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from event import Event, get_external_events
from util import pt_timedate_to_str
import requests
import os
app = Flask(__name__)

# TODO: paginate these
STUDENT_UNION_URL = "https://studentsunionucl.org/whats-on/json/1667084400/1667952000/list/5"
UCL_URL = "https://cms-feed.ucl.ac.uk/s/search.json?collection=drupal-meta-events&meta_FeedableSyndication=%22cd6bcf8d-393d-4e80-babb-1c73b2cb6c5f%22&start_rank=31ge_DateFilter=20221101&lt_DateFilter=20221201&num_ranks=500"

# TODO: abstract this to work with multiple users
token = "uclapi-user-4bc189d14ad8c6a-ffa9476e018c48f-ba6268f6ad1e2a2-dab3966954ff80b"

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
url = f"https://uclapi.com/oauth/authorise/?client_id={client_id}&state=1"

@app.route('/login')
def uclapi_login():
    return redirect(url)


@app.route('/callback')
def receive_callback():
    global token

    # extract query parameters
    code = request.args.get('code', '')


    # e.g. request an auth token behind-the scenes
    params = {"client_id": client_id, "code": code,
              "client_secret": client_secret}
    r = requests.get("https://uclapi.com/oauth/token", params=params)
    decoded = r.json()

    token = decoded['token']
    return token

@app.route('/consolidated_timetable')
def consolidated_timetable():
    params = {"token": token,
              "client_secret": client_secret,
              "date": None}

    events = []

    for i in range(7, 14):
        date = datetime.now()
        date += timedelta(days=i)
        params["date"] = date.strftime("%Y-%m-%d")

        r = requests.get("https://uclapi.com/timetable/personal", params=params)
        res = r.json()

        if not res["ok"]:
            print("error retrieving personal timetable")
            abort(404)

        slots = res["timetable"][params["date"]]
        for j in range(len(slots)):
            slot = slots[j]
            start_time = pt_timedate_to_str(date, slot['start_time'])
            end_time = pt_timedate_to_str(date, slot['end_time'])
            tag = slot['module']['module_id']
            title = slot['session_title']

            e = Event(title, start_time, end_time, tag, 0)
            events.append(e.toJSON())

    events += get_external_events(STUDENT_UNION_URL, UCL_URL)
    return events
