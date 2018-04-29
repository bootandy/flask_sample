import os
import sqlite3

from flask import abort, Flask, request

app = Flask(__name__)
app.config['DATABASE'] = 'ref.db'

INSERT_SQL = 'insert into referer (domain, date, creative_size) values (:domain, :date, :creative_size)'
SELECT_ALL_FOR_DOMAIN = 'select domain, date, creative_size from referer where domain = :domain order by date'
SELECT_HISTORY = 'select domain, count(domain) from referer group by domain'
SELECT_CREATIVE_SIZES = 'select domain, creative_size, count(*) from referer group by domain, creative_size'


@app.route('/get/<domain>')
def view_referer(domain):
    return '\n'.join([' '.join(row) for row in _query_db(SELECT_ALL_FOR_DOMAIN, {'domain': domain})])


@app.route('/history')
def view_history():
    return '\n'.join([' '.join(map(str, row)) for row in _query_db(SELECT_HISTORY)])


@app.route('/creative_sizes')
def view_creative_sizes():
    return '\n'.join([' '.join(map(str, row)) for row in _query_db(SELECT_CREATIVE_SIZES)])


@app.route('/new_data', methods=['POST'])
def post_to_db():
    data_dict = request.get_json() or {}
    ref = data_dict.get("headers", {}).get("Referer")
    date = data_dict.get("date")
    creative_size = data_dict.get("creative_size")
    if not ref:
        abort(400, "No referer")
    if not date:
        abort(400, "No date")
    if not creative_size:
        abort(400, "No creative_size")

    if ref and date and creative_size:
        _get_db(INSERT_SQL, {'domain': ref, 'date': date, 'creative_size': creative_size})
        return "Data inserted"
    abort(400, "Failed to insert")


def _set_up_db(db):
    qry = open('schema.sql', 'r').read()
    c = db.cursor()
    c.executescript(qry)


def _query_db(query, args=(), one=False):
    cur = _get_db(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def _get_db(sql, data):
    db_name = app.config['DATABASE']
    if not os.path.isfile(db_name):
        with sqlite3.connect(db_name) as conn:
            _set_up_db(conn)
    with sqlite3.connect(db_name) as conn:
        return conn.execute(sql, data)
