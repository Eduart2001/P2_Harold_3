import os
import sqlite3
from winreg import EnableReflectionKey
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from . import db as database
import time


app = database.get_App()


@app.route('/')
def index():
    keys = database.graph0().keys()
    values = database.graph0().values()
    min = database.get_min_year()
    max = database.get_max_year()
    familles=database.get_from_db("nom", "familles")
    return render_template("index.html", familles=familles, keys=keys, values=values, min=min, max=max)


@app.route('/charts', methods=['GET', 'POST'])
def charts():
    if request.method == "POST":
        
        chartId = request.form["chartId"]
        
        start_month = request.form["start_month"]
        start_year = request.form["start_year"]
        start_date = "01/"+start_month+"/"+start_year
        
        end_month=request.form["end_month"]
        end_year=request.form["end_year"]
        end_date = end_month+"/"+end_year
        
        family_filter = request.form["family_filter"]
        fullmoon = request.form['fullMoon']
        
        
        if family_filter == "":
            family_filter = None
            
        if int(chartId) == 0:
            keys = database.graph0().keys()
            values = database.graph0().values()
            return jsonify({"chartId": 0, "keys": str(keys), "values": str(values)})
        elif int(chartId) == 1:
            try:
                chart1 = database.graph1(start_date, end_date, family_filter)
                return jsonify({"chartId": 1, "keys": str(chart1.keys()), "values": str(chart1.values())})
            except:
                l=""
                if start_month=="":
                    l+='start-month-select,'
                if end_month=="":
                    l+='end-month-select,'
                if start_year=="":
                    l+='start-year-select,'
                if end_year=="":
                    l+='end-year-select,'
                
                return jsonify({'error':"dict_values("+l+")"})
        elif int(chartId) == 2:
            if start_month == "":
                start_month=None
            else:
                start_month=int(start_month)
            try:
                if fullmoon!="-1":
                    chart2 = database.graph2(int(start_year), start_month, family_filter, fullmoon)
                else:
                    raise ValueError
            except:
                l=""
                if start_year=="":
                    l+='start-year-select,'
                if fullmoon=="-1":
                    l+='fullmoon-select,'
                return jsonify({'error':"dict_values("+l+")"})
            
            
            keys = chart2.keys()
            values = chart2.values()
            if(fullmoon != ""):
                return jsonify({"chartId": 2, "keys": str(keys), "values": str(values)})
            else:
                return jsonify({'error': 'Missing data!'})
        else:
            return jsonify({'error': 'Missing data!'})

        return jsonify({'output': [str(), str()]})
