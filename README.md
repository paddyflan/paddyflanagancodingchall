# paddyflanagancodingchall

To query the sensor data, a get request is sent using the command "requests.get(BASE + "query/", data)" where BASE= URL that API runs on, and 'data' is a dictionary in the form 'data={'sensors':'0,2,1', 'metrics':'humidity,wind_speed', 'startdate':2, 'enddate':3}'
'sensors' represent a string of the sensors wanting to be queired separated by ','
'metrics' represents a string of the metrics wanting to be queried separated by ','
'startdate' represents the day number you would like to begin from
'enddate' represents the daynumber you woud like to query to

a response will be returned in the form of a dictionary representing the sensors queried and the corresponding averages of the metrics queried, as so:
{'sensor 0': {'humidity': 7.199999999999999, 'wind_speed': 4.5}, 'sensor 2': {'humidity': 12.2, 'wind_speed': 34.4}, 'sensor 1': {'humidity': 19.0, 'wind_speed': None}}
