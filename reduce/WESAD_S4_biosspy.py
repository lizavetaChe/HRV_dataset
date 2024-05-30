import pickle
import matplotlib.pyplot as plt
import numpy as np
from biosppy.signals import ecg
import pandas as pd

sampling_rate = 700
with open('S4.pkl', 'rb') as f:
    data = pickle.load(f, encoding="bytes")

signal = (data[b'signal'][b'chest'][b'ECG'])[:10000]
res = []
res = list((np.array(signal)).reshape(10000,))
#print(res)

out = ecg.ecg(signal=res, sampling_rate=700, show=False)
d = out.as_dict()
print(d['rpeaks'])