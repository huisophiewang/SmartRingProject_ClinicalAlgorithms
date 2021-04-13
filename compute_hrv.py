import sys
import os
import numpy as np
np.set_printoptions(threshold=sys.maxsize, suppress=True, precision=12)
import pyhrv
from scipy import signal, fft
import matplotlib.pyplot as plt
from util_signal import signal_resample, get_5min_segment, get_hr_from_rr
from util_file import read_rr
from util_time import get_task_timing
from util_signal import rr_psd_by_welch, compute_band_powers, get_shifted_windows, get_windowed_signal, psd_by_welch

DATA_DIR = r'C:\Users\huiwa\MATLAB\HeartRateVariability\data\LWP2'
hrv_time_param_names = ['mean_nn', 'SDNN', 'RMSSD', 'pNN50']
hrv_freq_param_names = ['LF', 'HF', 'lf_nu', 'hf_nu', 'LF\HF']
hrv_nonlinear_param_names = ['SD1', 'SD2', 'SD1\SD2']
hrv_param_names = hrv_time_param_names + hrv_freq_param_names
hrv_param_units = ['ms', 'ms', 'ms', 'ratio', 'bpm^2', 'bpm^2', 'ratio', 'ratio', 'ratio']
hrv_param_names_units = dict(zip(hrv_param_names, hrv_param_units))



# compute HRV time domain parameters from rr
# mean_nn, sdnn, rmssd, pnn50
# units: ms, ms, ms, ratio
def compute_hrv_time_params(rr_t, rr):
    rr = rr*1000
    mnn = np.mean(rr)
    sdnn = np.std(rr)
    rmssd = np.sqrt(np.sum(np.square(np.diff(rr))))
    pnn50 = len(np.argwhere(np.abs(np.diff(rr)) > 50)) / len(rr)
    time_params = [mnn, sdnn, rmssd, pnn50]
    print(time_params)
    return time_params

# compute HRV frequency domain parameters from rr
# 'LF', 'HF', 'lf_nu', 'hf_nu', 'LF\HF'
# units: bpm^2, bpm^2, bpm^2, ratio, ratio
def compute_hrv_freq_params_from_rr(rr_t, rr):
    resample_freq = 4.0
    t_new, rr_new = signal_resample(rr_t, rr, resample_freq, 'cubic')
    freq, psd = signal.welch(rr_new, fs=resample_freq, nperseg=256)
    #plot_signal_psd(t_new, rr_new, freq, psd)
    low, high, h_ratio = compute_band_powers(freq, psd)
    freq_params = [low, high, h_ratio]
    print(freq_params)
    return freq_params

# compute HRV frequency domain parameters from hr
def compute_hrv_freq_params_from_hr(hr_t, hr):
    hr_freq = 4.0
    freq, psd = signal.welch(hr, fs=hr_freq, nperseg=256)
    #plot_signal_psd(hr_t, hr, freq, psd)
    low, high, low_nu, high_nu, lh_ratio = compute_band_powers(freq, psd)
    compute_band_powers(freq, psd)
    freq_params = [low, high, low_nu, high_nu, lh_ratio]
    print(freq_params)
    return freq_params


# compute HRV nonlinear parameters from rr
def compute_hrv_nonlinear_params(rr_t, rr):
    _, sd1, sd2, sd21_ratio, area = pyhrv.nonlinear.poincare(rr, rr_t, False)
    #plt.show()
    sd12_ratio = 1/sd21_ratio
    nonlinear_params = [sd1, sd2, sd12_ratio]
    print(nonlinear_params)
    return nonlinear_params



def plot_signal_psd(t, x, freq, psd):
    # plot signal
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 6))
    fig.subplots_adjust(hspace=0.3)
    ax1.plot(t, x, 'b.-', markersize=5, alpha=0.5)
    ax1.set_xlabel('time [sec]')

    # plot psd
    ax2.plot(freq, psd, 'b.-', markersize=5, alpha=0.5)
    #ax2.set_xlim(0, 1)
    #ax2.set_xticks(np.arange(0, 1, 0.05))
    ax2.set_xlabel('frequency [Hz]')
    ax2.set_ylabel('psd')
    plt.show()

if __name__ == '__main__':
    subj = 'LWP2_0019'
    relax_task_id = 1
    lab_rr_t_fb, lab_rr_fb = read_rr(subj, 'firstbeat', 'raw')
    start_t, end_t = get_task_timing(subj, relax_task_id)
    rr_t_fb, rr_fb = get_windowed_signal(lab_rr_t_fb, lab_rr_fb, start_t, end_t)
    rr_t_fb_5min, rr_fb_5min = get_5min_segment(rr_t_fb, rr_fb)
    hr_t_fb_5min, hr_fb_5min = get_hr_from_rr(rr_t_fb_5min, rr_fb_5min, 'cubic')

    compute_hrv_freq_params_from_hr(hr_t_fb_5min, hr_fb_5min)
