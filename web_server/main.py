from flask import Flask, render_template
from flask_cors import CORS
import get

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/recent_data")
def recent_data():
	return render_template("recent_data.html")

@app.route("/get_data", methods=["GET"])
def get_data():
	return { "body": get.get_data() }

@app.route("/get_graph_data", methods=["GET"])
def get_graph_Data():
	return { "body": get.get_graph_data() }

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8008)

