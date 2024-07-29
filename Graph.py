import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial as srl
import csv

# Configure the serial port and baud rate
serial_port = 'COM13'  # Change this to your actual serial port
baud_rate = 9600

# Initialize the serial connection
ser = srl.Serial(serial_port, baud_rate)

# Initialize lists to store the data
time = []
height = []

# Create a figure and axis
fig, ax = plt.subplots()
line, = ax.plot(height, time)





def update(frame):
    line.set_data(height, time)
    ax.relim()
    ax.autoscale_view()
    return line,


def animate(i):
    # Read a line of data from the serial port
    line = ser.readline().decode('utf-8').strip()
    try:
        # Split the line into x and y values
        x_str, y_str = line.split(',')
        x_value = float(x_str)
        y_value = float(y_str)

        # Append the x and y values to the lists
        time.append(x_value)
        height.append(y_value)

        # Keep only the last 1000 data points to avoid memory issues
        if len(time) > 1000:
            time.pop(0)
            height.pop(0)

        # Update the plot
        ax.clear()
        ax.plot(height, time)
        plt.title('Experimento Massa-Mola')
        plt.xlabel('t[s]')
        plt.ylabel('y[cm]')

        with open('Dados_Massa_Mola.csv','w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['height','time'])
            for item1, item2 in zip(height, time):
                writer.writerow([item1,item2])


    except ValueError:
        pass


# Set up the animation
ani = animation.FuncAnimation(fig, animate, interval=10)

# Display the plot
plt.show()

# Close the serial connection when done
ser.close()
