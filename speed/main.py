import serial
import serial_helper
import write_db
import speed_calculator
import math
import asyncio

def main():
	port = "/dev/ttyACM0"
	ser = None
	while ser == None:
		ser = serial_helper.get_serial(port)

	time_list = []
	while True:
		line = serial_helper.get_line(ser)
		if line != None:
			if line == "end":
				break

			if line == "0":
				mph = 0
				asyncio.run(write_db.save_data(mph))
				continue

			if line != "-1"and line != '':
				if float(line) < 100 and len(time_list) != 0:
					time_list.append(time_list[-1])
				time_list.append(float(line))
			else:
				time_list.append(0)

			# print (time_list)
			if len(time_list) > 96:
				rpm = speed_calculator.calculate_rpm(time_list)
				mph = speed_calculator.calculate_mph(rpm)
				time_list = []
				# print (f"MPH: {mph:.2f}, {hex(math.floor(mph))}")
				asyncio.run(write_db.save_data(mph))
			# print (line)

if __name__ == "__main__":
	main()
