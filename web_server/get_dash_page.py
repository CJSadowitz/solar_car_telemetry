import asyncio
import psycopg

async def get_dash():
	data = {}
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()
		data["speed"] = await get_speed(cursor)
		data["laps"]  = await get_laps(cursor)

	except Exception as e:
		print ("WEB_SERVER::get_dash_page::get_dash::exception:", e)

	finally:
		await conn.close()
		print (data)
		return data

async def get_speed(cursor):
	await cursor.execute("SELECT speed FROM vehicle_speed ORDER BY timestamp DESC LIMIT 1")
	speed = await cursor.fetchone()
	return speed[0]

async def get_laps(cursor):
	track_distance = 3.15 # miles
	await cursor.execute("""
		WITH intervals AS (
			SELECT timestamp, speed, lag(timestamp) OVER (ORDER BY timestamp) AS prev_ts
			FROM vehicle_speed
		)
		SELECT SUM(CAST(speed AS float) * EXTRACT(EPOCH FROM(timestamp - prev_ts)) / 3600) AS total_distance
		FROM intervals WHERE prev_ts IS NOT NULL;
	""")
	distance = await cursor.fetchone()
	return distance[0] / track_distance

if __name__ == "__main__":
	print (asyncio.run(get_dash()))
