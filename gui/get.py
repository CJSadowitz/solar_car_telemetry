import asyncio
import psycopg
import can_translator

async def get_gui():
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor  = conn.cursor()

		table_names = ["pack_state_of_charge", "battery_pack_info", "mppt1_input", "mppt1_output", "mppt2_input", "mppt2_output"]
		can_ids = ["3f4", "3fa", "600", "601", "610", "611"]
		i = 0
		data = {}
		for can_id in can_ids:
			data[table_names[i]] = await get_readable_can_data(cursor, can_id)
			i += 1

		data["vehicle_speed"] = await get_speed(cursor)

	except Exception as e:
		print ("GUI::get::get_gui::exception:", e)

	finally:
		await conn.close()
		return data

async def get_readable_can_data(cursor, can_id):
	await cursor.execute("SELECT raw_data FROM can WHERE can_id = %s ORDER BY timestamp DESC LIMIT 1", (can_id,))
	raw_data = await cursor.fetchone()
	return can_translator.convert_data(can_id, raw_data[0])

async def get_speed(cursor):
	await cursor.execute("SELECT speed FROM vehicle_speed ORDER BY timestamp DESC LIMIT 1")
	return await cursor.fetchone()

if __name__ == "__main__":
	asyncio.run(get_gui())
