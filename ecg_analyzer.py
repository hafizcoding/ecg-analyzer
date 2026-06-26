import wfdb
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

# ============================================
# 1. LOAD THE DATA (WFDB FORMAT)
# ============================================
print("Loading ECG data...")

# Read the WFDB file (point to the filename without extension)
record = wfdb.rdrecord('100')
ecg_signal = record.p_signal[:, 0]  # Get first channel

print(f"Loaded {len(ecg_signal)} samples")
print(f"Sampling frequency: {record.fs} Hz")
print(f"First 10 values: {ecg_signal[:10]}")

# ============================================
# 2. FILTER THE SIGNAL
# ============================================
print("\nFiltering signal...")

fs = record.fs  # Sampling frequency from the file (usually 360 Hz)
nyquist = fs / 2

lowcut = 0.5
highcut = 50.0
low = lowcut / nyquist
high = highcut / nyquist

b, a = butter(4, [low, high], btype='band')
filtered_signal = filtfilt(b, a, ecg_signal)

print("Filtering complete")

# ============================================
# 3. FIND R-PEAKS (HEARTBEATS)
# ============================================
print("\nDetecting R-peaks...")

peaks, properties = find_peaks(filtered_signal, height=0.5, distance=100)

print(f"Found {len(peaks)} heartbeats")

# ============================================
# 4. CALCULATE HEART RATE
# ============================================
print("\nCalculating heart rate...")

if len(peaks) > 1:
    peak_intervals = np.diff(peaks) / fs
    avg_interval = np.mean(peak_intervals)
    heart_rate = 60 / avg_interval
    
    print(f"Average interval between beats: {avg_interval:.2f} seconds")
    print(f"Heart rate: {heart_rate:.1f} bpm")
else:
    print("ERROR: Not enough peaks found.")
    heart_rate = None

# ============================================
# 5. PLOT THE RESULTS
# ============================================
print("\nPlotting...")

fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Plot 1: Raw signal (first 10 seconds)
axes[0].plot(ecg_signal[:3600], label='Raw ECG', color='blue', linewidth=0.5)
axes[0].set_title('Raw ECG Signal (First 10 seconds)')
axes[0].set_xlabel('Sample')
axes[0].set_ylabel('Voltage (mV)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Filtered signal with peaks
axes[1].plot(filtered_signal[:3600], label='Filtered ECG', color='green', linewidth=0.8)
peaks_in_range = peaks[peaks < 3600]
axes[1].plot(peaks_in_range, filtered_signal[peaks_in_range], 'ro', markersize=8, label='R-peaks')
axes[1].set_title(f'Filtered ECG with R-peak Detection (HR: {heart_rate:.1f} bpm)')
axes[1].set_xlabel('Sample')
axes[1].set_ylabel('Voltage (mV)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ecg_analysis.png', dpi=150)
print("Plot saved as 'ecg_analysis.png'")

plt.show()

# ============================================
# 6. SUMMARY
# ============================================
print("\n" + "="*50)
print("ECG ANALYSIS COMPLETE")
print("="*50)
if heart_rate:
    print(f"Heart Rate: {heart_rate:.1f} bpm")
    print(f"Total Heartbeats Detected: {len(peaks)}")
    print(f"Recording Duration: {len(ecg_signal) / fs:.1f} seconds ({len(ecg_signal) / fs / 60:.1f} minutes)")
print("="*50)