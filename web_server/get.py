import sqlite3
import can_translater

def get_recent_entries():
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	cursor.execute("SELECT table_name FROM can_devices")
	tables = cursor.fetchall()

	recent_data = {}
	for (table_name, ) in tables:
		cursor.execute(f"SELECT raw FROM {table_name} ORDER BY timestamp DESC LIMIT 1")
		data = cursor.fetchone()
		if data != None:
			converted_data = can_translater.convert_data(table_name, data[0])
			recent_data[table_name] = converted_data

	conn.close()

	return recent_data

def get_dash_data():
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	cursor.execute(f"SELECT raw FROM pack_state_of_charge ORDER BY timestamp DESC LIMIT 1")
	battery_percent = cursor.fetchone()

	dash_data = {}
	dash_data["pack_state_of_charge"] = battery_percent
	# Include speed from database
	# Include time left from somewhere

	conn.close()

	return dash_data

if __name__ == "__main__":
	get_recent_entries()
