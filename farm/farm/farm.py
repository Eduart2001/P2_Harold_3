import os
import sqlite3
from winreg import EnableReflectionKey
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from . import db as database
import time


app = database.get_App()


@app.route('/')
def index():
    """When the application is launched this function is launched.
       By default it shows the base chart that shows data from the database of all velages born through decades

    Returns:
        render_template : to index.html
    """
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
        
        race1=request.form["raceType1"]
        race2=request.form["raceType2"]
        race3=request.form["raceType3"]
        percentage=request.form["percentage"]
        
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
        elif int(chartId) == 3:
            if percentage=="":
                print("OK")
                return jsonify({'error':"dict_values("+"percentage-select"+")"})
            if race1=="-1" and race2=="-1"and race3=="-1":
                l="raceType1-select,raceType2-select,raceType3-select"
                return jsonify({'error':"dict_values("+str(l)+")"})
            try:
                if float(percentage)<0:
                    chart3=database.graph3(int(race1),int(race2),int(race3),-float(percentage),True)
                else:
                    chart3=database.graph3(int(race1),int(race2),int(race3),float(percentage),False)
                keys=chart3.keys()
                values=chart3.values()
                return jsonify({"chartId": 3, "keys": str(keys), "values": str(values)})
            except:
                return jsonify({'error': 'Missing data!'})
        else:
            index()
