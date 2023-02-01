import requests
import json

BASE = 'http://127.0.0.1:5000/'



#test data to register new sensors
data = [{'country': 'Ireland', 'city': 'Dublin'}, 
        {'country': 'Ireland', 'city': 'Cork'}, 
        {'country': 'France', 'city': 'Paris'}]


#i reresents the sensor id
for i in range(len(data)):
    response = requests.post(BASE + 'regsensor/' + str(i), data[i])
    print(response.json())

input()


# data to add a few test metrics
data = [{'s_id': 0, 'temp': 19, 'humidity': 12.2, 'wind_speed': 56.4, 'daynumber': 1}, 
        {'s_id': 1,'temp': 13, 'wind_speed': 56.4, 'daynumber': 1},
        {'s_id': 2, 'humidity': 12.2, 'wind_speed': 56.4, 'daynumber': 2},
        {'s_id': 0, 'temp': 10, 'humidity': 2.2, 'wind_speed': 7, 'daynumber': 2},
        {'s_id': 1, 'temp': 2, 'humidity': 19, 'daynumber': 2},
        {'s_id': 2, 'temp': 19, 'humidity': 12.2, 'wind_speed': 12.4, 'daynumber': 3},
        {'s_id': 0, 'temp': 19, 'humidity': 12.2, 'daynumber': 3},
        {'s_id': 0, 'wind_speed': 2, 'daynumber': 3}]

for i in range(len(data)):
    response = requests.post(BASE + "addmetric/" + str(i), data[i])
    print(response.json())
    

input()


#some test queries
data = {'sensors':'0,2,1', 'metrics':'humidity,wind_speed', 'startdate':2, 'enddate':3}
data2 = {'sensors':'0,2', 'metrics':'wind_speed', 'startdate':1, 'enddate':3}



response = requests.get(BASE + "query/", data)
print(response.json())

response = requests.get(BASE + "query/", data2)
print(response.json())
