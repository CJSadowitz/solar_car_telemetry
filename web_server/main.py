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

@app.route("/get_dash_data", methods=["GET"])
def get_dash_data():
	return {"message": get.get_dash_data()}

@app.route("/get_recent", methods=["GET"])
def get_db():
	return {"message": get.get_recent_entries()}

@app.route("/get_all_gps", methods=["GET"])
def get_all_gps():
	return {"message": get.get_all_gps()}

@app.route("/get_recent_gps", methods=["GET"])
def get_recent_gps():
	return {"message": get.get_recent_gps()}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8008)

