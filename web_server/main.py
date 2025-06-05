from flask import Flask, render_template
from flask_cors import CORS
import get

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/home')
def home():
	return render_template("index.html")

@app.route('/recent_data')
def recent_data():
	return render_template("recent_data.html")

@app.route('/get_recent', methods=['GET'])
def get_db():
	return {"message": get.get_recent_entries()}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8008)

