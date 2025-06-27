import serial

def get_serial(port):
	ser = serial.Serial(port, baudrate=9600, timeout=3)
	return ser

def get_line(ser):
	line = None
	try:
		data = ser.readline()
		if data == b'':
			return "0"

		return data.decode("utf-8").strip()

	except KeyboardInterrupt:
		return "end"

	except Exception as e:
		# print ("SPEED::serial_helper::get_line::exception:", e)
		return "-1"
