import serial
import time
import numpy as np
from collections import deque
import threading
import pylsl
from scipy.signal import butter, filtfilt, welch

# Global variables
eeg_inlet = None
buffer = None
last_sample = 0
epoch_buffer = []

# Settings
fs = 250          # Sampling rate (Hz)
epoch_duration = 2  # Epoch duration in seconds
buffer_len = fs * epoch_duration  # Buffer length for one epoch

# Preprocessing parameters
high_pass_freq = 150  # High-pass filter cutoff frequency (Hz)
low_pass_freq = 50  # Low-pass filter cutoff frequency (Hz)
notch_freq = 60  # Notch filter frequency (Hz)

# Function to send data to Arduino
def send_data_to_arduino(data):
    ser.write(data.encode())

def lsl_thread():
    global buffer
    global last_sample
    global eeg_inlet
    global epoch_buffer
    global buffer_len
    
    while True:
        sample, times = eeg_inlet.pull_sample()
        if len(sample) > 0:
            last_sample = sample[0]  # Assuming single channel EEG data
            buffer.append(last_sample)
            epoch_buffer.append(last_sample)

            # Check if epoch buffer is full
            if len(epoch_buffer) >= buffer_len:
                # Process the epoch data
                process_epoch(epoch_buffer)

                # Clear the epoch buffer
                epoch_buffer.clear()

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def rms(data):
    return np.sqrt(np.mean(data ** 2))

def integral(data, dt):
    return np.sum(data) * dt

def derivative(data, dt):
    return np.gradient(data) / dt

def calculate_features(epoch_data, high_pass_freq, low_pass_freq, fs):
    # Apply high-pass, low-pass, and notch filters
    filtered_data = butter_bandpass_filter(epoch_data, high_pass_freq, low_pass_freq, fs)
    filtered_data = notch_filter(filtered_data, notch_freq, fs)

    # Calculate RMS
    rms_value = rms(filtered_data)

    # Calculate mean power spectrum
    freqs, psd = welch(filtered_data, fs=fs, nperseg=len(filtered_data))
    mean_power_spectrum = np.mean(psd)

    # Calculate integral
    dt = 1 / fs
    integral_value = integral(filtered_data, dt)

    # Calculate derivative
    derivative_value = derivative(filtered_data, dt)

    return rms_value, mean_power_spectrum, integral_value, derivative_value

def notch_filter(data, notch_freq, fs):
    nyq = 0.5 * fs
    notch_freq_normalized = notch_freq / nyq
    q_factor = 30  # Quality factor
    b, a = butter(2, [notch_freq_normalized - 1 / (2 * q_factor), notch_freq_normalized + 1 / (2 * q_factor)], btype='bandstop')
    return filtfilt(b, a, data)

def process_epoch(epoch_data):
    # Calculate features
    rms_value, mean_power_spectrum, integral_value, derivative_value = calculate_features(epoch_data)

    # Print or display the calculated features
    print("RMS:", rms_value)
    print("Mean Power Spectrum:", mean_power_spectrum)
    print("Integral:", integral_value)
    print("Derivative:", derivative_value)
    print("--------------------------")
    
    # Convert filtered data to string and send to Arduino
    data_str = ','.join(map(str, [rms_value, mean_power_spectrum, integral_value, derivative_value])) + '\n'
    #send_data_to_arduino(data_str)

# if __name__ == "__main__":
#     try:
#         ser
#     except NameError:
#         print("PySerial is not installed. Please install PySerial.")
#         exit()

#     # Initialize buffer and epoch buffer
#     buffer = deque(maxlen=buffer_len)
    
#     # Initialize LSL streams and create inlet
#     eeg_streams = pylsl.resolve_stream('type', 'EEG')
#     eeg_inlet = pylsl.stream_inlet(eeg_streams[0], recover=False)

#     # Initialize serial connection
#     SERIAL_PORT = 'COM1'  # Update the port accordingly
#     BAUD_RATE = 9600
#     ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
#     # Launch LSL thread
#     lsl = threading.Thread(target=lsl_thread, args=())
#     lsl.setDaemon(False)
#     lsl.start()
