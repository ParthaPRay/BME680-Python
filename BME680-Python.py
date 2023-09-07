# Partha Pratim Ray, September 7, 2023
# First run the BME860-Serial.ino in Arduino in I2C mode
# Next run this python script in Raspberry Pi 4 while connecting the Arduino with Raspbeery Pi 4 via USB


import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import serial
from datetime import datetime

# Make sure Matplotlib is in interactive mode
plt.ion()

# Create a serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)

# Lists to hold data
data = {
    'temperature': [],
    'pressure': [],
    'humidity': [],
    'gas': []
}

# Colors for each subplot
colors = {
    'temperature': 'red',
    'pressure': 'blue',
    'humidity': 'green',
    'gas': 'purple'
}

# Titles for each subplot
titles = {
    'temperature': 'Temperature (*C)',
    'pressure': 'Pressure (hPa)',
    'humidity': 'Humidity (%)',
    'gas': 'Gas (KOhms)'
}

# Create a new figure with subplots
fig, axes = plt.subplots(4, 1, sharex=True, figsize=(10, 15))
fig.subplots_adjust(hspace=0.5, right=0.75)

# Set the title for the entire window
# Set the title for the entire window
current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date in YYYY-MM-DD format
fig.suptitle(f"BME680 Monitoring - {current_date}", fontsize=16)


timestamps = []
time_elapsed = 0  # in seconds

def synchronize():
    # Read lines until a full line (ending with '\n') is received
    while ser.read().decode('utf-8', errors='ignore') != '\n':
        pass

# Synchronize before starting the main loop
synchronize()

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(line)  # Debug: Print the received line

        # Split the data
        values = line.split(',')

        try:
            if len(values) == 4:
                data['temperature'].append(float(values[0]))
                data['pressure'].append(float(values[1]))
                data['humidity'].append(float(values[2]))
                data['gas'].append(float(values[3]))

                time_elapsed += 2  # because you have a pause of 2 seconds in your loop
                timestamps.append(time_elapsed)

        except ValueError:
            print(f"Error parsing line: {line}")
            continue

        # Clear and update plots
        for ax, (key, values) in zip(axes, data.items()):
            ax.clear()
            ax.plot(timestamps, values, label=titles[key], color=colors[key])
            ax.set_title(titles[key])
            ax.set_ylabel(titles[key])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                
        axes[-1].set_xlabel('Time (seconds)')
        plt.draw()
        plt.pause(2)

except KeyboardInterrupt:
    print("Plotting terminated by user")

finally:
    ser.close()
    plt.show(block=True)  # Explicitly show the plot at the end
