import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import pytz

webhook_url = "SLACK WEB HOOK HERE"

bleep_prev_title = None
bleep_prev_link = None
thehacker_prev_title = None
thehacker_prev_link = None

while True:
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    req = requests.get("https://www.bleepingcomputer.com/feed/", headers = user_agent)
    soup = BeautifulSoup(req.content, features='xml')
    items = soup.findAll('item')



    bleep_title = items[0].find('title').text
    bleep_link = items[0].find('link').text

    if bleep_title != bleep_prev_title or bleep_link != bleep_prev_link:

            bleep_prev_title = bleep_title
            bleep_prev_link = bleep_link

            message = {"text": "News!!!\n\n News Title: " + bleep_title + "\nNews Address: " + bleep_link}
            response = requests.post(
                webhook_url, data=json.dumps(message),
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

    req = requests.get("https://feeds.feedburner.com/TheHackersNews", headers = user_agent)
    soup = BeautifulSoup(req.content, features='xml')
    items = soup.findAll('item')

    thehacker_title = items[0].find('title').text
    thehacker_link = items[0].find('link').text

    if thehacker_title != thehacker_prev_title or thehacker_link != thehacker_prev_link:

            thehacker_prev_title = thehacker_title
            thehacker_prev_link = thehacker_link

            message = {"text": "News!!!\n\n News Title: " + thehacker_title + "\nNews Address: " + thehacker_link}
            response = requests.post(
                webhook_url, data=json.dumps(message),
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

    tz = pytz.timezone("Europe/Istanbul")
    now = datetime.now(tz)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    f = open("news_log.txt", "a")
    out = "Job Time: " + dt_string + "\n"
    print(out)
    f.write(out)
    f.close()

    time.sleep(1800)
