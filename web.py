import os
import sqlite3

from flask import abort, Flask, request

app = Flask(__name__)
app.config['DATABASE'] = 'docs'

INSERT_SQL = 'insert into documents (title, content) values (:title, :content)'
SELECT_ALL_SQL = 'select distinct(title) from documents'
SELECT_EXACT_DOC = 'select content from documents where title = :title order by create_time desc limit 1'
SELECT_EXACT_DOC_BY_TIME = 'select content from documents where title = :title and create_time = :create_time'
SELECT_BY_TITLE = 'select create_time from documents where title = :title'


@app.route('/documents')
def list_all_documents():
    return '\n'.join([user[0] for user in _query_db(SELECT_ALL_SQL)])


@app.route('/documents/<title>')
def list_document_revisions(title):
    revivisons = [user[0] for user in _query_db(SELECT_BY_TITLE , {'title': title})]
    if revivisons:
        return "Versions for document with title %s:\n%s" % (title, '\n'.join(revivisons))
    abort(404)


@app.route('/documents/<title>/<timestamp>')
def get_document_at_time(title, timestamp):
    content = _query_db(SELECT_EXACT_DOC_BY_TIME, {'title': title, 'create_time': timestamp}, one=True)
    if content is not None:
        return content
    abort(404)


@app.route('/documents/<title>/latest')
def get_latest_document(title):
    content = _query_db(SELECT_EXACT_DOC, {'title': title}, one=True)
    if content is not None:
        return content
    abort(404)


@app.route('/documents/<title>', methods=['POST'])
def post_to_db(title):
    data_dict = request.get_json() or {}
    content = data_dict.get("content")
    if content:
        _get_db(INSERT_SQL, {'title': title, 'content': content})
        return "Data inserted"
    abort(400, "No insert: No content passed in")


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
