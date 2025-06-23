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
		write_db.save_data(delta, temperature)
		old = new

if __name__ == "__main__":
	main()
