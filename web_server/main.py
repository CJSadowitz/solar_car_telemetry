from flask import Flask
from flask_cors import CORS
import get

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/get_data", methods=["GET"])
def get_data():
	return { "body": get.get_data() }

@app.route("/get_graph_data", methods=["GET"])
def get_graph_data():
	return { "body": get.get_graph_data() }

@app.route("/get_dash", methods=["GET"])
def get_dash():
	return {"body": get.get_dash() }

@app.route("/get_gui", methods=["GET"])
def get_gui():
	return { "body": get.get_gui() }

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8008)

