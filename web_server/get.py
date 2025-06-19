import sqlite3
import can_translater
from datetime import datetime

def get_data():
	all_data = {}
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	amount_of_data = 1
	battery = ["battery_pack_info", "pack_balance_state_of_charge", "precharge_status"]
	cmus = ["cmu_301", "cmu_302", "cmu_303", "cmu_304", "cmu_305", "cmu_306", "cmu_307", "cmu_308", "cmu_309", "cmu_30A", "cmu_30B", "cmu_30C"]
	mppt = ["mppt1_input", "mppt1_output", "mppt1_status", "mppt2_input", "mppt2_output", "mppt2_status"]
	tables = battery + cmus + mppt

	for table in tables:
		data = get_can_table_data(cursor, table, amount_of_data)
		all_data[table] = data

	conn.close()

	return all_data

def get_can_table_data(cursor, table_name, amount):
	data = []
	cursor.execute(f"SELECT timestamp, raw FROM {table_name} ORDER BY timestamp DESC LIMIT {amount}")
	data = list(cursor.fetchall())
	cleaned_data = []
	for row in data:
		list_data = []
		dt = datetime.utcfromtimestamp(row[0])
		list_data.append(dt.strftime("%Y-%m-%d %H: %M: %S.%f"))
		list_data.append(can_translater.convert_data(table_name, row[1]))
		cleaned_data.append(list_data)

	return cleaned_data

if __name__ == "__main__":
	print (get_data())
