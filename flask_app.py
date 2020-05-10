
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for, current_app, g
from flask.cli import with_appcontext

import sqlite3
import click

app = Flask(__name__)
app.config["DEBUG"] = True


DATABASE = '/home/src/mysite/mytest.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_comments():
    cur = get_db().execute('SELECT content FROM comments')
    rv = cur.fetchall()
    cur.close()
    return rv

def set_comments(content):
    if len(content) != 0:
#        get_db().execute('INSERT INTO comments(content) VALUES("' + content + '")')
        get_db().execute('INSERT INTO comments(content) VALUES(?)', (content,))
        get_db().commit()



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        my_comments = get_comments()
        return render_template("main_page.html", comments=my_comments)

    set_comments(request.form["contents"])
    return redirect(url_for('index'))


@app.route('/test')
def test_page():
    return '<h1>This is a test</h1>'
