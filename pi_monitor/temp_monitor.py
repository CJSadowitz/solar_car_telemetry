import subprocess

def get_pi_temp():
	try:
		temp_str = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
		return temp_str.strip()[5:-2]

	except Exception as e:
		print ("PI_MONITOR::temp_monitor::get_pi_temp::exception:", e)
		return -1
