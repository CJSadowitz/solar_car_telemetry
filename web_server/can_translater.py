import sqlite3
import cantools
import can

def convert_data(table_name, can_data):
    dbc = cantools.database.load_file("../web_server/can_db.dbc")
    id = int(get_id(table_name), 16)
    message = can.Message(arbitration_id=id, data=[int(can_data[i:i+2], 16) for i in range(0, len(can_data), 2)])
    return dbc.decode_message(message.arbitration_id, message.data)

def get_id(table_name):
    conn = sqlite3.connect("../database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT can_id FROM can_devices WHERE table_name=?",(table_name,))
    result = cursor.fetchall()
    conn.close()
    return result[0][0]

if __name__ == "__main__":
    print (convert_data("cmu_301", "521200000801D900"))

