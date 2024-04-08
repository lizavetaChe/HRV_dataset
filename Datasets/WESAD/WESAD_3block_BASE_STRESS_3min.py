import pickle
import numpy
import neurokit2 as nk
from matplotlib import pyplot as plt

file = open('3block_BASE_STRESS_1min.txt', 'w')
arr_subject = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '13', '14', '15', '16', '17']

for i in arr_subject:

    file.write(f'S{i}.pkl' + '\n')

    print(f'S{i}.pkl' + '\n')

    with open(f'S{i}.pkl', 'rb') as f:
        data = pickle.load(f, encoding="bytes")

#  --- Get data ecg ---
    signal_ecg = (data[b'signal'][b'chest'][b'ECG']).squeeze()

#  --- Get data emotions ---
    signal_emotions = (data[b'label']).squeeze()

    ECG_stress = signal_ecg[signal_emotions == 2]
    ECG_base = signal_ecg[signal_emotions == 1]

    lenght = len(ECG_stress)
    ind_minutes = 700*60
    win = 3*ind_minutes # 3 min
    center = (lenght)//2

    file.write(f'Stress_time: {lenght/ind_minutes}' + '\n')
# - - - - - - - - - - - - - - - -
    ECG_stress_1 = ECG_stress[:win]
    ECG_stress_2 = ECG_stress[center-win//2:center+win//2]
    ECG_stress_3 = ECG_stress[lenght-win:]

    signals_ECG_stress, info_ECG_stress = nk.ecg_process(ECG_stress, sampling_rate=700)

    signals_ECG_stress_1, info_ECG_stress_1 = nk.ecg_process(ECG_stress_1, sampling_rate=700)
    signals_ECG_stress_2, info_ECG_stress_2 = nk.ecg_process(ECG_stress_2, sampling_rate=700)
    signals_ECG_stress_3, info_ECG_stress_3 = nk.ecg_process(ECG_stress_3, sampling_rate=700)

    peaks_s, info_s = nk.ecg_peaks(signals_ECG_stress.ECG_Clean, sampling_rate=700)

    peaks_s_1, info_s_1 = nk.ecg_peaks(signals_ECG_stress_1.ECG_Clean, sampling_rate=700)
    peaks_s_2, info_s_2 = nk.ecg_peaks(signals_ECG_stress_2.ECG_Clean, sampling_rate=700)
    peaks_s_3, info_s_3 = nk.ecg_peaks(signals_ECG_stress_3.ECG_Clean, sampling_rate=700)

    hrv_indices_s = nk.hrv(peaks_s, sampling_rate=700)

    hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=700)
    hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=700)
    hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=700)

# - - - - - - - - - - - - - - - -
    ECG_base_1 = ECG_base[:win]
    ECG_base_2 = ECG_base[center - win // 2:center + win // 2]
    ECG_base_3 = ECG_base[lenght - win:]

    signals_ECG_base, info_ECG_base = nk.ecg_process(ECG_base, sampling_rate=700)

    signals_ECG_base_1, info_ECG_base_1 = nk.ecg_process(ECG_base_1, sampling_rate=700)
    signals_ECG_base_2, info_ECG_base_2 = nk.ecg_process(ECG_base_2, sampling_rate=700)
    signals_ECG_base_3, info_ECG_base_3 = nk.ecg_process(ECG_base_3, sampling_rate=700)

    peaks_b, info_b = nk.ecg_peaks(signals_ECG_base.ECG_Clean, sampling_rate=700)

    peaks_b_1, info_b_1 = nk.ecg_peaks(signals_ECG_base_1.ECG_Clean, sampling_rate=700)
    peaks_b_2, info_b_2 = nk.ecg_peaks(signals_ECG_base_2.ECG_Clean, sampling_rate=700)
    peaks_b_3, info_b_3 = nk.ecg_peaks(signals_ECG_base_3.ECG_Clean, sampling_rate=700)

    hrv_indices_b = nk.hrv(peaks_b, sampling_rate=700)

    hrv_indices_b_1 = nk.hrv(peaks_b_1, sampling_rate=700)
    hrv_indices_b_2 = nk.hrv(peaks_b_2, sampling_rate=700)
    hrv_indices_b_3 = nk.hrv(peaks_b_3, sampling_rate=700)

    file.write(f'STRESS: Mean: {float(hrv_indices_s["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_s["HRV_MedianNN"].iloc[0])}, '
               f'Max: {float(hrv_indices_s["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_s["HRV_MinNN"].iloc[0])}' + '\n')
    file.write(
        f'STRESS_1: Mean: {float(hrv_indices_s_1["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_s_1["HRV_MedianNN"].iloc[0])}, '
        f'Max: {float(hrv_indices_s_1["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_s_1["HRV_MinNN"].iloc[0])}' + '\n')
    file.write(
        f'STRESS_2: Mean: {float(hrv_indices_s_2["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_s_2["HRV_MedianNN"].iloc[0])}, '
        f'Max: {float(hrv_indices_s_2["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_s_2["HRV_MinNN"].iloc[0])}' + '\n')
    file.write(
        f'STRESS_3: Mean: {float(hrv_indices_s_3["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_s_3["HRV_MedianNN"].iloc[0])}, '
        f'Max: {float(hrv_indices_s_3["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_s_3["HRV_MinNN"].iloc[0])}' + '\n')

    file.write(f'BASE: Mean: {float(hrv_indices_b["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_b["HRV_MedianNN"].iloc[0])}, '
               f'Max: {float(hrv_indices_b["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_b["HRV_MinNN"].iloc[0])}' + '\n')
    file.write(
        f'BASE_1: Mean: {float(hrv_indices_b_1["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_b_1["HRV_MedianNN"].iloc[0])}, '
        f'Max: {float(hrv_indices_b_1["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_b_1["HRV_MinNN"].iloc[0])}' + '\n')
    file.write(
        f'BASE_2: Mean: {float(hrv_indices_b_2["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_b_2["HRV_MedianNN"].iloc[0])}, '
        f'Max: {float(hrv_indices_b_2["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_b_2["HRV_MinNN"].iloc[0])}' + '\n')
    file.write(
        f'BASE_3: Mean: {float(hrv_indices_b_3["HRV_MeanNN"].iloc[0])}, Median: {float(hrv_indices_b_3["HRV_MedianNN"].iloc[0])}, '
        f'Max: {float(hrv_indices_b_3["HRV_MaxNN"].iloc[0])}, Min: {float(hrv_indices_b_3["HRV_MinNN"].iloc[0])}' + '\n')

file.close()