import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
#the point of this file is to get the five features we want as inputs for our model:
# - fft decomposition
# - mean average value
# - variance
# - standard deviation
# - energy


def get_features(s, train_mode = 1):
    """
    gets the features we want from the data, as well as the labels of each sample
    """

    np_s = s
    print(np_s.shape)
    
    for i in range(np_s.shape[0]):

        #for training/validation of model
        if train_mode == 1:
            features = np.empty(shape = (np_s.shape[0],11+2*len(np_s)), dtype = float)

            #for labels
            if np_s.iloc[i,0] == 'O':
                features[i,0:7] = np.array([1.0,0.0,0.0,0.0,0.0,0.0,0.0])
            if np_s.iloc[i,0] == 'U':
                features[i,0:7] = np.array([0.0,1.0,0.0,0.0,0.0,0.0,0.0])
            if np_s.iloc[i,0] == 'R':
                features[i,0:7] = np.array([0.0,0.0,1.0,0.0,0.0,0.0,0.0])
            if np_s.iloc[i,0] == 'T':
                features[i,0:7] = np.array([0.0,0.0,0.0,1.0,0.0,0.0,0.0])
            if np_s.iloc[i,0] == 'M':
                features[i,0:7] = np.array([0.0,0.0,0.0,0.0,1.0,0.0,0.0])
            if np_s.iloc[i,0] == 'I':
                features[i,0:7] = np.array([0.0,0.0,0.0,0.0,0.0,1.0,0.0])
            if np_s.iloc[i,0] == 'P':
                features[i,0:7] = np.array([0.0,0.0,0.0,0.0,0.0,0.0,1.0])
        
            np_s_i = np_s.iloc[i]
            #print(np_s_i.shape)
            #for j in range(np_s_i.shape[0]):
                #if j>0:
                #  if math.isnan(np_s_i[j]):
                #      np_s_i = np.delete(arr = np_s_i, obj = j)
                #     print(np_s_i.shape[0])
            
            j = 1

            while j <= np_s_i.shape[0]:
                if j >= np_s_i.shape[0]:
                    break
                elif math.isnan(np_s_i[j]):
                    np_s_i = np.delete(arr = np_s_i, obj = j)
                    #print(np_s_i.shape[0])
                else:
                    j+=1



            # fft( article uses mean of fft, so maybe consider that )
            fft_arr = np.fft.fft(np_s_i[3:])
            features[i,7:7+len(fft_arr)] = fft_arr
            #print(np.mean(fft_arr))

            #variance
            features[i,8+len(fft_arr)] = np.var(np_s_i[3:])
            #print(np.var(np_s_i[3:]))

            #standard deviation
            features[i,9+len(fft_arr)] = np.std(np_s_i[ 3:])
            #print(np.std(np_s_i[ 3:]))

            #mean average value
            features[i,10+len(fft_arr)] = np.mean(np_s_i[3:])
            #print(np.mean(np_s_i[3:]))

            #energy(still needs to be done)
            energy_k = 0
            energy = []
            for j in np_s_i[3:]:
                energy_k += j**2
                energy.append(energy_k)
            features[i,11+len(fft_arr):11+len(fft_arr)+len(energy)] = energy
            #print(len(energy))

         #for real time streaming
        elif train_mode == 0: 
            features = np.empty(shape = (np_s.shape[0],2*len(np_s)), dtype = float)
            # j = 1
            # while j <= np_s.shape[0]:
            #     if j >= np_s.shape[0]:
            #         break
            #     elif True in np.isnan(np_s_i[j]):
            #         np_s = np.delete(arr = np_s, obj = j)
            #         #print(np_s_i.shape[0])
            #     else:
            #         j+=1

            # fft( article uses mean of fft, so maybe consider that )
            fft_arr = np.fft.fft(np_s[3:])
            features[i,0:len(fft_arr)] = fft_arr
            #print(np.mean(fft_arr))

            #variance
            features[i,len(fft_arr)] = np.var(np_s[3:])
            #print(np.var(np_s_i[3:]))

            #standard deviation
            features[i,1+len(fft_arr)] = np.std(np_s[ 3:])
            #print(np.std(np_s_i[ 3:]))

            #mean average value
            features[i,2+len(fft_arr)] = np.mean(np_s[3:])
            #print(np.mean(np_s_i[3:]))

            #energy(still needs to be done)
            energy_k = 0
            energy = []
            for j in np_s[3:]:
                energy_k += j**2
                energy.append(energy_k)
            features[i,3+len(fft_arr):3+len(fft_arr)+len(energy)] = energy
    #features = np.hstack((np_s[:,0], features))
    #print(features) 
    return features


    