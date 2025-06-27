import asyncio
import psycopg

def clean_message(message):
	message = format(message)
	chunks = message.split(' ')
	can_data = chunks[1].split('#')
	id = can_data[0]
	data = can_data[1]
	return [chunks[0], id, data]

def format(msg):
	timestamp = msg.timestamp
	id = str(hex(msg.arbitration_id))
	data = ''.join(f"{byte:02X}" for byte in msg.data)
	formatted_message = str(timestamp) + ' ' + id[2:] + '#' + str(data)
	return formatted_message

async def save_data(data_list):
	try:
		conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")

		id = data_list[1]
		raw = data_list[2]

		async with conn:
			cursor = conn.cursor()
			await cursor.execute("INSERT INTO can (can_id, raw_data) VALUES (%s, %s)", (id, raw))

	except Exception as e:
		print ("CAN::WRITE_DB::save_data::exception:", e)

	finally:
		await conn.close()
