import asyncio
import psycopg

async def save_data(delta, total, temp):
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()

		query = "INSERT INTO pi_monitor (received, transmitted, total, temperature) VALUES (%s, %s, %s, %s)"
		await cursor.execute(query, (delta[0], delta[1], total, temp))
		await conn.commit()

	except Exception as e:
		print ("PI_MONITOR::write_db::save_data::exception:", e)
		await conn.rollback()

	finally:
		await conn.close()
