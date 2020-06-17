# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# 2. Create the date_precipitation dictionary

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# 3. Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""

    return jsonify(dict(session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()))


@app.route("/api/v1.0/stations")
def station():
    """Return the station data as json"""

    return jsonify(dict(session.query(Measurement.station).group_by(Measurement.station).all()))

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature data from most active station as json"""

    return jsonify(dict(session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-18').order_by(Measurement.date.desc()).all()))

@app.route("/api/v1.0/<start>")
def start(start):
    """Fetch the minimum temperature, the average temperature, and the max temperature for dates after a given start date."""
    
    return jsonify(dict(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Fetch the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""

    return jsonify(dict(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()))


if __name__ == "__main__":
    app.run(debug=True)
