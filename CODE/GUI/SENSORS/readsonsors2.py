import tkinter as tk
from tkinter import ttk
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np
from matplotlib.figure import Figure
import csv

# Variables
is_plotting = False
temperature= np.array([])
vibration = np.array([])
# pulses = np.array([])
force=np.array([])
csv_data = []  # List to hold the data
data_counter = 0  # Counter for unique data files
max_data_points = 50

# Lock for synchronizing access to shared data
data_lock = threading.Lock()
# Function to start reading data from Arduino
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
            
            temp_label.config(text=f'Temperature: {temp}')
            #pwm_label.config(text=f'PWM: {pwm}')
            vib_label.config(text=f'Vibration: {vib}')
            force_label.config(text=f'Force: {foc}')
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
        csvwriter.writerow(['Temperature','Vibration', 'Force'])
        for data_point in csv_data:
            csvwriter.writerow(data_point)
# Start a separate thread to continuously update data and plots
data_thread = threading.Thread(target=update_plot)
data_thread.daemon = True
data_thread.start()

# Function to update the first plot
def update_plot1():
    with data_lock:
        lines1.set_xdata(np.arange(0, len(temperature)))
        lines1.set_ydata(temperature)
    canvas1.draw()

# Function to update the second plot
def update_plot2():
    with data_lock:
        lines2.set_xdata(np.arange(0, len(vibration)))
        lines2.set_ydata(vibration)
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
    ser.close()
    ser = serial.Serial(selected_com_port, int(selected_baud_rate))
    ser.reset_input_buffer()

# Initialize tkinter window
root = tk.Tk()
root.title("ONE AXIS AUTOMATED DRILL GRAPHICAL USER INTERFACE TO READ SENSORS")
root.configure(background='lightblue')

# Serial communication setup
ser = serial.Serial()  # Initialize with default values
#ser.reset_input_buffer()

# Create GUI components
root.update()
start_button = ttk.Button(root, text="Start Plot", command=start_plotting)
stop_button = ttk.Button(root, text="Stop Plot", command=stop_plotting)
temp_label = ttk.Label(root, text="Temperature: ",font=("Helvetica",10))
#pwm_label = ttk.Label(root, text="PWM: ",font=("Helvetica",10))
vib_label = ttk.Label(root, text="Vibration: ",font=("Helvetica",10))
force_label = ttk.Label(root, text="Force: ",font=("Helvetica",10))

# Dropdown menu for COM port selection
com_port_label = ttk.Label(root, text="Select COM Port:")
com_port_label.grid(row=1, column=0, sticky="w",padx=10,pady=5)
com_ports = ["COM1", "COM2", "COM3", "COM4","COM5"]  # Replace with your available COM ports
com_port_combo = ttk.Combobox(root, values=com_ports)
com_port_combo.grid(row=1, column=1,padx=10,pady=5)
com_port_combo.set("COM1")  # Set a default COM port

# Dropdown menu for baud rate selection
baud_rate_label = ttk.Label(root, text="Select Baud Rate:")
baud_rate_label.grid(row=2, column=0, sticky="w",padx=10,pady=5)
baud_rates = ["9600", "115200", "57600", "38400"]  # Replace with your available baud rates
baud_rate_combo = ttk.Combobox(root, values=baud_rates)
baud_rate_combo.grid(row=2, column=1,padx=10,pady=5)
baud_rate_combo.set("9600")  # Set a default baud rate

# Button to update the serial connection with selected COM port and baud rate
update_button = ttk.Button(root, text="Update Serial Connection", command=update_serial_connection)
update_button.grid(row=3, column=0, columnspan=2)

# Matplotlib setup for the first plot
fig1 = Figure(figsize=(5,3))
ax1 = fig1.add_subplot(111)
ax1.set_title("Temperature")
#ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature")
ax1.grid(True)
ax1.set_xlim([0, 50])
ax1.set_ylim([10, 50])
lines1 = ax1.plot([], [])[0]
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.get_tk_widget().grid(row=1, column=3, columnspan=1,rowspan=4,padx=20, pady=10)
# Matplotlib setup for the second plot
fig2 = Figure(figsize=(5,3))
ax2 = fig2.add_subplot(111)
ax2.set_title("Vibration")
#ax2.set_xlabel("Time")
ax2.set_ylabel("Vibration")
ax2.grid(True)
ax2.set_xlim([0, 50])
ax2.set_ylim([-30, 30])
lines2 = ax2.plot([], [])[0]
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().grid(row=1, column=4, columnspan=1,rowspan=4,padx=20, pady=10)
canvas2.draw()

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
canvas4 = FigureCanvasTkAgg(fig4, master=root)
canvas4.get_tk_widget().grid(row=5, column=4, columnspan=1,rowspan=4,padx=20, pady=10)
canvas4.draw()

# Grid layout
start_button.grid(row=6, column=3)
stop_button.grid(row=7, column=3)
temp_label.grid(row=6, column=0)
#pwm_label.grid(row=8, column=0)
vib_label.grid(row=7, column=0)
force_label.grid(row=8, column=0)
root.after(1, update_plot)
root.mainloop()