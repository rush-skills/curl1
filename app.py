import os
import uuid
import random
import json

from flask import *
app = Flask(__name__)

data = {}

# Return (new?, session_id)
def get_session(request):
	session = request.headers.get('SESSION')
	if session and session in data:
		return (False, session)
	else:
		uid = uuid.uuid4().hex
		data[uid] = {"admin": False, "completed": False, "obj": {}}
		return (True, uid)

def generate_object(session_id):
	obj = {}
	obj["user_id"] = random.randint(1,10000)
	obj["id"] = uuid.uuid4().hex
	obj["data"] = "GLHF!"
	data[session_id]["obj"] = obj
	return obj

@app.route('/', methods=['GET', 'POST'])
def start():
	t = request.method
	resp = {"data": "Something is wrong"}
	if t == "GET":
		new, session_id = get_session(request)
		if new:
			resp["data"] = session_id
		else:
			resp = generate_object(session_id)
	elif t == "POST":
		new, session_id = get_session(request)
		if not new and data[session_id]["completed"]:
			resp["data"] = os.environ["FLAG1"]
	return jsonify(resp)

@app.route("/<uid>", methods=['GET', 'PUT', 'DELETE'])
def obj(uid=None):
	t = request.method
	new, session_id = get_session(request)
	user_data = data[session_id]
	obj = user_data["obj"]
	resp = "Something is wrong"
	if new or obj == {}:
		return session_id
	elif uid != obj["id"]:
		return resp
	else:
		if t == "GET":
			return jsonify(obj)
		elif t == "PUT":
			user_id = request.form.get("user_id")
			if user_id=="0":
				user_data["admin"] = True
			resp = "Success"
		elif t == "DELETE":
			if user_data["admin"]:
				user_data["completed"] = True
			user_data["obj"] = {}
			resp = "Success"
	return resp
			

port = int(os.environ['PORT'])

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=port, debug=True)