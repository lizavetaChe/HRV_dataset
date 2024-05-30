import pickle
import numpy
import neurokit2 as nk
from matplotlib import pyplot as plt

file = open('WESAD_shift__STRESS_10sec-1min.txt', 'w')
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

    lenght = len(ECG_stress)
    ind_minutes = 700*60

    win = ind_minutes  # 3 min
    shift = ind_minutes//60  # 1 min
    point = 0
    i=0

    file.write(f'Stress_time: {lenght/ind_minutes}' + '\n')
# - - - - - - - - - - - - - - - -
    while(point+win<=lenght):
        signal = ECG_stress[point:point+win]
        signals_ECG_stress, info_ECG_stress = nk.ecg_process(signal, sampling_rate=700)
        peaks_s, info_s = nk.ecg_peaks(signals_ECG_stress.ECG_Clean, sampling_rate=700)
        hrv_indices_s = nk.hrv(peaks_s, sampling_rate=700)
        file.write(f'STRESS_{i}: {float(hrv_indices_s["HRV_MeanNN"].iloc[0])}' + '\n')
        point = point+win-shift
        i+=1

    file.write('\n')

file.close()