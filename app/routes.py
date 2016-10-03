import sqlite3

from contextlib import closing
from flask import (
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash
)


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = "HELLO, WORLD"
USERNAME = "piper"
PASSWORD = "password"

app = Flask(__name__)
app.config.from_object(__name__)

def db_connect():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(db_connect()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = db_connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

if __name__ == '__main__':
    app.run()