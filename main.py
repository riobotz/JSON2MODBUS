from flask import Flask
from flask import request
from handler import handle_read
from handler import handle_write
import json
app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def read_value():
	if request.method=='POST':
		data = request.get_data()
		out=handle_write(json.loads(data))
	else:
		pom = request.url
		ind = pom.find('?')
		data = pom[ind+1:len(pom)]
		out=handle_read(json.loads(data))
	return out



if __name__=="__main__":
	app.run()