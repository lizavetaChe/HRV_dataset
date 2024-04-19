import pickle
import numpy
import neurokit2 as nk
from matplotlib import pyplot as plt

file = open('WESAD_STRESS_T.txt', 'w')

arr_subject = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '13', '14', '15', '16', '17']

for i in arr_subject:
    file.write(f'{i},')

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
    win = 3*ind_minutes # 1 min
    center = (lenght)//2

    file.write(f'{lenght / ind_minutes},')
# - - - - - - - - - - - - - - - -
    ECG_stress_1 = ECG_stress[:win]
    ECG_stress_2 = ECG_stress[center-win//2:center+win//2]
    ECG_stress_3 = ECG_stress[lenght-win:]

    ECG_base_1 = ECG_base[:win]
    ECG_base_2 = ECG_base[center - win // 2:center + win // 2]
    ECG_base_3 = ECG_base[lenght - win:]

    signals_ECG_stress, info_ECG_stress = nk.ecg_process(ECG_stress, sampling_rate=700)

    # signals_ECG_stress_1, info_ECG_stress_1 = nk.ecg_process(ECG_base_1, sampling_rate=700)
    # signals_ECG_stress_2, info_ECG_stress_2 = nk.ecg_process(ECG_base_2, sampling_rate=700)
    # signals_ECG_stress_3, info_ECG_stress_3 = nk.ecg_process(ECG_base_3, sampling_rate=700)

    analyze_df_s = nk.ecg_analyze(signals_ECG_stress, sampling_rate=700)

    # analyze_df_s_1 = nk.ecg_analyze(signals_ECG_stress_1, sampling_rate=700)
    # analyze_df_s_2 = nk.ecg_analyze(signals_ECG_stress_2, sampling_rate=700)
    # analyze_df_s_3 = nk.ecg_analyze(signals_ECG_stress_3, sampling_rate=700)

    peaks_s, info_s = nk.ecg_peaks(signals_ECG_stress.ECG_Clean, sampling_rate=700)

    # peaks_s_1, info_s_1 = nk.ecg_peaks(signals_ECG_stress_1.ECG_Clean, sampling_rate=700)
    # peaks_s_2, info_s_2 = nk.ecg_peaks(signals_ECG_stress_2.ECG_Clean, sampling_rate=700)
    # peaks_s_3, info_s_3 = nk.ecg_peaks(signals_ECG_stress_3.ECG_Clean, sampling_rate=700)

    hrv_indices_s = nk.hrv(peaks_s, sampling_rate=700)

    # hrv_indices_s_1 = nk.hrv(peaks_s_1, sampling_rate=700)
    # hrv_indices_s_2 = nk.hrv(peaks_s_2, sampling_rate=700)
    # hrv_indices_s_3 = nk.hrv(peaks_s_3, sampling_rate=700)

    file.write(
        f'{round(float(analyze_df_s["ECG_Rate_Mean"].iloc[0]), 3)},'

        f'{round(float(hrv_indices_s["HRV_MeanNN"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_SDNN"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_SDSD"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_RMSSD"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_pNN50"].iloc[0]), 3)},'

        f'{round(float(hrv_indices_s["HRV_LF"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_HF"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_LFHF"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_VLF"].iloc[0]), 3)},'

        f'{round(float(hrv_indices_s["HRV_SD1"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_SD2"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_DFA_alpha1"].iloc[0]), 3)},'
        f'{round(float(hrv_indices_s["HRV_SampEn"].iloc[0]), 3)}\n')

file.close()
