import tkinter as tk
from tkinter import ttk
import get
import can_translator
import asyncio

def update(root, battery, velocity, array):
	data = asyncio.run(get.get_gui())
	speed = data["vehicle_speed"][0]
	if speed != None:
		velocity[0].set(str(speed[:5]) + " MPH")

	battery[0].set("SoC:\n"       + get_soc(data["pack_state_of_charge"]) + " %")
	battery[1].set("Power:\n"     + get_power(data["battery_pack_info"])  + " W")
	array[2].set("MPPT1\n"        + get_current(data["mppt1_input"]) + " A")
	array[3].set("MPPT2\n"        + get_current(data["mppt2_input"]) + " A")
	array[1].set("Net Wattage:\n" + get_net_wattage(data) + " W")
	root.after(100, lambda: update(root, battery, velocity, array))

def get_soc(data_dict):
	return str(data_dict["Pack_SoC_Percentage"])[:5]

def get_power(data_dict):
	return str(float(data_dict["Pack_Current"]) * float(data_dict["Pack_Voltage"]))[:5]

def get_current(data_dict):
	return str(data_dict["MPPT_Input_Current"])[:5]

def get_net_wattage(data_dict):
	mppt1_input  = data_dict["mppt1_input"]
	mppt1_output = data_dict["mppt1_output"]
	mppt2_input  = data_dict["mppt2_input"]
	mppt2_output = data_dict["mppt2_output"]

	mppt1_input_wattage  = float(mppt1_input["MPPT_Input_Voltage"])   * float(mppt1_input["MPPT_Input_Current"])
	mppt1_output_wattage = float(mppt1_output["MPPT_Output_Voltage"]) * float(mppt1_output["MPPT_Output_Current"])
	mppt2_input_wattage  = float(mppt2_input["MPPT_Input_Voltage"])   * float(mppt2_input["MPPT_Input_Current"])
	mppt2_output_wattage = float(mppt2_output["MPPT_Output_Voltage"]) * float(mppt2_output["MPPT_Output_Current"])

	input_wattage  = mppt1_input_wattage  + mppt2_input_wattage
	output_wattage = mppt1_output_wattage + mppt2_output_wattage

	return str(input_wattage - output_wattage)[:5]
