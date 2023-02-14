import apprise
import os
import re
import urllib.parse
from flask import Flask, request

if 'SERVICES' in os.environ.keys():
    services = os.environ['SERVICES']
if 'WEBHOOK_BASE_URL' in os.environ.keys():
    webhook_base_url = os.environ['WEBHOOK_BASE_URL']

aplist = dict()

for service in services:
    apobj = apprise.Apprise()
    
    apobj.add(urllib.parse.urljoin(webhook_base_url, service))
    aplist[service] = apobj

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_json(force=True)
    body = data['body']
    service = re.search("(?<=Service )(\S+)", body).group()

    apobj = aplist[service]

    apobj.notify(
        title=data['title'],
        body=data['body'],
    )
    return 'ok'