
import tkinter as tk
from tkinter import ttk
import serial
# import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np
from matplotlib.figure import Figure
import csv

import customtkinter as ctk
import ctypes

# Variables
is_plotting = False
max_data_points = 50
data_counter = 0  # Counter for unique data files
csv_data = []  # List to hold the data
temperature= np.array([])
vibration = np.array([])
force=np.array([])
# pulses = np.array([])

# Lock for synchronizing access to shared data
data_lock = threading.Lock()
# Function to start reading data from Arduino

dark_mode = False
try:
    value = ctypes.windll.uxtheme.IsThemeActive()
    if value == 1:
        dark_mode = True
    else:
        dark_mode = False
except Exception as e:
    print (f'A Theme Error has occurred: {e}')
    dark_mode =  False

def toggle_dark_mode():
    global dark_mode
    dark_mode=not dark_mode
    update_Theme()

def update_Theme():
    theme = "dark" if dark_mode else "light"
    root.configure(background='black' if dark_mode else 'light')
    ctk.set_appearance_mode(theme)
    print(f"SWitching to {theme} Mode")
    switch_1.configure(text='Light Mode' if dark_mode else 'Dark Mode')

    # update the canvas themes
    # canvas1.get_tk_widget().configure(bg = 'black' if dark_mode else 'white')

def start_plotting():
    global is_plotting
    is_plotting = True
    thread = threading.Thread(target=update_plot)
    thread.daemon = True
    thread.start()
    ser.reset_input_buffer()

# Function to stop reading data from Arduino
def stop_plotting():
    global is_plotting
    is_plotting = False

# Function to update the first plot
def update_plot():
    global is_plotting, temperature,vibration,force,csv_data, data_counter
    while is_plotting:
        try:
            data = ser.readline().decode('utf-8').strip()
            comb_data= data.split(',')
            #if(len(comb_data)==3):
            temp = comb_data[0]
            vib = comb_data[1]
            foc=comb_data[2]
            with data_lock:
                if len(temperature) < 50:
                    temperature = np.append(temperature, float(temp[0:4]))
                    vibration = np.append(vibration, float(vib[0:4]))
                    # pulses = np.append(pulses, int(pwm[0:4]))
                    force=np.append(force,float(foc[0:4]))
                    
                else:
                    temperature[0:49] = temperature[1:50]
                    temperature[49] = float(temp[0:4])
                    vibration[0:49] = vibration[1:50]
                    vibration[49] = float(vib[0:4])
                    # pulses[0:49] = pulses[1:50]
                    # pulses[49] = int(pwm[0:4])
                    force[0:49] = force[1:50]
                    force[49] = float(foc[0:4])
            
            temp_label.configure(text=f'Temperature: {temp}')
            #pwm_label.config(text=f'PWM: {pwm}')
            vib_label.configure(text=f'Vibration: {vib}')
            force_label.configure(text=f'Force: {foc}')
                        # Append data to csv_data
            csv_data.append([temp,vib, foc])

            # Check if data exceeds 200 points and save to a new CSV file
            if len(csv_data) >= max_data_points:
                save_data_to_csv(data_counter)
                data_counter += 1
                csv_data = []
            root.after(1, updateplots)
        except Exception as e:
          print(e)
        #root.update()

# Function to save data to a CSV file with a unique identifier
def save_data_to_csv(counter):
    filename = f'datasensors{counter}.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Vibration','Temperature', 'Force'])
        for data_point in csv_data:
            csvwriter.writerow(data_point)
# Start a separate thread to continuously update data and plots
data_thread = threading.Thread(target=update_plot)
data_thread.daemon = True
data_thread.start()

# Function to update the 1st plot
def update_plot1():
    with data_lock:
        lines1.set_xdata(np.arange(0, len(vibration)))
        lines1.set_ydata(vibration)
    canvas1.draw()

# Function to update the 2nd plot
def update_plot2():
    with data_lock:
        lines2.set_xdata(np.arange(0, len(temperature)))
        lines2.set_ydata(temperature)
    canvas2.draw()

# # Function to update the third plot
# def update_plot3():
#     with data_lock:
#         lines3.set_xdata(np.arange(0, len(pulses)))
#         lines3.set_ydata(pulses)
#     canvas3.draw()

# Function to update the fourth plot
def update_plot4():
    with data_lock:
        lines4.set_xdata(np.arange(0, len(force)))
        lines4.set_ydata(force)
    canvas4.draw()

def updateplots():
    update_plot1()
    update_plot2()
   # update_plot3()
    update_plot4()

# Function to send commands to Arduino
def send_command(command):
    ser.write(command.encode('utf-8'))

# Function to update the serial connection with selected COM port and baud rate
def update_serial_connection():
    selected_com_port = com_port_combo.get()
    selected_baud_rate = baud_rate_combo.get()
    
    global ser
    try:
        ser.close()
        ser = serial.Serial(selected_com_port, int(selected_baud_rate))
        ser.reset_input_buffer()
        print(f'Connection on {ser} successful')
    except serial.SerialException as e:
        print(f'Error: {e}. Connection on {selected_com_port} not found.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

# Initialize tkinter window
root = ctk.CTk()
root.title("READ SENSORS GUI:          ONE AXIS AUTOMATED DRILL")
root.configure(background='lightblue')

# Serial communication setup
ser = serial.Serial()  # Initialize with default values
#ser.reset_input_buffer()

# Create GUI components
root.update()

combined_halves = ctk.CTkFrame(root)
left_half = ctk.CTkFrame(combined_halves)
right_half = ctk.CTkFrame(combined_halves)

group_1 = ctk.CTkFrame(left_half)
group_1a = ctk.CTkFrame(group_1)
group_1b = ctk.CTkFrame(group_1)

group_2=ctk.CTkFrame(left_half)
group_2a=ctk.CTkFrame(group_2)
group_2b=ctk.CTkFrame(group_2)
group_2c=ctk.CTkFrame(group_2)
group_2d=ctk.CTkFrame(group_2)
group_2e=ctk.CTkFrame(group_2)

group_3=ctk.CTkFrame(left_half)
group_3a=ctk.CTkFrame(group_3)
group_3b=ctk.CTkFrame(group_3)

group_4=ctk.CTkFrame(left_half)
group_4a=ctk.CTkFrame(group_4)
group_4b=ctk.CTkFrame(group_4)
group_4c=ctk.CTkFrame(group_4)

group_r_1=ctk.CTkFrame(right_half)
group_r_1a=ctk.CTkFrame(group_r_1)
group_r_1b=ctk.CTkFrame(group_r_1)

group_r_2=ctk.CTkFrame(right_half)
group_r_2a=ctk.CTkFrame(group_r_2)
group_r_2b=ctk.CTkFrame(group_r_2)

start_button = ctk.CTkButton(group_r_1a, text="Start Plot", command=start_plotting)
stop_button = ctk.CTkButton(group_r_1a, text="Stop Plot", command=stop_plotting)
temp_label = ctk.CTkLabel(group_4a,text="Temperature: ",font=("Helvetica",15))
vib_label = ctk.CTkLabel(group_4b, text="Vibration: ",font=("Helvetica",15))
force_label = ctk.CTkLabel(group_4c, text="Force: ",font=("Helvetica",15))
# switch_1 = ctk.CTkSwitch(master=group_1b, text={dark_mode}, command=toggle_dark_mode)
switch_1 = ctk.CTkSwitch(master=group_1b, text='Light Mode' if dark_mode else 'Dark Mode' , command=toggle_dark_mode)

# Dropdown menu for COM port selection
com_port_label = ctk.CTkLabel(group_2a, text="Select COM Port:")
com_port_label.grid(row=1, column=0, sticky="w",padx=10,pady=5)
com_ports = ["COM1", "COM2", "COM3", "COM4","COM5","COM6",
             "COM7","COM8","COM9","COM10","COM11","COM12","COM13",
             "COM14","COM15","COM16","COM17","COM18","COM19","COM20"]
com_port_combo = ttk.Combobox(group_2b, values=com_ports)
com_port_combo.set("COM1")  # Set a default COM port

# Dropdown menu for baud rate selection
baud_rate_label = ctk.CTkLabel(group_2c, text="Select Baud Rate:")
baud_rate_label.grid(row=2, column=0, sticky="w",padx=10,pady=5)
baud_rates = ["9600", "115200", "57600", "38400"]  # Replace with your available baud rates
baud_rate_combo = ttk.Combobox(group_2d, values=baud_rates)
baud_rate_combo.set("9600")  # Set a default baud rate

# Button to update the serial connection with selected COM port and baud rate
update_button = ctk.CTkButton(group_2e, text="Update Serial Connection", command=update_serial_connection)

# Matplotlib setup for the 1st plot
fig1 = Figure(figsize=(5,3))
ax1 = fig1.add_subplot(111)
ax1.set_title("Vibration")
#ax2.set_xlabel("Time")
ax1.set_ylabel("Vibration")
ax1.grid(True)
ax1.set_xlim([0, 50])
ax1.set_ylim([-30, 30])
lines1 = ax1.plot([], [])[0]
canvas1 = FigureCanvasTkAgg(fig1, master=group_r_2a)
canvas1.draw()

# Matplotlib setup for the 2nd plot
fig2 = Figure(figsize=(5,3))
ax2 = fig2.add_subplot(111)
ax2.set_title("Temperature")
#ax1.set_xlabel("Time")
ax2.set_ylabel("Temperature")
ax2.grid(True)
ax2.set_xlim([0, 50])
ax2.set_ylim([10, 50])
lines2 = ax2.plot([], [])[0]
canvas2 = FigureCanvasTkAgg(fig2, master=group_r_2a)

# # Matplotlib setup for the third plot
# fig3 = Figure(figsize=(5,3))
# ax3 = fig3.add_subplot(111)
# ax3.set_title("PWM")
# #ax3.set_xlabel("Time")
# ax3.set_ylabel("pwm")
# ax3.grid(True)
# ax3.set_xlim([0, 50])
# ax3.set_ylim([0, 260])
# lines3 = ax3.plot([], [])[0]
# canvas3 = FigureCanvasTkAgg(fig3, master=root)
# canvas3.get_tk_widget().grid(row=5, column=3, columnspan=1,rowspan=4,padx=20, pady=10)
# canvas3.draw()

# Matplotlib setup for the fourth plot
fig4 = Figure(figsize=(5,3))
ax4 = fig4.add_subplot(111)
ax4.set_title("Force")
#ax3.set_xlabel("Time")
ax4.set_ylabel("force in kg")
ax4.grid(True)
ax4.set_xlim([0, 50])
ax4.set_ylim([-0.5, 4])
lines4 = ax4.plot([], [])[0]
canvas4 = FigureCanvasTkAgg(fig4, master=group_r_2b)
canvas4.draw()

# Grid layout
com_port_label.pack(padx=5, pady=5)
com_port_combo.pack(padx=5,pady=5)
baud_rate_label.pack(padx=5,pady=5)
switch_1.pack(padx=10, pady=10)
start_button.pack(side='left',padx=5, pady=5)
stop_button.pack(side='right',padx=5, pady=5)
temp_label.pack(padx=5, pady=5)
vib_label.pack(padx=5, pady=5)
force_label.pack(padx=5, pady=5)
baud_rate_combo.pack(padx=5,pady=5)
update_button.pack(padx=5, pady=5)
canvas1.get_tk_widget().pack(side='left',padx=10, pady=10)
canvas2.get_tk_widget().pack(side='left', padx=10, pady=10)
canvas4.get_tk_widget().pack(side='left',padx=10, pady=10)
# canvas4.get_tk_widget().grid(row=5, column=4, columnspan=1,rowspan=4,padx=20, pady=10)

group_1b.pack(padx=5, pady=5, fill=ctk.X, expand=True)
group_1.pack(padx=5, pady=10, fill=ctk.X, expand=True)

group_2a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2c.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2d.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2e.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)

group_4a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_4b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_4c.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_4.pack(padx=5, pady=10, fill=ctk.X, expand=True)

group_r_1a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
# group_r_1b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_r_1.pack(padx=5, pady=10, fill=ctk.X, expand=True)

group_r_2a.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)
group_r_2b.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)
group_r_2.pack(padx=5, pady=10, fill=ctk.X, expand=True)

left_half.pack(side='left',padx=5, pady=5, fill=ctk.BOTH, expand=True)
right_half.pack(side='left',padx=5, pady=5, fill=ctk.BOTH, expand=True)
combined_halves.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True)

root.after(1, update_plot)
root.mainloop()

# python -m PyInstaller.__main__ --onefile read_sensors.py
