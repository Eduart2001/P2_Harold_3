
import datetime
import time
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
   
import ephem
#PyEphem provides an ephem Python package for performing high-precision astronomy computations

def get_moons_in_year(year):
    """Returns a list of the full  in a year. The list contains tuples
        of  the form (DATE,'full')
    """
    moons=[]

    date=ephem.Date(datetime.date(year,1,1))
    while date.datetime().year==year:

        date=ephem.next_full_moon(date)
        localtime=ephem.localtime(date)
        if localtime.year == year:
            # Append the date as a string to the list for easier comparison later
            moons.append( (localtime.strftime("%d/%m/%Y"),'full') )

    moons.sort(key=lambda x: x[1])

    return moons  

def get_full_moon_in_month(year,month):
    """Returns a list of the full moon in a month. The list contains tuples
        of the form (DATE,'full')"""
    date=ephem.Date(datetime.date(year,month,1))
    date=ephem.next_full_moon(date)
    localtime=ephem.localtime(date)
    
    return [(localtime.strftime("%d/%m/%Y"),'full')]

#print(get_full_moon_in_month(2022,1))
# print(get_moons_in_year(2022))

def get_from_db(name,table):
    """Returns a list of str type elements depending of the name given in args, it searches data on the database,
    It selects all id's from the animaux table if name=id and table=animaux for example.

    Args:
        name (str): name to search
        table (str): search table

    Returns:
        list: list of elements depending on the given name argument
    ***raise :ValueError, if there is any problem
    """
    l=[]
    try:
        db=connect_db()
        cursor=db.cursor()
        for i in cursor.execute(f"SELECT {name}  from {table}"):
            l.append(i[0])
        l.sort()
        return l
    except:
        raise ValueError()
    
def graph1(startDate,endDate,famille=None):
    """graph1

    Args:
        startDate (_type_): _description_
        endDate (_type_): _description_
        famille (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    startDate=time.strptime(startDate, "%d/%m/%Y")
    endDate=time.strptime(endDate, "%d/%m/%Y")
    def get_id_from_same_family(name):
        l=[]
        for i in cursor.execute(f"SELECT id from animaux where famille_id =(SELECT id from familles where nom like '{name}')"):
            l.append(i[0])
        return l
    
    d={}
    try:
        db=connect_db()
        cursor=db.cursor()
        if famille==None:
            for i in cursor.execute("SELECT date from velages"):
                temp=time.strptime(i[0], "%d/%m/%Y")
                if temp<=endDate and temp>=startDate :
                    if d.get(i[0],-1)!=-1:
                        a=d[i[0]]+1
                        d[i[0]]=a
                    else:
                        d[i[0]]=1
        else:
            temp_list=get_id_from_same_family(famille)
            for j in temp_list:
                t=cursor.execute(f"SELECT date  from velages WHERE id = (SELECT velage_id FROM animaux_velages WHERE animal_id='{j}')")
                for j in t:
                    temp=time.strptime(j[0], "%d/%m/%Y")
                    if temp<=endDate and temp>=startDate :
                        if d.get(j[0],-1)!=-1:
                            a=d[j[0]]+1
                            d[j[0]]=a
                        else:
                            d[j[0]]=1
        return d
    except:
        return d
#print(graph1("03/10/2000","19/11/2010"))
#print(graph1("03/10/2000","19/11/2010","Bleuet"))#28

def graph2(year,month=None,famille=None):
    d={}

    if month!=None:
        k=get_full_moon_in_month(year,month)
    else:
        k=get_moons_in_year(year)
    l=[x[0] for x in k]
    full_moon=0
    other_day=0
    try:
        
        if month!=None:
            import calendar
            first_day=1
            last_day=calendar.monthrange(year, month)[1]
            d=graph1(f"{first_day}/{month}/{year}",f"{last_day}/{month}/{year}",famille)
            for i in d.keys():
                if i==l[0]:
                    full_moon+=d[i]
                else:
                    other_day+=d[i]
        else:
            d=graph1(f"0{1}/0{1}/{year}",f"{31}/{12}/{year}",famille)
            print(d)
            for i in d.keys():
                if i in l:
                    full_moon+=d[i]
                else:
                    other_day+=d[i]
        return [(full_moon,"full"),(other_day,"other")]
    except:
        return d
    
    
    
print(graph2(2000))
#print(graph1("03/10/2000","19/11/2010"))
#print(graph1("03/10/2000","19/11/2010","Bleuet"))#28
#print(get_full_moon_in_month(2022,1))