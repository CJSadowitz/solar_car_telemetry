import sqlite3

def save_data(delta, temp):
	try:
		conn = sqlite3.connect("../database.db")
		cursor = conn.cursor()

		query = "INSERT INTO pi_monitor (received, transmitted, temperature) VALUES (?, ?, ?)"
		cursor.execute(query, (delta[0], delta[1], temp))
		conn.commit()

	except Exception as e:
		print ("PI_MONITOR::write_db::save_data::exception:", e)

	finally:
		conn.close()
