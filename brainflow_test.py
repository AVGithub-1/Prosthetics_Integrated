import argparse
import time
from SWTrial2 import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
import collections
from features import *
from matplotlib import pyplot as plt
from scipy import signal

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
    board.start_stream ()
    time.sleep(5)  # wait for stream to start
    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    
    # data_channel1 = collections.deque(np.zeros(100))
    # data_channel2 = collections.deque(np.zeros(100))
    # data_channel3 = collections.deque(np.zeros(100))
    # data_channel4 = collections.deque(np.zeros(100))
    counter = 0
    while(counter < 3):       # main loop to stream data from board
        
        
        data = board.get_board_data(num_samples=150)[1:5]
        
        # data_channel1.popleft()
        # data_channel1.append(data[0][0])
        #
        # data_channel2.popleft()
        # data_channel2.append(data[1][0])
        #
        # data_channel3.popleft()
        # data_channel3.append(data[2][0])
        #
        # data_channel4.popleft()
        # data_channel4.append(data[3][0])

        # print(data)
        # print(data.shape)

        data_channel3 = data[2]


        # #filtering data: butter bandpass filter, notch filter, epoching
        # data = butter_bandpass_filter(np.array(data_channel3), low_pass_freq, high_pass_freq, params.sampling_rate)
        # data = notch_filter(data, notch_freq, params.sampling_rate)
        print(data.shape)
        b, a = signal.iirnotch(60, 30, params.sampling_rate)
        data = signal.filtfilt(b, a, data)
        print(data.shape)
        #data = process_epoch(data)
        # fft = np.fft.fft(data)
        # f = np.fft.fftfreq(len(fft), 1/params.sampling_rate)
        # plt.plot(f, np.abs(fft))
        # plt.show()
        # features = get_features(np.reshape(data, data.shape[0]), train_mode = 0)
        # print(features)
        # print(features.shape)
        counter += 1




        #filtering data: butter bandpass filter, notch filter, epoching
        




        

    board.stop_stream()
    board.release_session()



if __name__ == "__main__":
    main()

#for get_current_board_data() / channels:
#    {'accel_channels': [5, 6, 7], 'ecg_channels': [1, 2, 3, 4], 'eeg_channels': [1, 2, 3, 4], 'emg_channels': [1, 2, 3, 4], 'eog_channels': [1, 2, 3, 4], 'marker_channel': 14, 'name': 'Ganglion', 'num_rows': 15, 'package_num_channel': 0, 'resistance_channels': [8, 9, 10, 11, 12], 'sampling_rate': 200, 'timestamp_channel': 13}

# run command (check brainflow IP from openBCI GUI, ganglion board id = 1):
#     C:/Users/prana/AppData/Local/Microsoft/WindowsApps/python3.12.exe 
    #c:/Users/prana/Desktop/openBCI_brainflow_stream/brainflow_test.py --ip-address 225.1.1.1 --board-id 1 --serial-port COM5
#   board_id: 1 for ganglion, 0 for cyton
#   ip_address: address in openbci, shows when you start session
