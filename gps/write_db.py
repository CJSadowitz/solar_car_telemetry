import asyncio
import psycopg

async def save_message(lat, lon, alt):
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()
		await cursor.execute("INSERT INTO gps (latitude, longitude, altitude) VALUES (%s, %s, %s)", (lat, lon, alt))
		await conn.commit()

	except Exception as e:
		print ("WRITE_DB::save_message::unknown exception:", e)
		await conn.rollback()
	finally:
		await conn.close()
