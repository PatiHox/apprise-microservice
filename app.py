import apprise
import os
import re
from flask import Flask, request

services = ["backend"]
webhook_base_url = "json://localhost:8080/webhook-step/"

if 'SERVICES' in os.environ.keys():
    services = os.environ['SERVICES'].split(',')
if 'WEBHOOK_BASE_URL' in os.environ.keys():
    webhook_base_url = os.environ['WEBHOOK_BASE_URL']

apobj = apprise.Apprise()

for service in services:
    url = webhook_base_url + service
    print (url)
    apobj.add(url, tag=service)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_json(force=True)
    body = data['body']
    try:
        service = re.search("(?<=Service )(\S+)", body).group()

        print ("Received data : " + body + " found service name: " + service)

        apobj.notify(
            title=data['title'],
            body=body,
            tag=service
        )
        return 'ok'
    except:
        print ("Error reading data")

        return 'fail'