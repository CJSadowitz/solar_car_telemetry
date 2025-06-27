import asyncio
import psycopg

async def save_data(data):
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()
		query = "INSERT INTO vehicle_speed (speed) VALUES (%s)"
		await cursor.execute(query, (data,))
		await conn.commit()

	except Exception as e:
		print ("SPEED::write_db::save_data:exception:", e)
		await cursor.rollback()

	finally:
		await conn.close()
