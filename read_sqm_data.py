#!/usr/bin/env python
import psycopg2
import re
import socket
import time

from settings import SQM_IP, SQM_PORT, DB_NAME, DB_TABLE, INTERVALL

# r, 00.00m,0000722291Hz,0000000000c,0000000.000s, 031.5C
prog = re.compile(r'(\d+\.\d+)m.*?(\d+)Hz.*?(\d+)c.*?(\d+\.\d+)s.*?(\d+\.\d+)C')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SQM_IP, SQM_PORT))

conn = psycopg2.connect("dbname='%s'" % DB_NAME)
cur = conn.cursor()

while 1:
    s.sendall('rx')
    string = s.recv(1024)

    match = prog.search(string)
    if match:
        try:
            values = {
                'magnitude': float(match.group(1)),
                'frequency': int(match.group(2)),
                'counts': int(match.group(3)),
                'period': float(match.group(4)),
                'temperature': float(match.group(5))
            }

            insert_stmt = 'INSERT INTO %s ' % DB_TABLE
            insert_stmt += '(magnitude, frequency, counts, period, temperature) '
            insert_stmt += 'VALUES (%(magnitude)s, %(frequency)s, %(counts)s, %(period)s, %(temperature)s)'

            cur.execute(insert_stmt, values)
            conn.commit()
        except ValueError:
            pass

    time.sleep(INTERVALL)
