import tkinter as tk
from tkinter import ttk

def setup_layout(root, battery, velocity, array, frames):
	# Battery Setup
	for item in battery:
		ttk.Label(frames[0], textvariable=item, font=("Arial", 20)).pack(expand=True)
	# Velocity
	for item in velocity:
		ttk.Label(frames[1], textvariable=item, font=("Arial", 36)).pack(expand=True)
	# Array
	for item in array:
		ttk.Label(frames[2], textvariable=item, font=("Arial", 20)).pack(expand=True)

def setup_variables(root):
	pack_soc      = tk.StringVar()
	battery_power = tk.StringVar()
	speed         = tk.StringVar()
	mppt1_in      = tk.StringVar()
	mppt1_out     = tk.StringVar()
	mppt2_in      = tk.StringVar()
	mppt2_out     = tk.StringVar()
	battery = [pack_soc, battery_power]
	velocity = [speed]
	array = [mppt1_in, mppt1_out, mppt2_in, mppt2_out]

	return battery, velocity, array

def setup_window(root):
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=2)
	root.columnconfigure(2, weight=1)
	root.rowconfigure(0, weight=1)

	battery_frame = ttk.Frame(root, padding=20, relief="ridge")
	battery_frame.grid(row=0, column=0, sticky="nsew")

	velocity_frame = ttk.Frame(root, padding=20, relief="ridge")
	velocity_frame.grid(row=0, column=1, sticky="nsew")

	array_frame = ttk.Frame(root, padding=20, relief="ridge")
	array_frame.grid(row=0, column=2, sticky="nsew")

	return battery_frame, velocity_frame, array_frame
