# ECG Signal Analyzer

## What it does
Loads an ECG recording from the MIT-BIH Arrhythmia Database, filters out noise, detects heartbeats (R-peaks), and calculates heart rate.

## How it works
1. **Filter:** Applies a bandpass filter (0.5–50 Hz) to remove noise and baseline drift
2. **Peak detection:** Finds the tall spikes (R-peaks) in the filtered signal
3. **Heart rate calculation:** Measures time between peaks and converts to beats per minute

## Results
- Successfully detects heartbeats in ECG recordings
- Calculated heart rate: 75.5 bpm
- Plot shows raw vs. filtered signal with detected peaks marked in red

## How to run
```bash
python ecg_analyzer.py
```

## Requirements
- wfdb
- numpy
- scipy
- matplotlib

## Data source
MIT-BIH Arrhythmia Database: https://physionet.org/content/mitdb/1.0.0/