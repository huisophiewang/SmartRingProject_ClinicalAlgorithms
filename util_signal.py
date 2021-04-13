import math
import numpy as np
import pandas as pd
from scipy import signal
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def get_hr_from_rr(rr_t, rr, fs, interp_method, unit):
    rr_t_resampled, rr_resampled = signal_resample(rr_t, rr, fs, interp_method)
    #print(rr_t_resampled)
    hr_t = rr_t_resampled
    if unit == 'bps':
        hr = 1/rr_resampled
    if unit == 'bpm':
        hr = 60 / rr_resampled
    #print(len(hr))
    return hr_t, hr



# rr upsample to 4 Hz, interpolation using cubic spline
# interpolation method: 'cubic', 'linear'
def signal_resample(x_t, x, f, interp_method):
    fun = interp1d(x_t, x, kind=interp_method)
    x_t_new = np.arange(x_t[0], x_t[-1], 1/f)
    x_new = fun(x_t_new)
    return x_t_new, x_new

def get_shifted_windows(start_t, end_t, win_size_sec, win_shift_sec):
    total_time = end_t - start_t
    #print(total_time)
    if total_time < win_size_sec:
        num_win = 0
    else:
        num_win = math.ceil((total_time - win_size_sec) / win_shift_sec) + 1
    #print(num_win)
    windows = np.zeros((num_win, 2))
    for i in range(num_win):
        # starting from the first window
        win_start = start_t + i * win_shift_sec
        win_end = win_start + win_size_sec
        # the last window may not be full size
        if i == num_win-1:
            windows[i, 0] = win_start
            windows[i, 1] = np.ceil(end_t)
        else:
            windows[i, 0] = win_start
            windows[i, 1] = win_end
    #pprint(windows)
    return windows

def get_windowed_signal(t, x, start_t, end_t):
    win_idx = np.where((start_t <= t) & (t <= end_t))
    #print(win_idx)
    win_t = t[win_idx]
    win_x = x[win_idx]
    return win_t, win_x

def get_5min_segment(t, x):
    duration = t[-1] - t[0]
    start_t = t[0] + (duration - 300)/2
    end_t = start_t + 300
    win_t, win_x = get_windowed_signal(t, x, start_t, end_t)
    return win_t, win_x


# example: [1, 3, 2, 7, 6], win_size=3, return [2, 2, 4, 5, 5]
# an odd number should be used for win_size
def moving_avg(data, win_size):
    wins = pd.Series(data).rolling(win_size, center=True)
    # the number of missed vals at the beginning and end
    miss_num = int((win_size - 1) / 2)
    avgs = wins.mean().tolist()[miss_num:-miss_num]
    # makes the avgs have the same size as original data
    avgs = [avgs[0]]*miss_num + avgs + [avgs[-1]]*miss_num
    print(avgs)
    return avgs




# periodogram is a way of estimating PSD (power spectral density)
# periodogram is equal to the smoothed sample PSD
def psd_by_periodgram(t, x):
    fs = 1 / (t[1] - t[0])
    freq, psd = signal.periodogram(x, fs)
    return freq, psd


# use windows can generate multiple samples (each window is a sample), so the result is more accurate
# The longer the window, the higher resolution in freq domain,
# the shorter the window, the more samples, but has lower resolution in freq domain
# window length is a balance between these two considerations
def psd_by_welch(x, fs):
    #nperseg = 256 by default
    freq, psd = signal.welch(x, fs=fs, nperseg=256)
    return freq, psd

# smooth and detrend
# original RR signal resampled to 4 Hz
# use Welch method to compute PSD
def rr_psd_by_welch(t, rr, moving_win=1):
    # smooth and detrend
    # rr_smooth = moving_avg(rr, moving_win)
    # rr_detrend = rr_smooth - np.mean(rr_smooth)
    fs = 4.0
    t_new, rr_new = signal_resample(t, rr, fs, 'cubic')
    freq, psd = signal.welch(rr_new, fs)

    # print(freq)
    # print(psd)
    # max_idx = np.argmax(psd)
    # print(freq[max_idx])
    return freq, psd

# smooth and detrend
# Lombscargle can be used on unevenly sampled signal, no need to resample
def rr_psd_by_ls(t, rr, moving_win_size=1):
    # smooth and detrend
    # rr_smooth = moving_avg(rr, moving_win_size)
    # rr_detrend = rr_smooth - np.mean(rr_smooth)

    freq = np.linspace(0.001, 1.0, 1000)
    psd = signal.lombscargle(t, rr, freq, normalize=True)

    return freq, psd

# LF 0.04 Hz - 0.15 Hz
# HF 0.14 Hz - 0.4 Hz
# ratio LF/HF
def compute_band_powers(freq, psd):
    very_low_indices = np.argwhere((freq > 0.0033) & (freq < 0.04))
    very_low_power = np.sum(psd[very_low_indices])
    #print(very_low_power)

    low_indices = np.argwhere((freq > 0.04) & (freq < 0.15))
    low_freq_power = np.sum(psd[low_indices])
    #print(low_freq_power)

    high_indices = np.argwhere((freq > 0.15) & (freq < 0.4))
    high_freq_power = np.sum(psd[high_indices])
    #print(high_freq_power)
    #print((very_low_power+ low_freq_power + high_freq_power))

    low_power_nu = low_freq_power/(low_freq_power+high_freq_power)
    high_power_nu = high_freq_power/(low_freq_power+high_freq_power)

    threshold_indices = np.argwhere((freq > 0) & (freq < 2))
    total_threshold_power = np.sum(psd[threshold_indices])
    # print(total_threshold_power)
    # total_power = np.sum(psd)
    #print(high_freq_power/(low_freq_power + high_freq_power))
    #high_ratio = high_freq_power/(very_low_power + low_freq_power + high_freq_power)
    high_ratio = high_freq_power/total_threshold_power

    low_high_ratio = low_freq_power/high_freq_power

    #return very_low_power, low_freq_power, high_freq_power, high_ratio
    return low_freq_power, high_freq_power, low_power_nu, high_power_nu, low_high_ratio

# maintain original length
def signal_time_shift(x, shift):
    if shift == 0:
        return x
    if shift > 0:
        # right shift
        padding = shift * [np.nan]
        res = np.hstack((padding, x[:-shift]))
        return res
    else:
        # left shift
        padding = -shift * [np.nan]
        res = np.hstack((x[-shift:], padding))
        return res

def get_rr_from_peaks(ppg_t, peak_idxs):
    rr_t = ppg_t[peak_idxs]
    rr = np.diff(rr_t)
    #print(rr)
    #return rr_t[:-1], rr
    return rr_t[1:], rr

def get_first_order_derivative(x, fs):
    # dx[n] = x[n+1]-x[n-1]/2*dt
    dt = 1/fs
    dx = np.diff(x)
    dx_dt = dx/dt
    #print(dx_dt[:100])
    #print(dx)
    return dx_dt


def plot_rr_psd(rr_t, rr):
    freq, psd = rr_psd_by_welch(rr_t, rr)
    moving_win_size = 1
    plot_signal_power(rr_t, rr, freq, psd, 'rr')

def plot_hr_psd(hr_t, hr):
    freq, psd = signal.welch(hr, 4.0)
    plot_signal_power(hr_t, hr, freq, psd, 'hr')

def plot_signal_power(t, x, freq, psd, signal_name):
    # plot signal
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 6))
    fig.subplots_adjust(hspace=0.3)
    ax1.plot(t, x, 'bo-', markersize=2, alpha=0.5)
    ax1.set_xlabel('time [sec]')
    ax1.set_ylabel(signal_name)

    # plot psd
    ax2.plot(freq, psd)
    ax2.set_xlim(0, 1)
    ax2.set_xticks(np.arange(0, 1, 0.05))
    ax2.set_xlabel('frequency [Hz]')
    ax2.set_ylabel('psd')
    plt.show()


if __name__ == '__main__':
    arr = [1, 3, 2, 7, 6]
    #moving_avg(arr, 3)
    signal = signal_time_shift(arr, -3)
    print(signal)