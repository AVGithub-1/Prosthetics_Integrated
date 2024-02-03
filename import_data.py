import json
import pandas as pd
import numpy as np

# Read data

num_jsons = 34


all_data = pd.DataFrame()


# this takes all of the json files with filtered data that we have, and puts them all into one big json file


# for i in range(num_jsons):
#     filepath = "data/EMG_hand_data"+str(i)+".json"
#     with open(filepath) as json_file:
#         data = json.load(json_file)

EMG_filepath = "../data/emg_recordings/EMG_hand_data.json"       
        
with open(EMG_filepath) as json_file:
         data = json.load(json_file)

def load_2D(data, key):
    '''
    Creates a dataframe out of filtered EMG data that we collect
    '''
    
    
    # Iterate through list elements to flatten
    l = []
    for s in data[key]['data']:
        l_ = []
        # Manually append first 3 elements
        l_.append(s[0])
        l_.append(s[1])
        l_.append(s[2])
        
        # Iterate through array element and append
        for d in s[3]:
            l_.append(d)
            
        # Finally append to L
        l.append(l_)
        
    # Also flatten header
    h = []
    head = data[key]['header']
    h.append(head[0])
    h.append(head[1])
    h.append(head[2])
    for t in head[3]:
        h.append(t)
        
    return pd.DataFrame(l, columns=h)

#     for i in ['U', 'T', 'I', 'M', 'R', 'P']:


df_U = load_2D(data, 'U')
df_T = load_2D(data, 'T')
df_I = load_2D(data, 'I')
df_M = load_2D(data, 'M')
df_R = load_2D(data, 'R')
df_P = load_2D(data, 'P')


new_data = pd.concat([df_U, df_T, df_I, df_M, df_R, df_P], ignore_index=True)



# print(all_data.shape)

