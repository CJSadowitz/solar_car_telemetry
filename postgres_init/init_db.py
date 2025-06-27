import asyncio
import psycopg
import datetime

async def initialize_database():
	conn = await psycopg.AsyncConnection.connect("dbname=solar_telemetry user=solar")
	try:
		cursor = conn.cursor()
		await init_tables(cursor)
	except:
		await conn.rollback()
		raise
	finally:
		await conn.commit()
		await conn.close()

async def init_tables(cursor):
	await cursor.execute(f"""
	CREATE TABLE IF NOT EXISTS can (
		timestamp TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
		can_id TEXT NOT NULL,
		raw_data TEXT NOT NULL
	);
	""")

	await cursor.execute(f"""
	CREATE TABLE IF NOT EXISTS gps (
		timestamp TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
		latitude TEXT NOT NULL,
		longitude TEXT NOT NULL,
		altitude TEXT NOT NULL
		);
	""")

	await cursor.execute(f"""
	CREATE TABLE IF NOT EXISTS vehicle_speed (
		timestamp TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
		speed TEXT NOT NULL
		);
	""")

	await cursor.execute(f"""
	CREATE TABLE IF NOT EXISTS pi_monitor (
		timestamp TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
		received TEXT NOT NULL,
		transmitted TEXT NOT NULL,
		total TEXT NOT NULL,
		temperature TEXT NOT NULL
		);
	""")
