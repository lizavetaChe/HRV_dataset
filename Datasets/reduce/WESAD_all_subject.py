import pickle
import numpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import neurokit2 as nk

arr = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '13', '14', '15', '16', '17']
file = open('text.txt', 'w')
STRESS_1 = 0
c = 1
STRESS_2 = 0
c2 = 1
STRESS_3 = 0
c3 = 1
for i in arr:
    print(f'S{i}.pkl')
    file.write(f'S{i}.pkl'+'\n')
    with open(f'S{i}.pkl', 'rb') as f:
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
    # print(emotion_intervals)

    ### --- Emo plot ---
    # y = res2
    # x = [i for i in range(lenght)]
    # plt.plot(x, y)
    # plt.show()

    # --- EСG + stress ---
    first_point = emotion_intervals[2][0][0]
    end_point = emotion_intervals[2][0][1]+1
    print("Stress time: ", (end_point-first_point)/ind_minutes)
    file.write(f'Stress time: {(end_point-first_point)/ind_minutes}' + '\n')
    win = ind_minutes # 60 sec
    center = (end_point-first_point)//2

    ECG_stress_1 = res1[first_point:first_point+win].copy()
    ECG_stress_2 = res1[center-win//2:center+win//2+1].copy()
    ECG_stress_3 = res1[end_point-win:end_point].copy()

    signals_ECG_stress_1, info_ECG_stress_1 = nk.ecg_process(ECG_stress_1, sampling_rate=700)
    signals_ECG_stress_2, info_ECG_stress_2 = nk.ecg_process(ECG_stress_2, sampling_rate=700)
    signals_ECG_stress_3, info_ECG_stress_3 = nk.ecg_process(ECG_stress_3, sampling_rate=700)

    # # nk.ecg_plot(signals_ECG_stress, info_ECG_stress)
    # # plt.show()

    peaks_s_1, info_s_1 = nk.ecg_peaks(signals_ECG_stress_1, sampling_rate=700)
    peaks_s_2, info_s_2 = nk.ecg_peaks(signals_ECG_stress_2, sampling_rate=700)
    peaks_s_3, info_s_3 = nk.ecg_peaks(signals_ECG_stress_3, sampling_rate=700)

    # # nk.hrv(peaks_s, sampling_rate=700, show=True)
    # # plt.show()

    hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=700, show=True)
    STRESS_1 += int(hrv_indices_s_1['HRV_MeanNN'].iloc[0])
    print('STRESS_1: ', int(hrv_indices_s_1['HRV_MeanNN'].iloc[0]))
    file.write(f'STRESS_1: {int(hrv_indices_s_1["HRV_MeanNN"].iloc[0])}' + '\n')
    hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=700, show=True)
    STRESS_2 += int(hrv_indices_s_2['HRV_MeanNN'].iloc[0])
    print('STRESS_2: ', int(hrv_indices_s_2['HRV_MeanNN'].iloc[0]))
    file.write(f'STRESS_2: {int(hrv_indices_s_2["HRV_MeanNN"].iloc[0])}' + '\n')
    hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=700, show=True)
    STRESS_3 += int(hrv_indices_s_3['HRV_MeanNN'].iloc[0])
    print('STRESS_3: ', int(hrv_indices_s_3['HRV_MeanNN'].iloc[0]))
    file.write(f'STRESS_3: {int(hrv_indices_s_3["HRV_MeanNN"].iloc[0])}' + '\n')


print(STRESS_1/15, STRESS_2/15, STRESS_3/15)
file.write(f'mean_1: {STRESS_1/15}' + '\n')
file.write(f'mean_2: {STRESS_2/15}' + '\n')
file.write(f'mean_3: {STRESS_3/15}' + '\n')


file.close()
