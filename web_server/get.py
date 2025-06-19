import sqlite3
import can_translater
from datetime import datetime

def get_data():
	all_data = {}
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	battery = ["battery_pack_info", "pack_balance_state_of_charge", "min_max_cell_temp", "min_max_cell_voltage"]
	cmu1 = ["cmu_301", "cmu_302", "cmu_303"]
	cmu2 = ["cmu_304", "cmu_305", "cmu_306"]
	cmu3 = ["cmu_307", "cmu_307", "cmu_309"]
	cmu4 = ["cmu_30A", "cmu_30B", "cmu_30C"]
	mppt = ["mppt1_input", "mppt1_output", "mppt1_temp", "mppt2_input", "mppt2_output", "mppt2_temp"]
	tables = battery + mppt

	for table in tables:
		data = get_can_table_data(cursor, table)
		all_data[table] = data

	all_data["cmu_1"] = get_cmu_data(cursor, cmu1)
	all_data["cmu_2"] = get_cmu_data(cursor, cmu2)
	all_data["cmu_3"] = get_cmu_data(cursor, cmu3)
	all_data["cmu_4"] = get_cmu_data(cursor, cmu4)

	conn.close()

	return all_data

def get_cmu_data(cursor, cmus):
	data = []
	can_data = {}
	for cmu in cmus:
		list_data = []
		cursor.execute(f"SELECT timestamp, raw FROM {cmu} ORDER BY timestamp DESC LIMIT 1")
		db_data = list(cursor.fetchall())
		for row in db_data:
			dt = datetime.utcfromtimestamp(row[0])
			list_data.append(dt.strftime("%Y-%m-%d %H: %M: %S.%f"))
			dict_data = can_translater.convert_data(cmu, row[1])
			for key in dict_data:
				if "Voltage" in key:
					if dict_data[key] > 7.5:
						can_data[key] = -999
						continue
				can_data[key] = dict_data[key]

	list_data.append(can_data)
	data.append(list_data)
	return data

def get_can_table_data(cursor, table_name):
	data = []
	cursor.execute(f"SELECT timestamp, raw FROM {table_name} ORDER BY timestamp DESC LIMIT 1")
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
	get_data()
