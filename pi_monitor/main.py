import lte_monitor
import temp_monitor
import write_db
import time

def main():
	interface = "wwan0"
	old = lte_monitor.get_interface_stats(interface)
	while True:
		time.sleep(1)
		new = lte_monitor.get_interface_stats(interface)
		delta = lte_monitor.get_delta_stats(old, new)
		temperature = temp_monitor.get_pi_temp()
		total = new[0] + new[1]
		write_db.save_data(delta, total, temperature)
		old = new

if __name__ == "__main__":
	main()
