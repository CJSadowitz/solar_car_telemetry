import serial
import pynmea2
import write_db

def main():
	ser = None
	try:
		port = "/dev/ttyACM0"
		ser = serial.Serial(port, 9600, timeout=1)
	except Exception as e:
		print ("MAIN::SERIAL_PORT::unknown exception", e)
		return 1

	try:
		lat, lon, alt = None, None, None
		while True:
			line = ser.readline().decode("utf-8").strip()
			if line.startswith("$GNRMC"):
				msg = pynmea2.parse(line)
				lat = msg.latitude
				lon = msg.longitude

			if line.startswith("$GNGGA"):
				msg = pynmea2.parse(line)
				alt = msg.altitude

			if (lat != None and lon != None and alt != None):
				write_db.save_message(lat, lon, alt)
				lat, lon, alt = None, None, None

	except Exception as e:
		print ("MAIN::READ_LINE::unknown exception", e)
		ser.close()
		return 1

	finally:
		ser.close()
		return 0


if __name__ == "__main__":
	main()
