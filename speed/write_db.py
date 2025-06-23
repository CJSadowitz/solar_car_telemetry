import sqlite3

def save_data(line):
	data = clean_data(line)
	try:
		conn = sqlite3.connect("../database.db")
		cursor = conn.cursor()
		query = "INSERT INTO vehicle_speed (speed) VALUES (?)"
		cursor.execute(query, (data,))
	except Exception as e:
		print ("SPEED::write_db::save_data:exception:", e)

def clean_data(line):
	return line
