import can
import cantools
import subprocess
import time

def check_line(id, data, pins):
	if id != "3fa":
		return
	bool = check_data(id, data)
	if not bool:
		pin_off(pins)
		return
	trip_relay(pins)

def check_data(id, can_data):
	try:
		dbc = cantools.database.load_file("../can_db.dbc")
		can_id = int(id, 16)
		message = can.Message(arbitration_id=can_id, data=[int(can_data[i:i+2], 16) for i in range(0, len(can_data), 2)])
		translated_data = dbc.decode_message(message.arbitration_id, message.data)
		if (abs(translated_data["Pack_Current"]) >= 55):
			return True
		return False
	except Exception as e:
		print ("CAN::over_current_protection::check_data::exception:", e)

def trip_relay(pins):
	try:
		for pin in pins:
			subprocess.run(["pinctrl", "set", str(pin), "op", "dh"])
	except Exception as e:
		print ("CAN::over_current_protection::trip_relay::exception:", e)

def pin_off(pins):
	try:
		for pin in pins:
			subprocess.run(["pinctrl", "set", str(pin), "op", "dl"])
	except Exception as e:
		print ("CAN::over_current_protection::pin_off::exception:", e)
