# Research of the Dependences of Heart Rate Variability Data on Cognitive Loads in Public Datasets

This repository contains code that was used as a tool for the implementation of research conducted at the Department of MOEVM, St. Petersburg Electrotechnical University "LETI", 2024.

The work examined ECG signals in synchronization with the psycho-emotional state, taken from subjects of the **WESAD** and **CASE** datasets.

---

The code is a Python 3.9 console application for processing biomedical data.

Before starting, you need to install the following packages: neurokit2, numpy, matplotlib. Also, for working with WESAD, the pickle module is required.

To install all necessary dependencies, use the command:

```
pip install -r requirements.txt
```

In addition, the contents of datasets must be included in the program directory. 
To correctly extract signals, you should use datasets structure in which they are presented [WESAD](https://ubicomp.eti.uni-siegen.de/home/datasets/icmi18/), [CASE](https://springernature.figshare.com/articles/dataset/CASE_Dataset-full/8869157).

---

This repository contains 3 main directories:

1. WESAD -- extracting HRV values ​​for subjects of the WESAD dataset.
2. CASE -- extracting HRV values ​​for subjects of the CASE dataset.
3. reduce -- a directory containing primary versions of the code. (Packages tests, data processing when changing the sampling frequency, basic interactions with the dataset).

The WESAD and CASE catalogs present both the code for processing and the values ​​​​obtained from the corresponding signal intervals.

The subdirectories contain values ​​for the neutral and stress states of subjects in a particular dataset.

The file names contain information regarding the datasets, the psycho-emotional state, 
the size and position of the window (the position is determined by the numbers $'1', '2', '3'$, which corresponds to the beginning, center and end of the full interval).

Files that contain $'shift..X-Y'$ in the name represent an iterative calculation 
(one iteration is a signal window of size $Y$, each subsequent iteration begins with a shift back $X$, which means the itertion starts from $(Y-X)$ seconds of the previous window, thus considering intervals with overlapping time).

The files represent both listed values ​​with the designation of the metrics under consideration and series of values ​​for calculation without designation 
(for the second case: files with code that have $'TABLE'$ at the end of the name, files with values that ​​have $'T'$ at the end of the name, 
the table data has the following structure: rows -- values ​​by subject, columns -- *'Subject'*, *'ECG_Rate_Mean'*, *'MeanNN'*, *'SDNN'*, *'SDSD'*, *'RMSSD'*, *'pNN50'*, *'LF'*, *'HF'*, *'LF/HF'*, *'VLF'*, *'SD1'*, *'SD2'*).

---

#### Publications on the topic of work:
- Article “Comparison of Approaches to the Selection of Datasets for HRV Research under Cognitive Loads” in the collection of reports of students and graduate students at the scientific and technical seminar of the Department of MOEVM. St. Petersburg, February 1 – 2, 2024.
- Article “Research of the Dependences of Heart Rate Variability Data on Cognitive Loads in Public Datasets” in the collection of materials of the XII scientific and practical conference “Science of the present and future”. St. Petersburg, May 16 – 17(18), 2024.
