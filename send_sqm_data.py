#!/usr/bin/env python
import json
import psycopg2
from pytz.reference import UTC
import requests

from datetime import datetime

from settings import DB_CONNECTION, DB_TABLE, API_URL, API_USER, API_PASS, API_LOCATION


def serializer(obj):
    if isinstance(obj, datetime):
        serial = obj.replace(tzinfo=UTC).isoformat()
        return serial
    else:
        return obj

response = requests.get(API_URL + 'latest/?location=' + API_LOCATION)

if response.status_code == 404:
    latest = False
else:
    latest = response.json()['timestamp']

conn = psycopg2.connect(DB_CONNECTION)
cur = conn.cursor()

select_stmt = "SELECT * FROM %s" % DB_TABLE
if latest:
    select_stmt += ' WHERE timestamp > \'%s\'' % latest
select_stmt += ' ORDER BY timestamp limit 100000'

cur.execute(select_stmt)

rows = cur.fetchall()

cur.close()
conn.close()

data = json.loads(json.dumps({
    'count': len(rows),
    'location': API_LOCATION,
    'rows': rows
}, default=serializer))

request = requests.post(API_URL + 'ingest/', auth=(API_USER, API_PASS), json=data)

if request.status_code != 200:
    print request.text
