#This code is the first attempt at writing software to integrate the EMG DAQ, ANN, and Hardware.

import pyfirmata
from pyfirmata import Arduino, SERVO
from time import sleep

# Initialize Arduino board
from pyOpenBCI import OpenBCICyton
import numpy as np
import time

# Initialize the time of the last print
last_print_time = time.time()

def process_data(sample):
    global last_print_time
    
    # Get the current time
    current_time = time.time()
    
    # Check if 0.3 seconds have passed since the last print
    if current_time - last_print_time >= 0.3:
        # Update the last print time
        last_print_time = current_time
        
        # 'sample' is an instance of the 'Sample' class from pyOpenBCI
        # You can access the channels data as a list using 'sample.channels_data'
        emg_data = np.array(sample.channels_data)
        
        print(emg_data)

port = 'COMX'  # Replace with the serial port you found
board = OpenBCICyton(port=port, daisy=False)


# Define servo pins for all 5 fingers
SERVO_PINS = [2, 3, 4, 5, 6]  # Adjust based on your setup

# Start streaming the data and processing it in real-time
board.start_stream(process_data)
# Configure servo pins
for pin in SERVO_PINS:
    board.digital[pin].mode = SERVO

# Function to move a finger to a specific angle
def move_finger(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.5)  # Adjust delay as needed

# Function to control hand movement based on neural network output
def control_hand(hand_unclench_output, finger_outputs):
    # Convert neural network outputs to servo angles
    hand_unclench_angle = int(hand_unclench_output * 180)
    finger_angles = [int(output * 180) for output in finger_outputs]

    # Move the hand to the unclenched position
    move_finger(SERVO_PINS[0], hand_unclench_angle)

    # Move each finger to the specified angle
    for i, angle in enumerate(finger_angles):
        move_finger(SERVO_PINS[i + 1], angle)

# Example usage with neural network outputs
neural_network_hand_output = 0.7  # Example value between 0 and 1
neural_network_finger_outputs = [0.3, 0.5, 0.8, 0.2, 0.6]  # Example values between 0 and 1

control_hand(neural_network_hand_output, neural_network_finger_outputs)
