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
    return render_template("index.html", familles=database.get_from_db("nom", "familles"),types=database.get_from_db("type", "types"),keys=keys, values=values, min=min, max=max)


@app.route('/charts', methods=['GET', 'POST'])
def charts():
    if request.method == "POST":
        chartId = request.form["chartId"]
        start_month = request.form["start_month"]
        start_year = request.form["start_year"]
        start_date = "01/"+start_month+"/"+start_year
        end_date = request.form["end_date"]
        family_filter = request.form["family_filter"]
        fullmoon = request.form['fullMoon']
        race=request.form["race"]
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
                return jsonify({'error': 'Missing data!'})
        elif int(chartId) == 2:
            if start_month == "":
                chart2 = database.graph2(
                    int(start_year), None, family_filter, fullmoon)
            else:
                try:
                    chart2 = database.graph2(
                        None, int(start_month), family_filter, fullmoon)
                except:
                    return jsonify({'error': 'Missing data!'})
            keys = chart2.keys()
            values = chart2.values()
            if(fullmoon != ""):
                return jsonify({"chartId": 2, "keys": str(keys), "values": str(values)})
            else:
                return jsonify({'error': 'Missing data!'})
        elif int(chartId)==3:
            print(race,percentage)
            return jsonify({'error': 'Missing data!'})
        else:
            return jsonify({'error': 'Missing data!'})

        return jsonify({'output': [str(), str()]})
