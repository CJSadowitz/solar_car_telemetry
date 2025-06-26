import sqlite3
import can_translater
from datetime import datetime

def get_data():
	all_data = {}
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	cmu1 = ["cmu_301", "cmu_302", "cmu_303"]
	cmu2 = ["cmu_304", "cmu_305", "cmu_306"]
	cmu3 = ["cmu_307", "cmu_308", "cmu_309"]
	cmu4 = ["cmu_30A", "cmu_30B", "cmu_30C"]

	all_data["z_cmu_1"] = get_cmu_data(cursor, cmu1)
	all_data["z_cmu_2"] = get_cmu_data(cursor, cmu2)
	all_data["z_cmu_3"] = get_cmu_data(cursor, cmu3)
	all_data["z_cmu_4"] = get_cmu_data(cursor, cmu4)

	all_data["a_pi_monitor"] = get_pi_monitor(cursor)


	battery = ["battery_pack_info", "pack_balance_state_of_charge", "min_max_cell_temp", "min_max_cell_voltage", "pack_state_of_charge"]
	mppt = ["mppt1_input", "mppt1_output", "mppt1_temp", "mppt2_input", "mppt2_output", "mppt2_temp"]
	tables = battery + mppt

	for table in tables:
		data = get_can_table_data(cursor, table)
		if table == "battery_pack_info" or table == "pack_state_of_charge":
			all_data["a_" + table] = data
			continue
		all_data[table] = data

	all_data["a_speed"] = get_speed(cursor)

	conn.close()

	return all_data

def get_speed(cursor):
	cursor.execute("SELECT * FROM vehicle_speed ORDER BY timestamp DESC LIMIT 1")
	db_data = cursor.fetchall()
	i = 0
	clean_list = []
	item_dict = {}
	actual_data = db_data[0]
	for item in actual_data:
		if i == 0:
			clean_list.append(item)
		elif i == 1:
			item_dict["speed_mph"] = float(item)
		i += 1
	clean_list.append(item_dict)
	return_list = []
	return_list.append(clean_list)
	return return_list

def get_pi_monitor(cursor):
	cursor.execute(f"SELECT * FROM pi_monitor ORDER BY timestamp DESC LIMIT 1")
	db_data = cursor.fetchall()
	i = 0
	clean_list = []
	item_dict = {}
	actual_data = db_data[0]
	for item in actual_data:
		if i == 0:
			clean_list.append(item)
		elif i == 1:
			item_dict["received"] = float(item)
		elif i == 2:
			item_dict["transmitted"] = float(item)
		elif i == 3:
			item_dict["total"] = float(item)
		elif i == 4:
			item_dict["pi_temp"] = float(item)
		i += 1
	clean_list.append(item_dict)
	return_list = []
	return_list.append(clean_list)
	return return_list

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
		can_dict = can_translater.convert_data(table_name, row[1])
		if (table_name == "battery_pack_info"):
			can_dict["Pack_Power"] = can_dict["Pack_Current"] * can_dict["Pack_Voltage"]
		list_data.append(can_dict)
		cleaned_data.append(list_data)

	return cleaned_data

def get_dash():
	try:
		conn = sqlite3.connect("../database.db")
		cursor = conn.cursor()

		data = {}
		data["pi_monitor"] = get_pi_dash(cursor, "pi_monitor")
		data["speed"]      = get_pi_dash(cursor, "vehicle_speed")

	except Exception as e:
		print ("WEB_SERVER::get::get_dash:exception:", e)

	finally:
		conn.close()
		return data

def get_pi_dash(cursor, table):
	cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 1")
	return cursor.fetchall()


def get_graph_data():
	tables = ["pack_state_of_charge", "battery_pack_info"]
	amount = 10
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()
	data = {}
	for table in tables:
		section = get_graph_data_db(cursor, table, amount)
		v_1, v_2, k_1, k_2 = sort_graph_sections(section)
		data[k_1] = v_1
		data[k_2] = v_2

	cursor.close()
	return data

def get_graph_data_db(cursor, table_name, amount):
	cursor.execute(f"SELECT timestamp, raw FROM {table_name} ORDER BY timestamp DESC LIMIT {amount}")
	data = list(cursor.fetchall())
	list_data = []
	for row in data:
		dt = datetime.utcfromtimestamp(row[0])
		list_data.append(dt.strftime("%Y-%m-%d %H: %M: %S.%f"))
		list_data.append(can_translater.convert_data(table_name, row[1]))

	return list_data

def sort_graph_sections(list_dicts):
	section_1 = []
	section_2 = []
	item_1 = None
	item_2 = None
	time_stamp = None
	j = 0
	# print (list_dicts)
	for item in list_dicts:
		if j % 2 == 0:
			time_stamp = item
			j += 1
			continue
		j += 1
		i = 0
		for key in item:
			if i == 0:
				section_1.append([time_stamp, item[key]])
				item_1 = key
			elif i == 1:
				section_2.append([time_stamp, item[key]])
				item_2 = key
			i += 1
	return section_1, section_2, item_1, item_2

def get_gui():
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()
	tables = ["vehicle_speed", "pack_state_of_charge", "battery_pack_info", "mppt1_input", "mppt1_output", "mppt2_input", "mppt2_output"]
	data = []
	for table in tables:
		data += get_pi_dash(cursor, table)

	conn.close()

	return data

if __name__ == "__main__":
	print (get_data())
