import lte_monitor
import temp_monitor
import write_db
import time
import asyncio


def main():
	interface = "wwan0"
	old = lte_monitor.get_interface_stats(interface)
	if (old == (None, None)):
		print ("PI_MONITOR::main::main::interface_is_none")
		return 1
	while True:
		time.sleep(1)
		new = lte_monitor.get_interface_stats(interface)
		delta = lte_monitor.get_delta_stats(old, new)
		temperature = temp_monitor.get_pi_temp()
		total = new[0] + new[1]
		asyncio.run(write_db.save_data(delta, total, temperature))
		old = new

if __name__ == "__main__":
	main()
