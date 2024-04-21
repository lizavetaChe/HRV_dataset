import csv
import pandas as pd
import neurokit2 as nk

#print(data['ecg'])
#        jstime  valence  arousal  video

arr_subject = [i for i in range(1, 31)]
#arr_subject = [1, 2]

file1 = open('CASE_BASE(5, 5)_3min_1.txt', 'w')
file2 = open('CASE_BASE(5, 5)_3min_2.txt', 'w')
file3 = open('CASE_BASE(5, 5)_3min_3.txt', 'w')

for i in arr_subject:

    # print(f'S{i}' + '\n')

    with open(f'Emo/sub_{i}.csv', 'r') as csvfile:
        data_emo = pd.read_csv(f'Emo/sub_{i}.csv')

    with open(f'Signal/sub_{i}.csv', 'r') as csvfile:
        data_sign = pd.read_csv(f'Signal/sub_{i}.csv')

    base_emo = data_emo.query('valence == 5 & arousal == 5')
    #stress_emo = data_emo.query('valence < 5 & arousal > 5')

    dict_intervals = {}
    arr = list(base_emo.index)
    count = 0
    count_interv = 0
    mas = []

    for j in range(len(arr)-1):
        if count == 0:
            dict_intervals[f'{count_interv}'] = [[data_emo.iloc[arr[j]]['jstime']]]

        count += 1
        if (arr[j+1] == arr[j] + 1):
            if (j == len(arr)-2):
                mas.append((count+1)/(20 * 60))
                # dict_intervals[f'{count_interv}'][0].append(arr[i+1])
                dict_intervals[f'{count_interv}'][0].append(data_emo.iloc[arr[j + 1]]['jstime'])
                dict_intervals[f'{count_interv}'].append((count+1)/(20*60))
        else:
            mas.append(count/(20*60))
            dict_intervals[f'{count_interv}'][0].append(data_emo.iloc[arr[j]]['jstime'])
            dict_intervals[f'{count_interv}'].append(count/(20*60))
            count_interv+=1
            count = 0

    tmp_ecg = []
    ecg = []

    # print(dict_intervals)

    for k in dict_intervals.keys():
        if dict_intervals[f'{k}'][1] >= 3:
            file1.write(f'{i},')
            file2.write(f'{i},')
            file3.write(f'{i},')
            print(i)
            start = dict_intervals[f'{k}'][0][0]
            end = dict_intervals[f'{k}'][0][1]

            center = end - start

            start1 = start
            end1 = start+(1000*60)

            start2 = center - (1000*30)
            end2 = center + (1000*30)

            start3 = end - (1000*60)
            end3 = end

            ecg1 = data_sign.query(f'daqtime >= {start1} & daqtime <= {end1}')['ecg'].tolist()
            ecg2 = data_sign.query(f'daqtime >= {start2} & daqtime <= {end2}')['ecg'].tolist()
            ecg3 = data_sign.query(f'daqtime >= {start3} & daqtime <= {end3}')['ecg'].tolist()


            signals_ECG_stress_1, info_ECG_stress_1 = nk.ecg_process(ecg1, sampling_rate=1000)
            signals_ECG_stress_2, info_ECG_stress_2 = nk.ecg_process(ecg2, sampling_rate=1000)
            signals_ECG_stress_3, info_ECG_stress_3 = nk.ecg_process(ecg3, sampling_rate=1000)

            analyze_df_s_1 = nk.ecg_analyze(signals_ECG_stress_1, sampling_rate=1000)
            analyze_df_s_2 = nk.ecg_analyze(signals_ECG_stress_2, sampling_rate=1000)
            analyze_df_s_3 = nk.ecg_analyze(signals_ECG_stress_3, sampling_rate=1000)

            peaks_s_1, info_s_1 = nk.ecg_peaks(signals_ECG_stress_1.ECG_Clean, sampling_rate=1000)
            peaks_s_2, info_s_2 = nk.ecg_peaks(signals_ECG_stress_2.ECG_Clean, sampling_rate=1000)
            peaks_s_3, info_s_3 = nk.ecg_peaks(signals_ECG_stress_3.ECG_Clean, sampling_rate=1000)

            hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=1000)
            hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=1000)
            hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=1000)

            file1.write(
                f'{round(float(analyze_df_s_1["ECG_Rate_Mean"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_1["HRV_MeanNN"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_SDNN"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_SDSD"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_RMSSD"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_pNN50"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_1["HRV_LF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_HF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_LFHF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_VLF"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_1["HRV_SD1"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_SD2"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_DFA_alpha1"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_1["HRV_SampEn"].iloc[0]), 3)}\n')

            file2.write(
                f'{round(float(analyze_df_s_2["ECG_Rate_Mean"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_2["HRV_MeanNN"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_SDNN"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_SDSD"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_RMSSD"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_pNN50"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_2["HRV_LF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_HF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_LFHF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_VLF"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_2["HRV_SD1"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_SD2"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_DFA_alpha1"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_2["HRV_SampEn"].iloc[0]), 3)}\n')

            file3.write(
                f'{round(float(analyze_df_s_3["ECG_Rate_Mean"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_3["HRV_MeanNN"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_SDNN"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_SDSD"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_RMSSD"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_pNN50"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_3["HRV_LF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_HF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_LFHF"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_VLF"].iloc[0]), 3)},'

                f'{round(float(hrv_indices_s_3["HRV_SD1"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_SD2"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_DFA_alpha1"].iloc[0]), 3)},'
                f'{round(float(hrv_indices_s_3["HRV_SampEn"].iloc[0]), 3)}\n')

file1.close()
file2.close()
file3.close()

# print(len(ecg)/(1000*60))
#
# print(max(mas))
# print(sum(mas))
# print(dict_intervals)

