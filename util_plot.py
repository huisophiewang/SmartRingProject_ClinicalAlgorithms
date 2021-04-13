import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import numpy as np
from util_time import get_task_timing_all, get_task_timing, get_multi_task_time
from util_file import read_acc, read_rr
from util_signal import get_windowed_signal
from util_subjs import subj_mb_lags, subj_relax_task_ids, subj_stress_task_ids
from util_tasks import task_names

task_types = ['relax', 'neutral', 'EMA',
              'mix', 'mental', 'EMA',
              'relax', 'neutral', 'EMA',
              'physical', 'relax', 'neutral', 'EMA',
              'mental', 'mental', 'mental', 'EMA', 'physical']
task_color_map = {'neutral': 'c',  # grey
                  'physical': 'm',  # orange
                  'mental': 'r',  # red
                  'relax': 'g',
                  'mix': 'y',
                  'EMA': '#7f7f7f'}  # grey

def plot_rr(rr_t, rr):
    fig, ax = plt.subplots(1, 1, figsize=(14, 4))
    ax.plot(rr_t, rr, 'b.-', markersize=5, alpha=0.5)
    plt.show()


def plot_rr_acc(rr_t, rr, acc_t, acc):
    fig, ax = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    ax[0].plot(rr_t, rr, 'b.-', markersize=3, alpha=0.5)
    #ax[0].xaxis.set_tick_params(labelbottom=True)

    ax[1].plot(acc_t, acc, 'r.-', markersize=3, alpha=0.5)
    #ax[1].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    #plot_task_by_color(subj, ax[1])
    plt.show()

def plot_acc(acc_t, acc, acc_x, acc_y, acc_z):
    fig, ax = plt.subplots(4, 1, figsize=(20, 10), sharex=True)
    ax[0].set_title('subj:{}\n'.format(subj))
    ax[0].plot(acc_t, acc, 'r.-', markersize=5, alpha=0.5)
    ax[0].xaxis.set_tick_params(labelbottom=True)
    #plot_task_by_color(subj, ax[0])

    ax[1].plot(acc_t, acc_x, '.-', markersize=5, alpha=0.5)
    ax[1].xaxis.set_tick_params(labelbottom=True)

    ax[2].plot(acc_t, acc_y, '.-', markersize=5, alpha=0.5)
    ax[2].xaxis.set_tick_params(labelbottom=True)

    ax[3].plot(acc_t, acc_z, '.-', markersize=5, alpha=0.5)
    ax[3].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    plt.show()

def compare_rr(subj, task_name, rr_t1, rr1, rr_t2, rr2, label1, label2):
    fig, ax = plt.subplots(1, 1, figsize=(14, 3), sharex=True)
    ax.set_title('subj: {}, task: {}\n'.format(subj, task_name))
    ax.plot(rr_t1, rr1, 'b.-', markersize=5, alpha=0.5, label=label1)
    ax.plot(rr_t2, rr2, 'r.-', markersize=5, alpha=0.5, label=label2)
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('RRs [sec]')
    ax.legend()
    plt.show()



def compare_hr(hr_t1, hr1, hr_t2, hr2, hr_t3, hr3):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].plot(hr_t1, hr1, 'b.-', markersize=5, alpha=0.5)
    ax[0].plot(hr_t2, hr2, 'r.-', markersize=5, alpha=0.5)
    ax[1].plot(hr_t1, hr1, 'b.-', markersize=5, alpha=0.5)
    ax[1].plot(hr_t3, hr3, 'g.-', markersize=5, alpha=0.5)
    plt.show()



def compare_acc(acc_t_fb, acc_fb, acc_t_mb, acc_mb):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].set_title('Device: {}\n'.format('firstbeat'))
    ax[0].plot(acc_t_fb, acc_fb, 'r.-', markersize=5, alpha=0.5)
    ax[0].xaxis.set_tick_params(labelbottom=True)
    #plot_task_by_color(subj, ax[0])

    ax[1].set_title('Device: {}\n'.format('msband'))
    ax[1].plot(acc_t_mb, acc_mb, 'r.-', markersize=5, alpha=0.5)
    ax[1].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    #plot_task_by_color(subj, ax[1])
    plt.show()

def compare_rr_acc(subj, task_name, rr_t_fb, rr_fb, rr_t_mb, rr_mb, acc_t_mb, acc_mb):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].set_title('subj: {}, task: {}\n'.format(subj, task_name))
    ax[0].plot(rr_t_fb, rr_fb, 'b.-', markersize=5, alpha=0.5, label='fb')
    ax[0].plot(rr_t_mb, rr_mb, 'r.-', markersize=5, alpha=0.5, label='mb')
    ax[0].set_ylabel('RRs [sec]')
    ax[0].legend()
    ax[1].plot(acc_t_mb, acc_mb, 'g.-', markersize=3, alpha=0.5)
    ax[1].set_ylabel('acc RMS [g]')
    ax[1].set_xlabel('time [sec]')
    plt.show()




def plot_hrvs(hrv1, hrv2):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(hrv1, hrv2, 'o', markersize=5, alpha=0.5)
    plt.show()

def plot_xcorr(corrs, corr_lags):
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.plot(corr_lags, corrs, 'g.')
    plt.show()

def plot_outliers(subj, start_task_id, end_task_id, start_t, rr_t_fb, rr_fb, acc_t_mb, acc_mb, rr_t_mb, rr_mb, i_outliers):
    fig, ax = plt.subplots(3, 1, figsize=(14, 8), sharex=True)
    ax[0].set_title('Subj: {}\n'.format(subj))
    ax[0].plot(acc_t_mb, acc_mb, 'c', label='mb acc')
    ax[0].legend(loc='upper right')

    ax[1].plot(rr_t_mb, rr_mb, 'r.-', markersize=5, alpha=0.5, label='mb')
    ax[1].plot(rr_t_fb, rr_fb, 'b.-', markersize=5, alpha=0.5, label='fb')
    ax[1].legend()

    ax[2].plot(rr_t_mb, rr_mb, 'r.-', markersize=5, alpha=0.5)
    ax[2].plot(rr_t_mb[i_outliers], rr_mb[i_outliers], '*', color='b', alpha=0.5)
    plot_task_by_color(subj, ax[2], start_task_id, end_task_id, start_t)
    plt.show()



def plot_BlandAltman(a, b, percent=False):
    fig, ax = plt.subplots(1, 1, figsize=(14, 6), sharex=True)
    a_b_avg = (a+b)/2
    a_b_diff = a - b

    if not percent:
        diff_mean = np.mean(a_b_diff)
        diff_std = np.std(a_b_diff)
        ax.plot(a_b_avg, a_b_diff, 'o', alpha=0.5)

    else:
        a_b_diff_percent = a_b_diff/a_b_avg
        diff_mean = np.mean(a_b_diff_percent)
        diff_std = np.std(a_b_diff_percent)
        ax.plot(a_b_avg, a_b_diff_percent, 'o', alpha=0.5)

    upper_limit = diff_mean + 1.96 * diff_std
    lower_limit = diff_mean - 1.96 * diff_std
    print('mean diff:')
    print(diff_mean)
    print('95% of differences:')
    print(lower_limit)
    print(upper_limit)
    ax.axhline(y=0.0, alpha=0.5, linestyle='-')
    ax.axhline(y=diff_mean, alpha=0.5, linestyle='--')
    ax.axhline(y=upper_limit, alpha=0.5, linestyle='--', color='r')
    ax.axhline(y=lower_limit, alpha=0.5, linestyle='--', color='r')
    plt.show()


def plot_task_time(subj, start_task_id, end_task_id, start_t, rr_t_mb, rr_mb, rr_t_fb, rr_fb, acc_t_mb, acc_mb):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].set_title('Subj: {}\n'.format(subj))
    ax[0].plot(acc_t_mb, acc_mb, 'c', label='mb acc')
    ax[0].legend(loc='upper right')

    ax[1].plot(rr_t_mb, rr_mb, 'r.-', markersize=5, alpha=0.5)
    ax[1].plot(rr_t_fb, rr_fb, 'b.-', markersize=5, alpha=0.5)
    plot_task_by_color(subj, ax[1], start_task_id, end_task_id, start_t)
    plt.show()

def plot_task_by_color(subj, ax, start_task_id, end_task_id, start_t):
    all_task_time = np.array(get_task_timing_all(subj)) - start_t
    for i in range(start_task_id-1, end_task_id):
        task_type = task_types[i]
        task_color = task_color_map[task_type]
        ax.axvspan(all_task_time[i], all_task_time[i + 1], alpha=0.3, color=task_color, label=task_type)

if __name__ == '__main__':
    subj = 'LWP2_0019'
    lab_rr_t_fb, lab_rr_fb = read_rr(subj, 'firstbeat', 'raw')
    lab_rr_t_mb, lab_rr_mb = read_rr(subj, 'msband', 'raw')
    lab_rr_t_mb = lab_rr_t_mb - subj_mb_lags[subj]
    lab_acc_t_mb, lab_acc_mb = read_acc(subj, 'msband')
    lab_acc_t_mb =  lab_acc_t_mb - subj_mb_lags[subj]


    task_id = subj_relax_task_ids[subj]
    start_t, end_t = get_task_timing(subj, task_id)
    start_t, end_t = get_multi_task_time(subj, 1, 6)
    #print(start_t, end_t)

    print('segment length: {} sec'.format(end_t-start_t))
    rr_t_fb, rr_fb = get_windowed_signal(lab_rr_t_fb, lab_rr_fb, start_t, end_t)
    rr_t_mb, rr_mb = get_windowed_signal(lab_rr_t_mb, lab_rr_mb, start_t, end_t)
    acc_t_mb, acc_mb = get_windowed_signal(lab_acc_t_mb, lab_acc_mb, start_t, end_t)
    rr_t_fb = rr_t_fb - start_t
    rr_t_mb = rr_t_mb - start_t
    acc_t_mb = acc_t_mb - start_t

    plot_task_time(subj, 1, 6, start_t, rr_t_mb, rr_mb, rr_t_fb, rr_fb, acc_t_mb, acc_mb)














