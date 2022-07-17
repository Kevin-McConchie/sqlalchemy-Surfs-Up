import numpy as np
import pandas as pd
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
Measurement= Base.classes.measurement
Station= Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():

    # Query precipitation values
    data = session.query(Measurement.date, Measurement.prcp)

    # Create dictionary
    prcp={date:prcp for date, prcp in data}
    session.close()

    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stationid():

    # Query station id's values
    data2 = session.query(Station.station, Station.name)
    
    # Create dictionary
    stations={station:name for station, name in data2}
    session.close()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    # set date rage for data
    limit_date = dt.date(2017, 8, 23)- dt.timedelta(days=365)

    # create details for query
    sel = [Measurement.station,
    func.count(Measurement.tobs)]

    # set criteria for most active station
    most_active = session.query(*sel).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.id).desc()).first()
            
    # select information for most active station
    data3 = session.query(Measurement.tobs).\
    filter(Measurement.station == most_active[0]).\
    filter(Measurement.date>=limit_date).all()

    session.close()

    tobs_list = list(np.ravel(data3))
    return jsonify(tobs_list =tobs_list )


# @app.route("/api/v1.0/<start>/<end>")
# def start():
    
#     sel = [func.min(Measurement.tobs),
#     func.max(Measurement.tobs),
#     func.avg(Measurement.tobs)]
    
#     # create start date variable
#     # start_dt= dt.datetime.strftime('%Y-%m-%d')
   
#     if not end:
#     # start = dt.datetime.strptime(start, "%Y%m%d")
#     # set criteria for query

#     # select data for query
#         data4 = session.query(*sel).\
#         filter(Measurement.date >= start).all()
    
#     # create dictionary for query
#     stats=[]
#     for min, max, avg in data4:
#         stats_dict={}
#         stats_dict['TMIN'] = min
#         stats_dict['TMAX'] = max
#         stats_dict['TAVG'] = avg
#         stats.append(stats_dict)
        
        
#     session.close()

#     return jsonify(stats)


@app.route("/api/v1.0/<start>/<end>")
def start():
    
    sel = [func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)]
    
    # create start date variable
    start= dt.datetime.strptime('%Y-%m-%d')
    end= dt.datetime.strptime('%Y-%m-%d')

    # set criteria for query
    sel = [func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)]
    

    # select data for query
    data4 = session.query(*sel).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
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
