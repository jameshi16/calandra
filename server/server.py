from flask import Flask, redirect, request, session, abort
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from event import Event, get_external_events
from util import pt_timedate_to_str
from user import User
from daoImpl import UserDAOImpl

import uuid
import requests
import os
app = Flask(__name__)

# TODO: paginate these
STUDENT_UNION_URL = "https://studentsunionucl.org/whats-on/json/1667084400/1667952000/list/5"
UCL_URL = "https://cms-feed.ucl.ac.uk/s/search.json?collection=drupal-meta-events&meta_FeedableSyndication=%22cd6bcf8d-393d-4e80-babb-1c73b2cb6c5f%22&start_rank=31ge_DateFilter=20221101&lt_DateFilter=20221201&num_ranks=500"

# TODO: abstract this to work with multiple users
token = ""

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
oauth_url = f"https://uclapi.com/oauth/authorise/?client_id={client_id}&state=1"

@app.route('/login')
def uclapi_login():
    return redirect(oauth_url)


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

    # send request to oauth user
    params = {"client_secret": client_secret, "token": token}
    r = requests.get("https://uclapi.com/oauth/user/data", params=params)

    decoded = r.json()

    daoImpl = UserDAOImpl()
    user = User(daoImpl, decoded["upi"])
    user.loadDB()

    user.token = token
    user.session = str(uuid.uuid4())
    user.saveDB()
    daoImpl.destroy()

    print("for user {}, saved token {}, session {}".format(user.id, user.token, user.session))

    return user.session

@app.route('/consolidated_timetable')
def consolidated_timetable():
    session = request.args.get('session', '')
    if session == '':
        abort(401)

    # TODO: ideally, this should be balanced in a queue. hackathon.
    daoImpl = UserDAOImpl()
    user = User(daoImpl, None)
    user.loadFromSessionDB(session)
    token = None

    if user.session != session:
        print("invalid session {}", session)
        daoImpl.destroy
        abort(401)
    else:
        token = user.token
        daoImpl.destroy

    params = {"token": token,
              "client_secret": client_secret,
              "date": None}

    events = []

    # TODO: get @ngenethlis to change his search range
    # to 7 to 14 days from now, so that this part of the
    # code will have meaningful data

    # Gets events
    for i in range(7, 14):
        date = datetime.now()
        date += timedelta(days=i)
        params["date"] = date.strftime("%Y-%m-%d")

        r = requests.get("https://uclapi.com/timetable/personal", params=params)
        res = r.json()

        if not res["ok"]:
            print("error retrieving personal timetable")
            redirect(oauth_url)

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

    # Gets user information
    params = {
        "client_secret": client_secret,
        "token": token
    }
    r = requests.get("https://uclapi.com/oauth/user/data", params)

    # TODO: plaster r.status_code all over the place
    if r.status_code != 200:
        abort(503)

    data = r.json()
    if not data["ok"]:
        redirect(oauth_url)

    return {
        "name": data["given_name"],
        "department": data["department"],
        "events": events
    }
