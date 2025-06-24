import subprocess
import json

def get_dash_local():
	url = "localhost:8008/get_gui"
	output = subprocess.run(["curl", url, "-s"], stdout=subprocess.PIPE, text=True)
	data = json.loads(output.stdout)
	return data
