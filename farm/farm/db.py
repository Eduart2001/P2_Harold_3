
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
def get_min_year():
    try:
        db=connect_db()
        min_year=9999
        cursor=db.cursor()
        for i in cursor.execute("SELECT date from velages"):
            k=time.strptime(i[0], "%d/%m/%Y")
            if k[0]<min_year:
                min_year=k[0]
        return int(min_year)
    except:
        raise ValueError
    
def get_max_year():
    try:
        db=connect_db()
        max_year=0
        cursor=db.cursor()
        for i in cursor.execute("SELECT date from velages"):
            k=time.strptime(i[0], "%d/%m/%Y")
            if k[0]>max_year:
                max_year=k[0]
        return int(max_year)
    except:
        raise ValueError


def graph0():
    """graph0, is a function to show data about the flow of birth through decades.
       it uses 2 functions to get the max and min year in the db.
       than creates a dictionnary of decades.
       
    Raises:
        ValueError: **

    Returns:
        dictionnary: dictionnary of born calvings through decades
    """
    try:
        d={}
        db=connect_db()
        cursor=db.cursor()
        min=(get_min_year()//10)*10-10
        max=((get_max_year()//10)*10)
        
        for i in range(max,min,-10):
            d[i]=0
            
        for i in cursor.execute("SELECT date from velages"):
            temp=time.strptime(i[0], "%d/%m/%Y")
            for j in d.keys():
                
                if temp>=time.strptime("01/01/"+str(j),"%d/%m/%Y"):
                    d[j]=d[j]+1
                    break
        return d
    except:
        raise ValueError()

def graph1(startDate,endDate,famille=None):
    """graph1 function helps to extract necessary data, it shows the number of born calvings through one specified periode
       the search could be specified to a single family, if none it will show all

    Args:
        startDate str: the date that the periode search starts
        endDate str: the date that the periode search ends
        famille str: name of calvings family . Defaults to None.

    Returns:
        dictionnary: where the key is the date and the value is the number of clavings born on that day
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
    """graph2 function helps to extract necessary data, it shows the number of born calvings on a full moon and
       the number of born calvings outside the full moon, through one specified periode
       the search could be specified to a single family, if none it will show all
       if month == None : it means that we will look through the year else: through the month of that year

    Args:
        year int: the year to search for the full moon
        month int: the month to search for the full moon. Defaults to None.
        famille str: name of calvings family . Defaults to None.

    Returns:
        list: with 2 tuples the 1st one contains the number of the calvings born on the full moon, and the text 'full moon' the 
              2nd contains the calvings born outside the full moon, and the text 'other'
    """
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
        raise ValueError
    
    
    
#print(graph2(2000))
#print(graph1("03/10/2000","19/11/2010"))
#print(graph1("03/10/2000","19/11/2010","Bleuet"))#28
#print(get_full_moon_in_month(2022,1))