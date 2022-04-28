import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
from . import db as database


app=database.get_App()

@app.route('/')
def index():
    keys=database.graph0().keys()
    values=database.graph0().values()
    print(keys,values)
    return render_template("index.html",familles=database.get_from_db("nom","familles"),keys=keys,values=values,types=database.get_from_db("type","types"))

@app.route('/',methods=['POST','GET'])
def graphics():
    pass
