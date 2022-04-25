import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
import click
from flask.cli import with_appcontext

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file 

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'farm.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FARM_SETTINGS', silent=True)

def get_App():
    return app

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init_db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
          
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)






'''-------------------------------------------------------------------------------------------------------------
   ----------------------------------GETTERS AND SETTERS FOR DATA IN DATABASE-----------------------------------
   -------------------------------------------------------------------------------------------------------------'''
   
   
def get_from_db(name,table):
    l=[]
    try:
        db=connect_db()
        print(db)
        cursor=db.cursor()
        print(cursor)
        for i in cursor.execute(f"SELECT {name}  from {table}"):
            l.append(i[0])
        l.sort()
        return l
    except:
        return l
    
        