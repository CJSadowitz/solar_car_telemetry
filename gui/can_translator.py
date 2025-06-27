import cantools
import can

def convert_data(can_id, can_data):
	try:
		dbc = cantools.database.load_file("../can_db.dbc")
		id = int(can_id, 16)
		message = can.Message(arbitration_id=id, data=[int(can_data[i:i+2], 16) for i in range(0, len(can_data), 2)])
		return dbc.decode_message(message.arbitration_id, message.data)
	except Exception as e:
		print ("GUI::can_translator::convert_data::exception:", e)
