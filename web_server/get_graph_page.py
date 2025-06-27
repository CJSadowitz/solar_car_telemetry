import can_translator
import asyncio
import psycopg

async def get_graph_data():
	ids = ["3f4", "3fa"]
	amount = 10
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()
		data = {}
		for i in range(len(ids)):
			section = await get_graph_data_db(cursor, ids[i], amount)
			v_1, v_2, k_1, k_2 = sort_graph_sections(section)
			data[k_1] = v_1
			data[k_2] = v_2

	except Exception as e:
		print ("WEB_SERVER::get_graph_page::get_graph_data::exception:", e)

	finally:
		await cursor.close()
		return data

async def get_graph_data_db(cursor, id, amount):
	await cursor.execute("SELECT timestamp, raw_data FROM can WHERE can_id=%s ORDER BY timestamp DESC LIMIT %s", (id, amount))
	data = await cursor.fetchall()
	list_data = []
	for row in data:
		list_data.append(row[0].strftime("%Y-%m-%d %H: %M: %S.%f"))
		list_data.append(can_translator.convert_data(id, row[1]))

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
	print (asyncio.run(get_graph_data()))
