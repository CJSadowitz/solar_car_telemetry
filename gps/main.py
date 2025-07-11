import serial
import pynmea2
import write_db
import asyncio

def main():
	ser = get_serial_port("/dev/gps")
	if (ser == None):
		return 1

	output = 0
	while output != 1:
		output = loop_gps_lines(ser)

	ser.close()

def get_serial_port(port):
	try:
		ser = serial.Serial(port, 9600, timeout=1)
		return ser
	except Exception as e:
		print ("GPS::MAIN::get_serial_port::exception:", e)
		return None

def loop_gps_lines(ser):
	try:
		lat, lon, alt = None, None, None
		data = ser.readline()
		if data == b'':
			return 0

		line = data.decode("utf-8").strip()
		msg = pynmea2.parse(line)
		if line.startswith("$GNRMC"):
			lat, lon = msg.latitude, msg.longitude
		elif line.startswith("$GNGGA"):
			alt = msg.altitude
		if (lat != None and lon != None and alt != None):
			asyncio.run(init_db.initialize_database())(write_db.save_message(lat, lon, alt))
			lat, lon, alt = None, None, None
			return 0

	except pynmea2.ChecksumError:
		print ("GPS::MAIN::loop_gps_lines::checksumerror:", e)
		return 0

	except Exception as e:
		print ("GPS::MAIN::loop_gps_lines::exception:", e)
		return 1


if __name__ == "__main__":
	main()
