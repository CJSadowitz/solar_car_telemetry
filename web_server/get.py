import can_translator
import asyncio
import psycopg

async def get_data():
	all_data = {}
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()
		all_data["a:_pi_monitor"] = await get_pi_monitor(cursor)
		# all_data["aa:_speed"]     = await get_speed(cursor)

		cmu1 = ["301", "302", "303"]
		cmu2 = ["304", "305", "306"]
		cmu3 = ["307", "308", "309"]
		cmu4 = ["30a", "30b", "30c"]

		all_data["z:_cmu_1"] = await get_cmu_data(cursor, cmu1)
		all_data["z:_cmu_2"] = await get_cmu_data(cursor, cmu2)
		all_data["z:_cmu_3"] = await get_cmu_data(cursor, cmu3)
		all_data["z:_cmu_4"] = await get_cmu_data(cursor, cmu4)

		mppt_name = ["mppt1_input", "mppt1_output", "mppt1_temp", "mppt2_input", "mppt2_output", "mppt2_temp"]
		mppt_id   = ["600", "601", "602", "610", "611", "612"]
		for i in range(len(mppt_id)):
			all_data[mppt_name[i]] = await get_can_table_data(cursor, mppt_id[i])

		battery_name = ["battery_pack_info", "pack_balance_state_of_charge", "min_max_cell_temp", "min_max_cell_voltage", "pack_state_of_charge"]
		battery_id = ["3fa", "3f5", "3f9", "3f8", "3f4"]
		for i in range(len(battery_id)):
			all_data[battery_name[i]] = await get_can_table_data(cursor, battery_id[i])

	except Exception as e:
		print ("WEB_SERVER::get::get_data::exception:", e)

	finally:
		await conn.close()
		return all_data

async def get_speed(cursor):
	await cursor.execute("SELECT * FROM vehicle_speed ORDER BY timestamp DESC LIMIT 1")
	db_data = await cursor.fetchone()
	clean_list = []
	item_dict = {}
	clean_list.append(db_data[0].strftime("%Y-%m-%d %H:%M:%S"))
	item_dict["speed_mph"] = float(db_data[1])
	clean_list.append(item_dict)
	return_list = []
	return_list.append(clean_list)
	return return_list

async def get_pi_monitor(cursor):
	await cursor.execute("SELECT * FROM pi_monitor ORDER BY timestamp DESC LIMIT 1")
	db_data = await cursor.fetchone()
	clean_list = []
	item_dict = {}
	clean_list.append(db_data[0].strftime("%Y-%m-%d %H:%M:%S"))
	item_dict["received"]    = float(db_data[1])
	item_dict["transmitted"] = float(db_data[2])
	item_dict["total"]       = float(db_data[3])
	item_dict["pi_temp"]     = float(db_data[4])
	clean_list.append(item_dict)
	return_list = []
	return_list.append(clean_list)
	return return_list

async def get_cmu_data(cursor, cmus):
	data = []
	can_data = {}
	for cmu in cmus:
		list_data = []
		await cursor.execute("SELECT timestamp, raw_data FROM can WHERE can_id=%s ORDER BY timestamp DESC LIMIT 1", (cmu,))
		db_data = await cursor.fetchone()
		list_data.append(db_data[0].strftime("%Y-%m-%d %H:%M:%S"))
		dict_data = can_translator.convert_data(cmu, db_data[1])
		for key in dict_data:
			if "Voltage" in key:
				if dict_data[key] > 7.5:
					can_data[key] = -999
					continue
			can_data[key] = dict_data[key]

	list_data.append(can_data)
	data.append(list_data)
	return data

async def get_can_table_data(cursor, id):
	await cursor.execute("SELECT timestamp, raw_data FROM can WHERE can_id=%s ORDER BY timestamp DESC LIMIT 1", (id,))
	data = await cursor.fetchone()
	cleaned_data = []
	list_data = []
	list_data.append(data[0].strftime("%Y-%m-%d %H:%M:%S"))
	can_dict = can_translator.convert_data(id, data[1])
	if (id == "3fa"):
		can_dict["Pack_Power"] = float(can_dict["Pack_Current"]) * float(can_dict["Pack_Voltage"])
	list_data.append(can_dict)
	cleaned_data.append(list_data)

	return cleaned_data

# FIX THIS NEXT :D
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

if __name__ == "__main__":
	print (asyncio.run(get_data()))
