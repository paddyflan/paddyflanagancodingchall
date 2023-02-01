# paddyflanagancodingchall

For this project a REST API was created with Flask and SQLAlchemy to register sensors, add metrics to the sensors and then query the sensor data for the average value of the metrics over a specified date range.

## Requirements
* Flask
* Flask-Restful
* Flask-SQLAlchemy

## Usage 
To run the API, execute the following command in terminal 
python3 main.py

To then generate the test cases execute the following command in a separate terminal window__
python3 test.py__
Three sensors will be registered to the database__
Next press enter in the terminal window__
New metrics will then be added to the database__
Next press enter again in the database__
This will query the database for the following cases__
data = {'sensors':'0,2,1', 'metrics':'humidity,wind_speed', 'startdate':2, 'enddate':3}__
and data2 = {'sensors':'0,2', 'metrics':'wind_speed', 'startdate':1, 'enddate':3}__

A response will be returned in the form of a dictionary representing the sensors queried and the corresponding averages of the metrics queried

The test.py file can be altered to register different sensors, add different metrics and create different queries.
