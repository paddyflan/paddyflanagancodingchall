from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy.sql import func



app = Flask(__name__)
api = Api(app)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# design models

#model for the sensor
class SensorModel(db.Model):
    __tablename__ = 'sensor'
    s_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    metrics = db.relationship('Metrics', backref='sensor')  #relationsjip between metrics model



#to parse through sensor args when registering new sensor
# must include all arguments or system will abort
sensor_put_args = reqparse.RequestParser()
sensor_put_args.add_argument("country", type=str, help="country name is required", required=True)
sensor_put_args.add_argument("city", type=str, help="city name is required", required=True)

resource_fields = {
	's_id': fields.Integer,
	'country': fields.String,
	'city': fields.String,
}


#model for the metrics
class Metrics(db.Model):
    __tablename__ = 'metrics'
    m_id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('sensor.s_id'), nullable=False)
    temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    daynumber = db.Column(db.Integer, nullable=False)


#to parse through the metrics args
# must inlude sensor id and day number or system will abort
metrics_put_args = reqparse.RequestParser()
metrics_put_args.add_argument("s_id", type=int, help="sensor id is required", required=True)
metrics_put_args.add_argument("temp", type=float, help="temperature")
metrics_put_args.add_argument("humidity", type=float, help="humidity")
metrics_put_args.add_argument("wind_speed", type=float, help="wind speed")
metrics_put_args.add_argument("daynumber", type=int, help="day number is required", required=True)

resource_fields2 = {
    'm_id': fields.Integer,
    's_id': fields.Integer,
	'temp': fields.Float,
	'humidity': fields.Float,
    'wind_speed': fields.Float,
    'daynumber': fields.Integer
}


#to parse through the query args
#if any argument is not included system will abort
query_get_args = reqparse.RequestParser()
query_get_args.add_argument("sensors", type=str, help="sensors is required", required=True)
query_get_args.add_argument("metrics", type=str, help="metrics is required", required=True)
query_get_args.add_argument("startdate", type=int, help="start date is required", required=True)
query_get_args.add_argument("enddate", type=int, help="end date is required", required=True)

resource_fields3 = {
    'sensors': fields.String,
	'metrics': fields.String,
	'startdate': fields.Integer,
    'enddate': fields.Integer
}


#create database only needs to be done once
db.create_all()


#class to register sensor
class registerSensor(Resource):
    @marshal_with(resource_fields)
    def post(self, sensor_id):
        args = sensor_put_args.parse_args()
        result = SensorModel.query.filter_by(s_id=sensor_id).first()

        # if sensor ID is already taken abort with status code 409
        if result:
            abort(409, message="sensor id taken...")

        # else register sensor
        sensor = SensorModel(s_id=sensor_id, country=args['country'], city=args['city'])
        db.session.add(sensor)
        db.session.commit()

        # return the parameters of the newly registered sensor along with status code 201
        return sensor, 201

# class to add a new metric to the database
class addMetric(Resource):
    @marshal_with(resource_fields2)
    def post(self, metric_id):
        args = metrics_put_args.parse_args()
        sensor = SensorModel.query.filter_by(s_id=args['s_id']).first()

        # if sensor id not in databse abort with status code 404
        if not sensor:
            abort(404, message="could not find sensor with that id...")
        met = Metrics.query.filter_by(m_id=metric_id).first()

        #if metric id is already taken abort with status code 409
        if met:
            abort(409, message="metric id taken...")

        #else add this newly recorded metric to the database
        newmetric = Metrics(m_id=metric_id, s_id=args['s_id'], temp=args['temp'], humidity=args['humidity'], wind_speed=args['wind_speed'], daynumber=args['daynumber'])
        db.session.add(newmetric)
        db.session.commit()

        # return parameters of the newly added metric along with  status code 201
        return newmetric, 201


#class to query the sensors
class querySensors(Resource):
    #@marshal_with(resource_fields2)
    def get(self):
        
        #dictionary result to return stored here
        finalresult={}
        args = query_get_args.parse_args()


        sensorids= args['sensors'].split(',')
        #parse through each sensor to be queried
        for x in sensorids:
            sensorid=int(x)

            metrics = Metrics.query.filter(Metrics.daynumber >= args['startdate'], Metrics.daynumber<= args['enddate'], Metrics.s_id==sensorid).all()
            #if there is no metric within the date range and with that sensor id then abort with status code 404
            if not metrics:
                abort(404, message="could not find sensor with that id in that date range...")

            #else parse through the different metrics for that sensor in that date range
            metss= args['metrics'].split(',')
            result={}
            for met in metss:
                finalval=0
                number=0

                #for chosen metric, parse through the database metrics and find average value for chosen metric
                #add this average value of chosen metric to a dictionary
                for i in range(len(metrics)):

                    if getattr(metrics[i], met):
                        number=number+1
                        finalval= finalval+ getattr(metrics[i], met)
                if number == 0:
                    number = None
                    result[met]=None
                else:
                    average= finalval/number
                    result[met]= average
                
            finalresult['sensor '+str(sensorid)] = result

        #return the dictionary of average values of queried metrics for each queried sensors
        return finalresult



# add the endpoints to the API
api.add_resource(registerSensor, '/regsensor/<int:sensor_id>')
api.add_resource(addMetric, '/addmetric/<int:metric_id>')
api.add_resource(querySensors, '/query/')

if __name__ == "__main__":
    app.run(debug=True)
