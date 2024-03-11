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

res3_test = nk.signal_resample(res1, sampling_rate=700, desired_sampling_rate=256, method='interpolation')
res4_test = nk.signal_resample(res2, sampling_rate=700, desired_sampling_rate=256, method='interpolation')

if (len(res3_test)==len(res4_test)):
    print('Good')

lenght = len(res3_test)
ind_minutes = lenght//36+1

# --- Are all emotions? ---
# unique_emo = list(set(res4_test))
# print(unique_emo)

res4 = [0 if x==-1 else x for x in res4_test]

# --- Emo plot ---
# y = res4
# x = [i for i in range(lenght)]
# plt.plot(x, y)
# plt.show()

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
end_point = emotion_intervals[2][2][1]+1
print("Stress time: ", (end_point-first_point)/ind_minutes)
win = ind_minutes//2+1 # 30 sec
center = (end_point-first_point)//2

ECG_stress_1 = res3_test[first_point:first_point+win].copy()
ECG_stress_2 = res3_test[center-win//2:center+win//2+1].copy()
ECG_stress_3 = res3_test[end_point-win:end_point].copy()

signals_ECG_stress_1, info_ECG_stress_1 = nk.ecg_process(ECG_stress_1)
signals_ECG_stress_2, info_ECG_stress_2 = nk.ecg_process(ECG_stress_2)
signals_ECG_stress_3, info_ECG_stress_3 = nk.ecg_process(ECG_stress_3)

# nk.ecg_plot(signals_ECG_stress_1, info_ECG_stress_1)
# plt.show()

peaks_s_1, info_s_1 = nk.ecg_peaks(signals_ECG_stress_1, sampling_rate=256)
peaks_s_2, info_s_2 = nk.ecg_peaks(signals_ECG_stress_2, sampling_rate=256)
peaks_s_3, info_s_3 = nk.ecg_peaks(signals_ECG_stress_3, sampling_rate=256)

# nk.hrv(peaks_s_1, sampling_rate=256, show=True)
# plt.show()

hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=256, show=True)
print('STRESS_1: \n', hrv_indices_s_1)
hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=256, show=True)
print('STRESS_2: \n', hrv_indices_s_2)
hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=256, show=True)
print('STRESS_3: \n', hrv_indices_s_3)

# --- EСG + base ---
first_point_base = emotion_intervals[1][0][0]
end_point_base = emotion_intervals[1][0][1]+1
print("Baseline: ", (end_point_base-first_point_base)/ind_minutes)
center_base = (end_point_base-first_point_base)//2
#
ECG_base_1 = res3_test[first_point_base:first_point_base+win].copy()
ECG_base_2 = res3_test[center_base-win//2:center_base+win//2+1].copy()
ECG_base_3 = res3_test[end_point_base-win:end_point_base].copy()

signals_ECG_base_1, info_ECG_base_1 = nk.ecg_process(ECG_base_1, sampling_rate=256)
signals_ECG_base_2, info_ECG_base_2 = nk.ecg_process(ECG_base_2, sampling_rate=256)
signals_ECG_base_3, info_ECG_base_3 = nk.ecg_process(ECG_base_3, sampling_rate=256)

# nk.ecg_plot(signals_ECG_stress, info_ECG_stress)
# plt.show()

peaks_b_1, info_b_1 = nk.ecg_peaks(signals_ECG_base_1, sampling_rate=256)
peaks_b_2, info_b_2 = nk.ecg_peaks(signals_ECG_base_2, sampling_rate=256)
peaks_b_3, info_b_3 = nk.ecg_peaks(signals_ECG_base_3, sampling_rate=256)

# nk.hrv(peaks_s, sampling_rate=256, show=True)
# plt.show()

hrv_indices_b_1 = nk.hrv(peaks_b_1, sampling_rate=256, show=True)
print('BASE_1: \n', hrv_indices_b_1)
hrv_indices_b_2 = nk.hrv(peaks_b_2, sampling_rate=256, show=True)
print('BASE_2: \n', hrv_indices_b_2)
hrv_indices_b_3 = nk.hrv(peaks_b_3, sampling_rate=256, show=True)
print('BASE_3: \n', hrv_indices_b_3)
