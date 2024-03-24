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
res1 = np.array(signal_ecg).reshape(len(signal_ecg), )

#  --- Get data emotions ---
signal_emotions = (data[b'label'])
res2 = np.array(signal_emotions).reshape(len(signal_emotions), )

res3_test = nk.signal_resample(res1, sampling_rate=700, desired_sampling_rate=256, method='interpolation')
res4_test = nk.signal_resample(res2, sampling_rate=700, desired_sampling_rate=256, method='interpolation')

lenght = len(res3_test)
res4 = [0 if x==-1 else x for x in res4_test]

def get_emotion_intervals(res):
    dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    dict[res[0]].append([0])
    for i in range(1, lenght - 1):
        if res[i] == res[i + 1]:
            if i + 1 == lenght - 1:
                dict[res[i]][-1].append(i + 1)
            continue
        else:
            dict[res[i]][-1].append(i)
            dict[res[i + 1]].append([i + 1])
    return dict


emotion_intervals = get_emotion_intervals(res4)
print(emotion_intervals)

# --- EСG + stress ---
first_point = emotion_intervals[2][2][0]
end_point = emotion_intervals[2][2][1]
ECG_stress = res3_test[first_point:end_point].copy()
signals_ECG_stress, info_ECG_stress = nk.ecg_process(ECG_stress, sampling_rate=256)
#nk.ecg_plot(signals_ECG_stress, info_ECG_stress )
#plt.show()
peaks_s, info_s = nk.ecg_peaks(signals_ECG_stress, sampling_rate=256)
# nk.hrv(peaks_s, sampling_rate=256, show=True)
# plt.show()
hrv_indices_s = nk.hrv(peaks_s, sampling_rate=256, show=True)
print('STRESS: \n', hrv_indices_s)