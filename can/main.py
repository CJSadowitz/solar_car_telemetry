import can_receiver
import write_db

def main():
	try:
		# Test if it crashes out here if can network is not on
		bus = can_receiver.get_data_bus()
		while True:
			message = can_receiver.get_can_line(bus)
			if message == None:
				break
			data = write_db.clean_message(message)
			write_db.save_data(data)
	except Exception as e:
		print ("MAIN::unknown exception:", e)

if __name__ == "__main__":
	main()
