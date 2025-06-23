import subprocess

def get_pi_temp():
	temp_str = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
	return temp_str.strip()[5:-2]

if __name__ == "__main__":
	print (get_pi_temp())
