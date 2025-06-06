import sqlite3

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
			recent_data[table_name] = list(str(data[0]))

	return recent_data

if __name__ == "__main__":
	get_recent_entries()
