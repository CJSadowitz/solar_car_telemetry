import can

def get_data_bus():
	try:
		bus = can.interface.Bus(channel="can0", interface="socketcan")
		return bus
	except OSError as e:
		if e.errno != 19:
			print ("CAN::CAN_RECEIVER::get_data_bus::unknown error:", e.errno)
		print ("CAN::CAN_RECEIVER::get_data_bess::oserror", e)
	except Exception as e:
		print ("CAN::CAN_RECEIVER::get_data_bus::exception:", e)
	return None

def get_can_line(bus):
	try:
		return bus.recv(timeout=1.0)
	except Exception as e:
		print ("CAN::CAN_RECEIVER::get_can_line::excpetion:", e)
		return None

