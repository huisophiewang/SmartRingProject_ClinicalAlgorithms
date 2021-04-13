import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util_file import DATA_DIR, read_rr, read_hr, write_5min_hrv, read_5min_hrv
from util_time import get_task_timing
from util_stats import pearson_corr, np_xcorr, Welch_t_test
from util_signal import get_5min_segment, get_windowed_signal, get_hr_from_rr, get_shifted_windows, signal_resample
from util_subjs import all_subjs, all_stress_subjs
from util_subjs import subj_mb_lags, relax_task_ids, IAPS_task_ids, stress_task_ids
from compute_hrv import hrv_param_names, hrv_param_names_units
from compute_hrv import compute_hrv_time_params, compute_hrv_nonlinear_params, compute_hrv_freq_params_from_hr


def compute_5min_hrv_freq_params(subj, task_id, device, rr_type):
    task_rr_t, task_rr = read_rr(subj, device, rr_type, task_id)
    rr_t_5min, rr_5min = get_5min_segment(task_rr_t, task_rr)
    # convert rr to hr
    hr_t_5min, hr_5min = get_hr_from_rr(rr_t_5min, rr_5min, 4.0, 'cubic', 'bpm')
    freq_params = compute_hrv_freq_params_from_hr(hr_t_5min, hr_5min)
    return freq_params

def compute_5min_hrv_time_params(subj, task_id, device, rr_type):
    task_rr_t, task_rr = read_rr(subj, device, rr_type, task_id)
    rr_t_5min, rr_5min = get_5min_segment(task_rr_t, task_rr)
    time_params = compute_hrv_time_params(rr_t_5min, rr_5min)
    return time_params


def compute_all_subj_5min_hrv(subj_list, task_type, subj_task_ids, device, rr_type):
    num_subj = len(subj_list)
    num_param = len(hrv_param_names)
    all_subj_hrv_params = np.zeros((num_subj, num_param))
    for i, subj in enumerate(subj_list):
        print(subj)
        task_id = subj_task_ids[i]
        time_params = compute_5min_hrv_time_params(subj, task_id, 'firstbeat', 'raw')
        all_subj_hrv_params[i, :4] = time_params
        freq_params = compute_5min_hrv_freq_params(subj, task_id, 'firstbeat', 'raw')
        all_subj_hrv_params[i, 4:] = freq_params
    write_5min_hrv(subj_list, task_type, device, rr_type, all_subj_hrv_params, hrv_param_names)


def hrv_t_test(task1_type, task2_type):
    df1 = read_5min_hrv(task1_type, 'firstbeat', 'raw')
    df2 = read_5min_hrv(task2_type, 'firstbeat', 'raw')
    for hrv_param_name in hrv_param_names:
        print('---------------')
        print(hrv_param_name)
        Welch_t_test(df1[hrv_param_name].to_numpy(), df2[hrv_param_name].to_numpy())

if __name__ == '__main__':

    #compute_all_subj_5min_hrv(all_stress_subjs, 'relax', relax_task_ids, 'firstbeat', 'raw')
    #compute_all_subj_5min_hrv(all_stress_subjs, 'stress', stress_task_ids, 'firstbeat', 'raw')
    hrv_t_test('relax', 'stress')






