#!/usr/bin/env python
# coding=utf-8

"""wrap psycopg2 threaded connection pool using contextmanager.

see example usage in test_pool.py

"""

from contextlib import contextmanager

import psycopg2.pool
import psycopg2.extras


POOL = None
CONF = {
    "db.poolmin": "3",
    "db.poolmax": "10",
    "db.host": "localhost",
    "db.port": "5432",
    "db.name": "t1",
    "db.user": "t1",
    "db.password": "fNfwREMqO69TB9YqE+/OzF5/k+s=",
}


def _get_pool():
    global POOL
    if not POOL:
        POOL = psycopg2.pool.ThreadedConnectionPool(
            int(CONF.get("db.poolmin", 3)),
            int(CONF.get("db.poolmax", 10)),
            host=CONF.get("db.host", "localhost"),
            port=int(CONF.get("db.port", "5432")),
            database=CONF.get("db.name"),
            user=CONF.get("db.user"),
            password=CONF.get("db.password"))
    return POOL


@contextmanager
def get_conn():
    conn = _get_pool().getconn()
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        POOL.putconn(conn)


@contextmanager
def get_cursor():
    with get_conn() as conn:
        yield conn.cursor()


@contextmanager
def get_dict_cursor():
    with get_conn() as conn:
        yield conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
