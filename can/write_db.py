import sqlite3

def clean_message(message):
	chunks = message.split(' ')
	can_data = chunks[2].split('#')
	id = can_data[0]
	data = can_data[1]
	return [chunks[0], id, data]

def save_data(data_list):
	try:
		conn = sqlite3.connect("../database.db")
		cursor = conn.cursor()

		timestamp = data_list[0]
		can_id = data_list[1]
		raw = data_list[2]

		cursor.execute("SELECT table_name FROM can_tables WHERE can_id = ?", (can_id,))
		result = cursor.fetchone()

		if result:
			table_name = result[0]
			query = f"INSERT INTO {table_name} (timestamp, can_id, raw) VALUES (?, ?, ?)"
			cursor.execute(query, (timestamp, can_id, raw))
			conn.commit()
		else:
			print (f"WRITE_DB::save_data::{can_id} not found in can_tables")

	except sqlite3.Error as e:
		print ("WRITE_DB::save_data::sqlite3 error:", e)
	except Exception as e:
		print ("WRITE_DB::save_data::unknown exception:", e)

	finally:
		conn.close()
