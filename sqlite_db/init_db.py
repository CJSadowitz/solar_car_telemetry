import sqlite3

def init_database():
	mppt1_tables = ["mppt1_input", "mppt1_output", "mppt1_temp", "mppt1_aux_power", "mppt1_limits", "mppt1_status", "mppt1_power_connector", "mppt1_mode", "mppt1_max_output_voltage", "mppt1_max_input_current"]
	mppt1_ids = ["600", "601", "602", "603", "604", "605", "606", "608", "60a", "60b"]

	mppt2_tables = ["mppt2_input", "mppt2_output", "mppt2_temp", "mppt2_aux_power", "mppt2_limits", "mppt2_status", "mppt2_power_connector", "mppt2_mode", "mppt2_max_output_voltage", "mppt2_max_input_current"]
	mppt2_ids = ["610", "611", "612", "613", "614", "615", "616", "618", "61a", "61b"]

	cmu_tables = ["cmu_301", "cmu_302", "cmu_303", "cmu_304", "cmu_305", "cmu_306", "cmu_307", "cmu_308", "cmu_309", "cmu_30A", "cmu_30B", "cmu_30C"]
	cmu_ids = ["301", "302", "303", "304", "305", "306", "307", "308", "309", "30a", "30b", "30c"]

	bmu_tables = ["bmu_heartbeat_sensor", "pack_state_of_charge", "pack_balance_state_of_charge", "charger_control_info", "precharge_status", "min_max_cell_voltage", "min_max_cell_temp", "battery_pack_info", "battery_pack_status", "battery_pack_fan_status", "battery_pack_extended_info"]
	bmu_ids = ["300", "3f4", "3f5", "3f6", "3f7", "3f8", "3f9", "3fa", "3fb", "3fc", "3fd"]

	tables = mppt1_tables + mppt2_tables + cmu_tables + bmu_tables
	ids = mppt1_ids + mppt2_ids + cmu_ids + bmu_ids

	init_tables(tables, ids)
	init_data(ids, tables)

def init_tables(tables, can_ids):
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	# Master table for all devices on the can network
	cursor.execute(f"""
	CREATE TABLE IF NOT EXISTS can_devices (
		can_id TEXT PRIMARY KEY,
		table_name TEXT
	);
	""")

	for i in range(len(tables)):
		cursor.execute(f"""
		CREATE TABLE IF NOT EXISTS {tables[i]} (
			timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
			can_id TEXT NOT NULL CHECK (can_id = '{can_ids[i]}'),
			raw TEXT NOT NULL,
			FOREIGN KEY (can_id) REFERENCES can_devices(can_id)
		);
		""")

	cursor.execute(f"""
	CREATE TABLE IF NOT EXISTS gps (
		timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
		latitude TEXT NOT NULL,
		longitude TEXT NOT NULL,
		altitude TEXT NOT NULL
		);
	""")

	conn.commit()
	conn.close()

def init_data(ids, names):
	# Insert all data in the master table base
	conn = sqlite3.connect("../database.db")
	cursor = conn.cursor()

	cursor.executemany("INSERT OR IGNORE INTO can_devices (can_id, table_name) VALUES (?, ?);", list(zip(ids, names)))
	conn.commit()
	conn.close()
