# importing the requests library 
import requests 
import json
from datetime import date
import datetime

http_headers = {'Content-Type': 'application/json','accept': 'application/json'}
host_file = 'hosts.json'

with open(host_file) as jsonFile:
    hosts = json.load(jsonFile)
    jsonFile.close()

#Create Status Report
URL = 'http://127.0.0.1:5000/Bioaccess/01_status'
print('Creating Status Report from: ' + str(json.dumps(hosts)))
r = requests.request(method = 'post',url = URL,headers  = http_headers,data = json.dumps(hosts))
print('Result: ',r.text)

#Create ImageLog Report
URL = 'http://127.0.0.1:5000/Bioaccess/04_analize_images_log'
initial_date = str(date.today() - datetime.timedelta(days=1))
end_date     = str(date.today() - datetime.timedelta(days=1))
print('Creating ImageLog Report from: ' + initial_date + ' to ' + end_date)
data = {"hosts": hosts['hosts'],"initial_date": initial_date,"end_date": end_date}
r = requests.request(method = 'post',url = URL,headers  = http_headers,data = json.dumps(data))
print('Result: ',r.text)


#Check Freeze
URL = 'http://127.0.0.1:5000/Bioaccess/03_check_freeze'
print('Checking Freeze State from: '  +  str(json.dumps(hosts)))
data = {"hosts": hosts['hosts']}
r = requests.request(method = 'post',url = URL,headers  = http_headers,data = json.dumps(data))
print('Result: ',r.text)


#Clear Logs
URL = 'http://127.0.0.1:5000/Bioaccess/12_clear_logs'
initial_date = str(date.today() - datetime.timedelta(days=16))
end_date     = str(date.today() - datetime.timedelta(days=15))
print('Clearing logs: '  +  str(json.dumps(hosts)))
data = {"hosts": hosts['hosts']}
data = {"hosts": hosts['hosts'],"initial_date": initial_date,"end_date": end_date}
r = requests.request(method = 'post',url = URL,headers  = http_headers,data = json.dumps(data))
print('Result: ',r.text)

#Screenshot
URL = 'http://127.0.0.1:5000/Bioaccess/02_get_screenshot'
print('Get Screenshot collage: '  +  str(json.dumps(hosts)))
data = {"hosts": hosts['hosts']}
r = requests.request(method = 'post',url = URL,headers  = http_headers,data = json.dumps(data))
print('Result: ',r.text)

#Get Logs
#URL = 'http://127.0.0.1:5000/Bioaccess/08_get_logs'
#initial_date = str(date.today() - datetime.timedelta(days=1))
#end_date     = str(date.today() - datetime.timedelta(days=1))
#print('Creating ImageLog Report from: ' + initial_date + ' to ' + end_date)
#data = {"hosts": hosts['hosts'],"initial_date": initial_date,"end_date": end_date,"_ImagesLog": "True","_Logs": "True","_Termografias": "True"}
#r = requests.request(method = 'post',url = URL,headers  = http_headers,data = json.dumps(data))
#print('Result: ',r.text)
