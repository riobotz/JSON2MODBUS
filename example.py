import requests
import serial
import json
import handler

ret=requests.post("http://127.0.0.1:5000/",data='{"addr":"7","baud":"9600","st":"201","val":"10"}')
#ret=requests.get("http://127.0.0.1:5000/",data='{"addr":"7","baud":"9600","st":"18","reg":"1"}')


print ret
