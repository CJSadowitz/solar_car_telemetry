import tkinter as tk
from tkinter import ttk
import get
import can_translator

def update(root, battery, velocity, array):
	data = get.get_dash_local()
	speed = (data["body"][0])
	velocity[0].set(str(speed[1][:5]) + " MPH")
	i = 0
	net_wattage = 0
	for tuple in data["body"][1:]:
		output = clean_data(tuple)
		if i == 0:
			battery[i].set("SoC:\n" + get_soc(output)[:5] + " %")
		elif i == 1:
			wattage = get_wattage(output)
			battery[i].set("Power:\n" + str(wattage) + " W")
		else:
			# MPPT 1 input
			if i == 2:
				array[2].set("MPPT1\n" + get_current(output) + " A")
			if i == 4:
				array[3].set("MPPT2\n" + get_current(output) + " A")
			net_wattage += get_wattage(output)
		i += 1

	array[1].set("Net Wattage:\n" + str(net_wattage) + " W")
	root.after(100, lambda: update(root, battery, velocity, array))

def get_soc(can_dict):
	i = 0
	for key in can_dict:
		if i == 1:
			return str(can_dict[key])
		i += 1

def get_current(can_dict):
	i = 0
	current = ""
	for key in can_dict:
		if i == 1:
			current += str(can_dict[key])
		i += 1
	return current
def get_wattage(can_dict):
	voltage = 0
	current = 0
	i = 0
	for key in can_dict:
		if i == 0:
			voltage = float(can_dict[key])
			continue
		if i == 1:
			current == float(can_dict[key])
			continue
		i += 1
	wattage = voltage * current
	return wattage

def clean_data(tuple):
	id = tuple[1]
	raw_data = tuple[2]
	output = can_translator.convert_data_id(id, raw_data)
	return output
