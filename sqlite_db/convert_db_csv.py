import sqlite3
import can_translator
from datetime import datetime, timezone
from tqdm import tqdm

def main():
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	tables = get_tables(cursor)
	tables = tables[1:]
	data = []
	for table in tqdm(tables, desc="Getting data"):
		data.append(get_data(cursor, table))

	conn.close()

def get_tables(cursor):
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
	tables = cursor.fetchall()
	return [table[0] for table in tables]

def get_data(cursor, table_name):
	cursor.execute(f"SELECT * FROM {table_name} ORDER BY timestamp")
	db_data = cursor.fetchall()
	data = []
	for row in tqdm(db_data, desc=f"converting db data from {table_name}"):
		list_data = []
		dt = None
		if (table_name != "gps"):
			dt = datetime.fromtimestamp(row[0], tz=timezone.utc)
			list_data.append(dt.strftime("%Y-%m-%d %H: %M: %S.%f"))
			list_data.append(can_translator.convert_data(table_name, row[2]))
		else:
			list_data.append(row)
		data.append(list_data)

	return data

if __name__ == "__main__":
	main()
