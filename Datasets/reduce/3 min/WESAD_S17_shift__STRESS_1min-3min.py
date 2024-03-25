import pickle
import numpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import neurokit2 as nk

file = open('S17_shift__STRESS_1min-3min.txt', 'w')

with open('S17.pkl', 'rb') as f:
    data = pickle.load(f, encoding="bytes")
# print(data)

#  --- Get data ecg ---
signal_ecg = (data[b'signal'][b'chest'][b'ECG'])
res1 = np.array(signal_ecg).reshape(len(signal_ecg), )

#  --- Get data emotions ---
signal_emotions = (data[b'label'])
res2 = np.array(signal_emotions).reshape(len(signal_emotions), )

# if (len(res1)==len(res2)):
#     print('Good')
#     lenght = len(res1)

lenght = len(res1)
#ind_minutes = lenght//36+1
ind_minutes = 700*60
# print(ind_minutes)

def get_emotion_intervals(res2):
    dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    dict[res2[0]].append([0])
    for i in range(1, lenght - 1):
        if res2[i] == res2[i + 1]:
            if i + 1 == lenght - 1:
                dict[res2[i]][-1].append(i + 1)
            continue
        else:
            dict[res2[i]][-1].append(i)
            dict[res2[i + 1]].append([i + 1])
    return dict

emotion_intervals = get_emotion_intervals(res2)

# --- EСG + shift stress ---
first_point = emotion_intervals[2][0][0]
win = 3*ind_minutes # 3 min
shift = ind_minutes # 1 min
point = first_point
print("time: ", np.sum(res2 == 2)/ind_minutes)

for i in range(7):
    ECG_stress = res1[point:(point + win + 1)].copy()
    signals_ECG_stress, info_ECG_trans_stress = nk.ecg_process(ECG_stress, sampling_rate=700)
    peaks_t_s, info_t_s = nk.ecg_peaks(signals_ECG_stress, sampling_rate=700)
    hrv_indices_t_s = nk.hrv(peaks_t_s, sampling_rate=700, show=True)
    point = point+win-shift
    print(res2[point])
    print("\nIteration: ", i, hrv_indices_t_s)
    file.write(f'{i}: {res2[point]} - {int(hrv_indices_t_s["HRV_MeanNN"].iloc[0])}' + '\n')

# nk.ecg_plot(signals_ECG_stress, info_ECG_stress)
# plt.show()
# nk.hrv(peaks_s, sampling_rate=700, show=True)
# plt.show()

file.close()
