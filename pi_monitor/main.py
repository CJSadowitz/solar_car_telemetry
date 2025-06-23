import lte_monitor
import temp_monitor
import write_db

def main():
	interface = "wwan0"
	old = lte_monitor.get_interface_stats(interface)

	while True:
		new = lte_monitor.get_interface_stats(interface)
		delta = lte_monitor.get_delta_stats(old, new)
		write_db.save_data(delta)
		old = new

if __name__ == "__main__":
	main()
