import tkinter as tk
from tkinter import ttk
from setup import setup_variables, setup_window, setup_layout
import update

def main():
	root = tk.Tk()
	frames = setup_window(root)
	battery, velocity, array = setup_variables(root)
	setup_layout(root, battery, velocity, array, frames)

	ttk.Button(root, text="Quit", command=root.destroy).place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
	root.attributes("-fullscreen", True)
	update.update(root, battery, velocity, array)
	root.mainloop()

if __name__ == "__main__":
    main()
