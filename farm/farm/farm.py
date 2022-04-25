import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
from farm import db as database


app=database.get_App()

@app.route('/')
def index():
    return render_template("index.html",familles=database.get_from_db("nom","familles"))

@app.route('/',methods=['POST','GET'])
def graphics():
    pass