def get_interface_stats(interface):
	with open("/proc/net/dev", "r") as file:
		for line in file:
			if interface in line:
				data = line.split(":")[1].split()
				received_bytes    = int(data[0])
				transmitted_bytes = int(data[8])
				return received_bytes, transmitted_bytes
	return None, None


def get_delta_stats(old_tuple, new_tuple):
	received    = new_tuple[0] - old_tuple[0]
	transmitted = new_tuple[1] - old_tuple[1]
	return received, transmitted
