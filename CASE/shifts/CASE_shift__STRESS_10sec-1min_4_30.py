import csv
import pandas as pd
import neurokit2 as nk

#        jstime  valence  arousal  video

arr_subject = ['4', '30']

file = open('CASE_shift__STRESS_10sec-1min_4_30.txt', 'w')

for i in arr_subject:

    file.write(f'{i},')
    print(f'S{i}' + '\n')

    with open(f'Emo/sub_{i}.csv', 'r') as csvfile:
        data_emo = pd.read_csv(f'Emo/sub_{i}.csv')

    with open(f'Signal/sub_{i}.csv', 'r') as csvfile:
        data_sign = pd.read_csv(f'Signal/sub_{i}.csv')

    #base_emo = data_emo.query('valence > 5 & arousal < 5')
    stress_emo = data_emo.query('valence < 5 & arousal > 5')

    dict_intervals = {}
    arr = list(stress_emo.index)
    count = 0
    count_interv = 0
    mas = []

    for i in range(len(arr)-1):
        if count == 0:
            dict_intervals[f'{count_interv}'] = [[data_emo.iloc[arr[i]]['jstime']]]

        count += 1
        if (arr[i+1] == arr[i] + 1):
            if (i == len(arr)-2):
                mas.append(count/(20 * 60))
                # dict_intervals[f'{count_interv}'][0].append(arr[i+1])
                dict_intervals[f'{count_interv}'][0].append(data_emo.iloc[arr[i + 1]]['jstime'])
                dict_intervals[f'{count_interv}'].append((count+1)/(20*60))
        else:
            mas.append(count/(20*60))
            dict_intervals[f'{count_interv}'][0].append(data_emo.iloc[arr[i]]['jstime'])
            dict_intervals[f'{count_interv}'].append(count/(20*60))
            count_interv+=1
            count = 0

    tmp_ecg = []
    ecg = []

    for i in dict_intervals.keys():
        start = dict_intervals[f'{i}'][0][0]
        end = dict_intervals[f'{i}'][0][1]

        tmp_ecg.append(data_sign.query(f'daqtime >= {start} & daqtime <= {end}')['ecg'].tolist())

    ecg = sum(tmp_ecg, [])
    print(len(ecg)/(1000*60))

    signals_ECG_stress, info_ECG_stress = nk.ecg_process(ecg, sampling_rate=1000)

    analyze_df_s = nk.ecg_analyze(signals_ECG_stress, sampling_rate=1000)

    peaks_s, info_s = nk.ecg_peaks(signals_ECG_stress.ECG_Clean, sampling_rate=1000)

    hrv_indices_s = nk.hrv(peaks_s, sampling_rate=1000)

    ind_minutes = 1000*60
    win = ind_minutes  # 1 min
    shift = ind_minutes//6  # 10 sec
    point = 0

    while(point+win<=len(ecg)):
        signal = ecg[point:point+win]
        signals_ECG_stress, info_ECG_stress = nk.ecg_process(signal, sampling_rate=1000)
        peaks_s, info_s = nk.ecg_peaks(signals_ECG_stress.ECG_Clean, sampling_rate=1000)
        hrv_indices_s = nk.hrv(peaks_s, sampling_rate=1000)
        file.write(f'{round(float(hrv_indices_s["HRV_MeanNN"].iloc[0]), 3)},')
        point = point+win-shift

    file.write(
        f'\n')


file.close()

# print(len(ecg)/(1000*60))
#
# print(mas)
# print(sum(mas))
# print(dict_intervals)

