#!/usr/bin/env python
import json
import psycopg2
from pytz.reference import UTC
import requests

from datetime import datetime

from settings import DB_NAME, DB_TABLE, LOCATION, API_URL, API_USER, API_PASS

def serializer(obj):
    if isinstance(obj, datetime):
        serial = obj.replace(tzinfo=UTC).isoformat()
        return serial
    else:
        return obj

print API_URL + 'latest/'
response = requests.get(API_URL + 'latest/')

if response.status_code == 404:
    latest = False
else:
    latest = response.json()['timestamp']
    
conn = psycopg2.connect("dbname='%s'" % DB_NAME)
cur = conn.cursor()

select_stmt = "SELECT * FROM %s" % DB_TABLE

if latest:
    cur.execute(select_stmt + " WHERE timestamp > %s", (latest, ))
else:
    cur.execute(select_stmt)

rows = cur.fetchall()

cur.close()
conn.close()

data = json.loads(json.dumps({
    'count': len(rows),
    'location': LOCATION,
    'rows': rows
}, default=serializer))

request = requests.post(API_URL + 'ingest/', auth=(API_USER, API_PASS), json=data)

if request.status_code != 200:
    print request.text
