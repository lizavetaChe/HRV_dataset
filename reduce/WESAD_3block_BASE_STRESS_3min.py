import pickle
import numpy
import neurokit2 as nk

file = open('S17_3block_STRESS_1min_NEW.txt', 'w')

with open('S17.pkl', 'rb') as f:
    data = pickle.load(f, encoding="bytes")
# print(data)

#  --- Get data ecg ---
signal_ecg = (data[b'signal'][b'chest'][b'ECG']).squeeze()

#  --- Get data emotions ---
signal_emotions = (data[b'label']).squeeze()

ECG_stress = signal_ecg[signal_emotions == 2]

lenght = len(ECG_stress)
ind_minutes = 700*60
win = ind_minutes # 3 min
center = (lenght)//2

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

hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=700)
hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=700)
hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=700)


print('STRESS_1: \n', hrv_indices_s_1)
print('STRESS_2: \n', hrv_indices_s_2)
print('STRESS_3: \n', hrv_indices_s_3)


file.write(f'STRESS_1: {int(hrv_indices_s_1["HRV_MeanNN"].iloc[0])}' + '\n')
file.write(f'STRESS_2: {int(hrv_indices_s_2["HRV_MeanNN"].iloc[0])}' + '\n')
file.write(f'STRESS_3: {int(hrv_indices_s_3["HRV_MeanNN"].iloc[0])}' + '\n')

file.close()