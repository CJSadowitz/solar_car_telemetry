import sqlite3

def save_message(lat, lon, alt):
	conn = None
	try:
		conn = sqlite3.connect("../database.db")
		cursor = conn.cursor()
		query = f"INSERT INTO gps (latitude, longitude, altitude) VALUES (?, ?, ?)"
		cursor.execute(query, (lat, lon, alt))
		conn.commit()

	except Exception as e:
		print ("WRITE_DB::save_message::unknown exception:", e)

	finally:
		conn.close()
