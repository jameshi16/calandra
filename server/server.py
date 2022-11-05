from flask import Flask, redirect, request
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
app = Flask(__name__)
token = None

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

    print(decoded) # access token here
    token = decoded['token']
    return token

@app.route('/demo')
def demo():
    global token
    # e.g. request an auth token behind-the-scenes
    params = {"token": token,
              "client_secret": client_secret,
              "date": "2022-10-31"}

    r = requests.get("https://uclapi.com/timetable/personal", params=params)
    return r.json() # your timetable!
