#!/usr/bin/env python
import psycopg2

from settings import DB_CONNECTION, DB_TABLE

create_stmt = '''
CREATE TABLE %(table)s (
    id           serial primary key,
    timestamp    timestamp without time zone default (now() at time zone 'utc'),
    magnitude    double precision,
    frequency    integer,
    counts       integer,
    period       double precision,
    temperature  double precision
);
CREATE INDEX ON %(table)s("timestamp");
''' % {
    'table': DB_TABLE
}

conn = psycopg2.connect(DB_CONNECTION)
cur = conn.cursor()
cur.execute(create_stmt)
conn.commit()
