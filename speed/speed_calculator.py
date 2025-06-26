import math

def calculate_rpm(time_list):
	# Time in microseconds
	total = sum(time_list)
	seconds_per_pulse = (total / 1000000) / len(time_list)
	seconds_per_rotation = seconds_per_pulse * 96
	minute_per_rotation = seconds_per_rotation / 60
	rpm = 1 / minute_per_rotation
	return rpm

def calculate_mph(rpm):
	rotations_per_hour = rpm * 60
	inches_per_hour = rotations_per_hour * 21.25 * math.pi
	miles_per_hour = inches_per_hour / 63360
	return miles_per_hour
