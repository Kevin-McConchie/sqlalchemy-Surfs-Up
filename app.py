import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement= Base.classes.measurement
station= Base.classes.station

 # Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Date and preciptation information: /api/v1.0/precipitation<br/>"
        f"Station id and name: /api/v1.0/stations<br/>"
        f"Dates and temperature obs for most active station from last 12 months: /api/v1.0/tobs<br/>"
        f"Min. Max. and Avg. tempratures for given start date: /api/v1.0/yyyy-mm-dd<br/>"
        f"Min. Max. and Avg. tempratures for given start and end date:/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def prcp():

    # Query precipitation values
    data = session.query(measurement.date, measurement.prcp)

    # Create dictionary
    prcp={date:prcp for date, prcp in data}
    session.close()

    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stationid():

    # Query station id's values
    data2 = session.query(station.station, station.name)
    
    # Create dictionary
    stations={station:name for station, name in data2}
    session.close()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    # set date rage for data
    limit_date = dt.date(2017, 8, 23)- dt.timedelta(days=365)

    # create details for query
    sel = [measurement.station,
    func.count(measurement.tobs)]

    # set criteria for most active station
    most_active = session.query(*sel).\
            group_by(measurement.station).\
            order_by(func.count(measurement.id).desc()).first()
            
    # select information for most active station
    data3 = session.query(measurement.tobs).\
    filter(measurement.station == most_active[0]).\
    filter(measurement.date>=limit_date).all()

    session.close()

    tobs_list = list(np.ravel(data3))
    return jsonify(tobs_list =tobs_list )


@app.route("/api/v1.0/start")
def start(start_dt):
    
    # create start date variable
    start_dt= dt.datetime.strptime('%Y-%m-%d')

    # set criteria for query
    sel = [measurement.date,measurement.tobs,
    func.min(measurement.tobs),
    func.max(measurement.tobs),
    func.avg(measurement.tobs)]
    
    # select data for query
    data4 = session.query(*sel).\
        filter(measurement.date >= start_dt).all()
    
    # create dictionary for query
    stats=[]
    for min, max, avg in data4:
        stats_dict={}
        stats_dict['TMIN'] = min
        stats_dict['TMAX'] = max
        stats_dict['TAVG'] = avg
        stats.append(stats_dict)
        
        
    session.close()

    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
