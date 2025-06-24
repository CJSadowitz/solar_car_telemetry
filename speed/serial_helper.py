import serial

def get_serial(port):
	ser = serial.Serial(port, baudrate=115200, timeout=1)
	if ser == None:
		print ("SPEED::serial_helper::get_serial:serial port not found")
	return ser

def get_line(ser):
	line = None
	if ser.in_waiting:
		line = ser.readline().decode("utf-8").strip()
	return line
