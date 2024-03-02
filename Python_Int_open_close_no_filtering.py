import argparse
import time
from SWTrial2 import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
import collections
from features import *
import numpy as np
import serial

def send_through_serial(data):
    # Initialize serial connection
    ser = serial.Serial('COM1', 9600)  # Change 'COM1' to your COM port and 9600 to your baud rate
    ser.write(data.encode())  # Write data to serial port
    ser.close()  # Close serial connection

def main():
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board
    params.sampling_rate = 350

    print(params.ip_address, type(params.ip_address))
    print(params.serial_port, type(params.serial_port))

    board = BoardShim(args.board_id, params)
    board.prepare_session()
    board.start_stream()
    time.sleep(5)  # wait for stream to start
    
    # Set threshold value
    threshold = 0.5 # Change this depending on rest EMG
    window_size = 100  # Change this value as needed

    data_channels = [collections.deque(np.zeros(window_size)) for _ in range(4)]
    
    while True:  # main loop to stream data from board
        data = board.get_current_board_data(args.board_id)[1:5]

        # Update the deque for each channel
        for i in range(4):
            data_channels[i].popleft()
            data_channels[i].append(data[i][0])

        # Calculate the mean of the data within each window
        means = [np.mean(channel) for channel in data_channels]

        # Rectify and threshold the mean data for each channel
        thresholded_data = [1 if abs(mean) > threshold else 0 for mean in means]

        # Check if 3 out of 4 channels go over threshold
        if sum(thresholded_data) >= 3:
            # Send '1' through COM port
            send_through_serial('1')
        else:
            # Send '0' through COM port
            send_through_serial('0')
        
        time.sleep(0.01)  # Adjust sleep time as needed

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
