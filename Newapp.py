import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,


##Creating the engine 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Importing the database 
Base = automap_base()

#Reflecting the tables
Base.prepare(engine, reflect=True)

#Saving the base 
Passenger = Base.classes.measurement

#Createing the session
session = Session(engine)

#Setting up the Flask APP

app = Flask(__name__)

#Adding the home Route
@app.route("/")
def Homes():
    "Api Routes"
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

#Adding the precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    "Precipitation names"
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Meausurement.date >= '2016-10-01').\
        group_by(Measurement.date).all()
    all_precipitation = []
    for result in results:
        precipitation_dict = {}
        precipitation_dict["date"] = result[0]
        precipitation_dict["prcp"] = result[1]
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

#Adding the Stations Route
@app.route("/api/v1.0/stations")
def stations():
    "Stations"
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    all_sessions = list(np.ravel(results))
    return jsonify(all_sessions)

#Adding the temperature Route
@app.route("/api/v1.0/tobs")
def tobs():
    """Temperature observations (tobs) for last year"""
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-10-01').all()

    all_tobs = []

    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result[0]
        tobs_dict["tobs"] = result[1]
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

#Adding the max min and averge temperture Route
@app.route("/api/v1.0/<start>")
def start(start):
    """The list of the mtemp, the average temp, and maxtem"""
    year, month, date = map(int, start.split('-'))
    date_start = dt.date(year,month,day)
    # Query for tobs of defined start date
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs).\
                            func.avg(Measurement.tobs)).filter(Measurement.date >= date_start).all()
    data = list(np.ravel(results))
    return jsonify(data)

#Adding the max min and averge temperture Route
@app.route("/api/v1.0/<start>/<end>")
def range_temp(start,end):
    """The list of the mtemp, the average temp, and maxtem"""
    year, month, date = map(int, start.split('-'))
    date_start = dt.date(year,month,day)
    year2, month2, date2 = map(int, end.split('-'))
    date_end = dt.date(year2,month2,day2)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs).\
                            func.avg(Measurement.tobs)).filter(Measurement.date >= date_start).filter(Measurement.date <= date_end).all()
    data = list(np.ravel(results))
    return jsonify(data)

#Run the App
if __name__ == '__main__':
    app.run(debug=True)
