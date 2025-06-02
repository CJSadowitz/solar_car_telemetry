def get_data_bus():
	try:
		bus = can.interface.Bus(channel="can0", bustype="socketcan")
		return bus
	except OSError as e:
		if e.errno != 19:
			print ("CAN_RECEIVER::get_data_bus::unknown error:", e.errno)
		print ("CAN_RECEIVER::get_data_bus::can network not found")
	except Exception as e:
		print ("CAN_RECEIVER::get_data_bus::unknown exception:", e)
	return None

def get_can_line(bus):
	try:
		return bus.recv(timeout=1.0)
	except Exception as e:
		print ("CAN_RECEIVER::get_can_line::unknown excpetion:", e)
		return None

