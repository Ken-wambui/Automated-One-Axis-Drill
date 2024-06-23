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
pulses = np.array([])

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
        # switch_1
        
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
    canvas3.get_tk_widget().configure(bg = 'black' if dark_mode else 'white')
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
    global is_plotting,pulses,csv_data, data_counter
    while is_plotting:
        try:
            data = ser.readline().decode('utf-8').strip()
            comb_data= data.split(',')
            #if(len(comb_data)==3):
            
            pwm = comb_data[0]
            
            with data_lock:
                if len(pulses) < 50:
                    pulses = np.append(pulses, int(pwm[0:4]))                              
                else:
                    pulses[0:49] = pulses[1:50]
                    pulses[49] = float(pwm[0:4])

            # pwm_label.ure(text=f'PWM: {pwm}')
            pwm_label.configure(text=f'PWM: {pwm}')

                        # Append data to csv_data
            csv_data.append([pwm])

            # Check if data exceeds 200 points and save to a new CSV file
            if len(csv_data) >= max_data_points:
                save_data_to_csv(data_counter)
                data_counter += 1
                csv_data = []
            root.after(1, update_plot3)
        except Exception as e:
          print(e)
        #root.update()

# Function to save data to a CSV file with a unique identifier
def save_data_to_csv(counter):
    filename = f'datapwm{counter}.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['PWM'])
        for data_point in csv_data:
            csvwriter.writerow(data_point)


# Start a separate thread to continuously update data and plots
data_thread = threading.Thread(target=update_plot)
data_thread.daemon = True
data_thread.start()

# Function to update the third plot
def update_plot3():
    with data_lock:
        lines3.set_xdata(np.arange(0, len(pulses)))
        lines3.set_ydata(pulses)
    canvas3.draw()

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
root.title("MOTOR CONTROL GUI:          ONE AXIS AUTOMATED DRILL")
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

group_r_1=ctk.CTkFrame(right_half)
group_r_1a=ctk.CTkFrame(group_r_1)
group_r_1b=ctk.CTkFrame(group_r_1)

group_r_2=ctk.CTkFrame(right_half)

start_button = ctk.CTkButton(group_r_1a, text="Start Plot", command=start_plotting)
stop_button = ctk.CTkButton(group_r_1a, text="Stop Plot", command=stop_plotting)
pwm_label = ctk.CTkLabel(group_4a, text="PWM: ",font=("Helvetica",15))
fast_drill_speed_button = ctk.CTkButton(group_3a, text="FAST DRILL SPEED", command=lambda: send_command('fastdrill'))
slow_drill_speed_button = ctk.CTkButton(group_3b, text="SLOW DRILL SPEED", command=lambda: send_command('slowdrill'))
stop_machine_button = ctk.CTkButton(group_1a, text="STOP MACHINE", command=lambda: send_command('stopmachine'))
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

# Matplotlib setup for the third plot
fig3 = Figure(figsize=(6,4))
ax3 = fig3.add_subplot(111)
ax3.set_title("PWM")
#ax3.set_xlabel("Time")
ax3.set_ylabel("pwm")
ax3.grid(True)
ax3.set_xlim([0, 50])
ax3.set_ylim([0, 260])
lines3 = ax3.plot([], [])[0]
canvas3 = FigureCanvasTkAgg(fig3, master=group_r_2)
canvas3.draw()

# Grid layout
com_port_label.pack(padx=5, pady=5)
com_port_combo.pack(padx=5,pady=5)
baud_rate_label.pack(padx=5,pady=5)
switch_1.pack(padx=10, pady=10)
start_button.pack(side='left',padx=5, pady=5)
stop_button.pack(side='right',padx=5, pady=5)
pwm_label.pack(padx=5, pady=5)
baud_rate_combo.pack(padx=5,pady=5)
update_button.pack(padx=5, pady=5)

fast_drill_speed_button.pack(padx=10, pady=10)
slow_drill_speed_button.pack( padx=10, pady=10)
stop_machine_button.pack(padx=10, pady=10)

canvas3.get_tk_widget().pack(padx=10, pady=10)

group_1a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_1b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_1.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)

group_2a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2c.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2d.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2e.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_2.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)

group_3a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_3b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_3.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)

group_4a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_4.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)

group_r_1a.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
# group_r_1b.pack(padx=5, pady=5, fill=ctk.BOTH, expand=True)
group_r_1.pack(padx=5, pady=10, fill=ctk.X, expand=True)

group_r_2.pack(padx=5, pady=10, fill=ctk.BOTH, expand=True)

left_half.pack(side='left',padx=5, pady=5, fill=ctk.BOTH, expand=True)
right_half.pack(side='left',padx=5, pady=5, fill=ctk.BOTH, expand=True)
combined_halves.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True)

root.after(1, update_plot)
root.mainloop()

# python -m PyInstaller.__main__ --onefile run_motors.py