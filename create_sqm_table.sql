CREATE TABLE sqm_babelsberg (
    id           serial primary key, 
    timestamp    timestamp without time zone default (now() at time zone 'utc'),
    magnitude    double precision,
    frequency    integer,
    counts       integer,
    period       double precision,
    temperature  double precision
);
