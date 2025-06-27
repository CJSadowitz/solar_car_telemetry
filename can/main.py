import can_receiver
import write_db
from over_current_protection import check_line, pin_off
import asyncio

def main():
	pins = [18, 15, 14, 23]
	pin_off(pins)
	try:
		bus = can_receiver.get_data_bus()
		while True:
			message = can_receiver.get_can_line(bus)
			if message == None:
				break
			data = write_db.clean_message(message)
			check_line(data[1], data[2], pins)
			asyncio.run(write_db.save_data(data))

	except Exception as e:
		print ("CAN::MAIN::exception:", e)

if __name__ == "__main__":
	main()
