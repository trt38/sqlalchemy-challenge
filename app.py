import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#Flask Setup
app = Flask(__name__)

#Create home route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

Create Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create new session
    session = Session(engine)
    #Query prcp measurement in last 12 months
    date = dt.datetime(2017, 8, 23)
    year_ago = date - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date <= date).filter(Measurement.date > year_ago).all()
    
    session.close()
    
    #Create Dictionary
    all_precip = []
    for result in results:
        precip_dict = {}
        precip_dict["date"] = result.date
        precip_dict["prcp"] = result.prcp
        all_precip.append(precip_dict)
    
    return jsonify(dict(all_precip))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.name).all()
    session.close()
    
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    date = dt.datetime(2017, 8, 23)
    year_ago = date - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date <= date).\
    filter(Measurement.date > year_ago).\
    filter(Measurement.station == "USC00519281").all()
    session.close()
    
    temps = [int(result[1]) for result in results]
    
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
     def start_temp(start):
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        
        tmin = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all
        tavg = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all
        tmax = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all
       
        session.close()
        
        temps_dict = {temps_dict["Temp (Min)"]: tmin, 
                     temps_dict["Temp (Avg)"]: tavg,
                     temps_dict["Temp (Max)"]: tmax}
                
        return jsonify(temps_dict)
     
@app.route("/api/v1.0/temps/<start_date>/<end_date>")
    def start_end(start, end):
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(start, '%Y-%m-%d')
        
        tmin = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all
        tavg = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all
        tmax = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all
       
        session.close()
        
        temps_dict = {temps_dict["Temp (Min)"]: tmin, 
                     temps_dict["Temp (Avg)"]: tavg,
                     temps_dict["Temp (Max)"]: tmax}
                
        return jsonify(temps_dict)
     
        

if __name__ == "__main__":
    app.run(debug=False)