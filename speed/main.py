import serial
import serial_helper
import write_db

def main():
	port = "/dev/ttyACM0"
	ser = None
	while ser == None:
		ser = serial_helper.get_serial(port)

	while True:
		line = serial_helper.get_line(ser)
		if line != None:
			print (line)
			# write_db.save_data(line)

if __name__ == "__main__":
	main()
