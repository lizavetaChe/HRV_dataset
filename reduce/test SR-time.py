import pickle
import numpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import neurokit2 as nk

with open('S4.pkl', 'rb') as f:
    data = pickle.load(f, encoding="bytes")
# print(data)

#  --- Get data ecg ---
signal_ecg = (data[b'signal'][b'chest'][b'ECG'])
res1 = []
res1 = list((np.array(signal_ecg)).reshape(len(signal_ecg), ))

#  --- Get data emotions ---
signal_emotions = (data[b'label'])
res2 = []
res2 = list((np.array(signal_emotions)).reshape(len(signal_emotions), ))

# if (len(res1)==len(res2)):
#     print('Good')
#     lenght = len(res1)

# lenght = len(res1)
# ind_minutes = lenght//36+1
# ind_minutes = lenght//(700*60)
c_emotion_1 = [x for x in res2 if (x != 0)]
ind_minutes_1 = len(c_emotion_1)//(700*60)
print(ind_minutes_1)

c_emotion_2 = [x for x in res2 if (x != 0 and x != 5 and x != 6 and x != 7)]
ind_minutes_2 = len(c_emotion_2)//(700*60)
print(ind_minutes_2)