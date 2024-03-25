import pickle
import numpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import neurokit2 as nk

file = open('S17_3block_BASE+STRESS_60.txt', 'w')

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
print(emotion_intervals)

### --- Emo plot ---
# y = res2
# x = [i for i in range(lenght)]
# plt.plot(x, y)
# plt.show()

# --- EСG + stress ---
first_point = emotion_intervals[2][0][0]
end_point = emotion_intervals[2][0][1]+1
print("Stress time: ", (end_point-first_point)/ind_minutes)
win = ind_minutes # 60 sec
center = (end_point-first_point)//2 

ECG_stress_1 = res1[first_point:first_point+win].copy()
ECG_stress_2 = res1[center-win//2:center+win//2+1].copy()
ECG_stress_3 = res1[end_point-win:end_point].copy()

signals_ECG_stress_1, info_ECG_stress_1 = nk.ecg_process(ECG_stress_1, sampling_rate=700)
signals_ECG_stress_2, info_ECG_stress_2 = nk.ecg_process(ECG_stress_2, sampling_rate=700)
signals_ECG_stress_3, info_ECG_stress_3 = nk.ecg_process(ECG_stress_3, sampling_rate=700)

# nk.ecg_plot(signals_ECG_stress, info_ECG_stress)
# plt.show()

peaks_s_1, info_s_1 = nk.ecg_peaks(signals_ECG_stress_1, sampling_rate=700)
peaks_s_2, info_s_2 = nk.ecg_peaks(signals_ECG_stress_2, sampling_rate=700)
peaks_s_3, info_s_3 = nk.ecg_peaks(signals_ECG_stress_3, sampling_rate=700)

# nk.hrv(peaks_s, sampling_rate=700, show=True)
# plt.show()

hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=700, show=True)
print('STRESS_1: \n', hrv_indices_s_1)
file.write(f'STRESS_1: {int(hrv_indices_s_1["HRV_MeanNN"].iloc[0])}' + '\n')
hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=700, show=True)
print('STRESS_2: \n', hrv_indices_s_2)
file.write(f'STRESS_2: {int(hrv_indices_s_2["HRV_MeanNN"].iloc[0])}' + '\n')
hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=700, show=True)
print('STRESS_3: \n', hrv_indices_s_3)
file.write(f'STRESS_3: {int(hrv_indices_s_3["HRV_MeanNN"].iloc[0])}' + '\n')

# --- EСG + base ---
first_point_base = emotion_intervals[1][0][0]
end_point_base = emotion_intervals[1][0][1]+1
print("Baseline: ", (end_point_base-first_point_base)/ind_minutes)
center_base = (end_point_base-first_point_base)//2
#
ECG_base_1 = res1[first_point_base:first_point_base+win].copy()
ECG_base_2 = res1[center_base-win//2:center_base+win//2+1].copy()
ECG_base_3 = res1[end_point_base-win:end_point_base].copy()

signals_ECG_base_1, info_ECG_base_1 = nk.ecg_process(ECG_base_1, sampling_rate=700)
signals_ECG_base_2, info_ECG_base_2 = nk.ecg_process(ECG_base_2, sampling_rate=700)
signals_ECG_base_3, info_ECG_base_3 = nk.ecg_process(ECG_base_3, sampling_rate=700)

# nk.ecg_plot(signals_ECG_stress, info_ECG_stress)
# plt.show()

peaks_b_1, info_b_1 = nk.ecg_peaks(signals_ECG_base_1, sampling_rate=700)
peaks_b_2, info_b_2 = nk.ecg_peaks(signals_ECG_base_2, sampling_rate=700)
peaks_b_3, info_b_3 = nk.ecg_peaks(signals_ECG_base_3, sampling_rate=700)

# # nk.hrv(peaks_s, sampling_rate=700, show=True)
# # plt.show()

hrv_indices_b_1 = nk.hrv(peaks_b_1, sampling_rate=700, show=True)
print('BASE_1: \n', hrv_indices_b_1)
file.write(f'BASE_1: {int(hrv_indices_b_1["HRV_MeanNN"].iloc[0])}' + '\n')
hrv_indices_b_2 = nk.hrv(peaks_b_2, sampling_rate=700, show=True)
print('BASE_2: \n', hrv_indices_b_2)
file.write(f'BASE_2: {int(hrv_indices_b_2["HRV_MeanNN"].iloc[0])}' + '\n')
hrv_indices_b_3 = nk.hrv(peaks_b_3, sampling_rate=700, show=True)
print('BASE_3: \n', hrv_indices_b_3)
file.write(f'BASE_3: {int(hrv_indices_b_3["HRV_MeanNN"].iloc[0])}' + '\n')

file.close()