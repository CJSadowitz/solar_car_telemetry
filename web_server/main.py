from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/home')
def home():
	return render_template("index.html")

@app.route('/get_recent', methods=['GET'])
def get_db():
	return {"message": "test_method"}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8008)

