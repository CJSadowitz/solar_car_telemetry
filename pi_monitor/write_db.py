import sqlite3

def save_data(delta):
	try:
		conn = sqlite3.connect("../database")
		cursor = conn.cursor()

		query = "INSERT INTO pi_monitor (received, transmitted) VALUES (?, ?)"
		cursor.execute(query, (delta[0], delta[1]))

	except Exception as e:
		print ("PI_MONITOR::write_db::save_data::exception:", e)

	finally:
		conn.close()
