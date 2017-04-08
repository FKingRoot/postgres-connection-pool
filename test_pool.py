#!/usr/bin/env python
# coding=utf-8

"""
test the db pool
"""

import pytest

from dbpool import get_cursor, get_dict_cursor


@pytest.fixture(scope="session")
def db():
    with get_cursor() as cur:
        cur.execute(u"""\
DROP TABLE IF EXISTS t1
""")
        cur.execute(u"""\
CREATE TABLE t1 (
id uuid DEFAULT uuid_generate_v4(),
data text)
""")
        cur.execute(u"""\
INSERT INTO t1
(data)
VALUES
('abc'),
('def'),
('ghi')
""")


def test_get_cursor(db):
    with get_cursor() as cur:
        cur.execute(u"""\
SELECT 1
""")
        assert cur.fetchone()[0] == 1

    with get_cursor() as cur:
        cur.execute(u"""\
SELECT data FROM t1 ORDER BY data
""")
        r = cur.fetchall()
        assert r[0][0] == "abc"
        assert r[1][0] == "def"
        assert r[2][0] == "ghi"


def test_get_dict_cursor(db):
    with get_dict_cursor() as cur:
        cur.execute(u"""\
SELECT data FROM t1 ORDER BY data
""")
        r = cur.fetchall()
        # r[0] is of type psycopg2.extras.DictRow, not a raw python dict.
        assert r[0]['data'] == "abc"
        assert dict(r[0]) == {'data': "abc"}
        assert r[1]['data'] == "def"


def test_abort_on_exception(db):
    try:
        with get_cursor() as cur:
            cur.execute(u"""\
INSERT INTO t1
(data)
VALUES
('jkl')
""")
            1 / 0                   # raise exception
    except ZeroDivisionError:
        pass
    with get_cursor() as cur:
        cur.execute(u"""\
SELECT data FROM t1 WHERE data = 'jkl'
""")
        r = cur.fetchone()
        assert r is None


def test_insert_new_data(db):
    with get_cursor() as cur:
        cur.execute(u"""\
INSERT INTO t1
(data)
VALUES
('mno')
""")
    with get_cursor() as cur:
        cur.execute(u"""\
SELECT data FROM t1 WHERE data = 'mno'
""")
        r = cur.fetchone()
        assert r[0] == 'mno'
