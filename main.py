from flask import Flask
from flask import request
from handler import handle_read
from handler import handle_write
import json
app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def read_value():
	print "x"
	out=""
	if request.method=='POST':
		print "post"
		data = request.get_data()
		print data
		out=handle_write(json.loads(data))
	else:
		print "get"
		#pom = request.url
		data = request.data
		#print pom
		#ind = pom.find('?')
		#print ind
		#data = pom[ind+1:len(pom)]
		print data
		out=handle_read(json.loads(data))
		print out
	return out



if __name__=="__main__":
	app.run(debug=False, host='0.0.0.0')