from flask import Flask
from flask_cors import CORS
import asyncio
import get_data_page
import get_graph_page

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/get_data", methods=["GET"])
def get_data():
	return { "body": asyncio.run(get_data_page.get_data()) }

@app.route("/get_graph_data", methods=["GET"])
def get_graph_data():
	return { "body": asyncio.run(get_graph_page.get_graph_data()) }

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8008)

