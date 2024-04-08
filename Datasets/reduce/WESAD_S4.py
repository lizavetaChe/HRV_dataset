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

if (len(res1)==len(res2)):
    print('Good')
    lenght = len(res1)

#lenght = len(res1)

#  --- Are all emotions? ---
# unique_emo = list(set(res2))
# print(unique_emo)

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
print(emotion_intervals)

#  --- Emo plot ---
# y = res2
# x = [i for i in range(lenght)]
# plt.plot(x, y)
# plt.show()

#  --- EСG ---
ECG_signals, ECG_info = nk.ecg_process(res1, sampling_rate=700)
# print(ECG_signals)
nk.ecg_plot(ECG_signals, ECG_info)
plt.show()


#  --- HRV ---
peaks, info_ = nk.ecg_peaks(ECG_signals, sampling_rate=700)
nk.hrv(peaks, sampling_rate=700, show=True)
plt.show()


#  --- Metrics full set ---
hrv_indices = nk.hrv(peaks, sampling_rate=700, show=True)
print(hrv_indices)

#  --- EСG + stress ---
first_point = emotion_intervals[2][0][0]
end_point = emotion_intervals[2][0][1]
EСG_stress = res1[first_point:end_point+1].copy()
signals_EСG_stress, info_EСG_stress = nk.ecg_process(EСG_stress, sampling_rate=700)
peaks_s, info_s = nk.ecg_peaks(signals_EСG_stress, sampling_rate=700)
nk.hrv(peaks_s, sampling_rate=700, show=True)
#
# plt.show()
hrv_indices_s = nk.hrv(peaks_s, sampling_rate=700, show=True)
print('STRESS: \n', hrv_indices_s)

#  --- test borders ---
# EСG_stress_test = res1[first_point-10:end_point+11].copy()
# signals_EСG_stress_test, info_EСG_stress_test = nk.ecg_process(EСG_stress, sampling_rate=700)
# peaks_s_test, info_s_test= nk.ecg_peaks(signals_EСG_stress_test, sampling_rate=700)
# nk.hrv(peaks_s_test, sampling_rate=700, show=True)
# hrv_indices_s_1 = nk.hrv(peaks_s_test, sampling_rate=700, show=True)
# print('TEST: \n', hrv_indices_s_1)



# Plot
# fig = plt.gcf()
# fig.set_size_inches(10, 12, forward=True)
# fig.savefig("myfig.png")
