import os
import sys
import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize, suppress=True, precision=12)
from util_time import get_task_timing
from util_tasks import task_names
DATA_DIR = r'C:\Users\huiwa\MATLAB\HeartRateVariability\data\LWP2'

def read_rr(subj, device, rr_type, task_id='all'):
    subj_dir = os.path.join(DATA_DIR, subj)
    if task_id == 'all':
        fp = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'rr', rr_type]) + '.csv')
        df = pd.read_csv(fp)
    else:
        if isinstance(task_id, int):
            fp = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'rr', rr_type, 'task' + str(task_id)]) + '.csv')
        else:
            fp = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'rr', rr_type, 'task' + task_id]) + '.csv')
        df = pd.read_csv(fp)
    rr_t = df['unix_timestamp'].to_numpy()
    rr = df['rr'].to_numpy()
    return rr_t, rr


def read_hr(subj, device, hr_type, task_id):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'hr', 'task' + str(task_id), hr_type]) + '.csv')
    df = pd.read_csv(fp)
    hr_t = df['unix_timestamp'].to_numpy()
    hr = df['hr'].to_numpy()
    return hr_t, hr

def read_acc(subj, device, task_id='all'):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'acc_raw']) + '.csv')
    df = pd.read_csv(fp)
    if task_id == 'all':
        df_task = df
    else:
        start_t, end_t = get_task_timing(subj, task_id)
        df_task = df.loc[df['unix_timestamp'].between(start_t, end_t+1, inclusive=True)]
    acc_t = df_task['unix_timestamp'].to_numpy()
    acc = df_task['rms_acc'].to_numpy()
    return acc_t, acc

def read_5min_hrv(task_type, device, rr_type,):
    fn_in = '_'.join(['lab', task_type, device, rr_type, '5min_hrv']) + '.csv'
    fp_in = os.path.join(DATA_DIR, 'all_subjs', fn_in)
    df = pd.read_csv(fp_in)
    return df

def write_rr_to_csv(rr_t, rr, subj, device, rr_type, task_id):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp_out = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'rr', rr_type, 'task'+str(task_id)]) + '.csv')
    df = pd.DataFrame(columns=['unix_timestamp', 'rr'])
    df['unix_timestamp'] = rr_t
    df['rr'] = rr
    df.to_csv(fp_out, index=False, float_format='%.6f')

def write_hr_to_csv(hr_t, hr, subj, device, hr_type, task_id):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp_out = os.path.join(subj_dir, '_'.join([subj, 'lab', device, 'hr', 'task' + str(task_id), hr_type]) + '.csv')
    df = pd.DataFrame(columns=['unix_timestamp', 'hr'])
    df['unix_timestamp'] = hr_t
    df['hr'] = hr
    df.to_csv(fp_out, index=False, float_format='%.6f')

def write_signal_by_task(subj, device, signal_name, task_id, signal_t, signal):
    df = pd.DataFrame(columns=['unix_timestamp', signal_name])
    df['unix_timestamp'] = signal_t
    df[signal_name] = signal
    fp_task = os.path.join(DATA_DIR, subj, '_'.join([subj, 'lab', device, signal_name, 'task'+str(task_id)]) + '.csv')
    df.to_csv(fp_task, index=False, float_format='%.6f')

def write_5min_hrv(subjs, task_type, device, rr_type, hrvs, hrv_param_names):
    fn_out = '_'.join(['lab', task_type, device, rr_type, '5min_hrv']) + '.csv'
    fp_out = os.path.join(DATA_DIR, 'all_subjs', fn_out)
    df1 = pd.DataFrame(data=subjs, columns=['subj_id'])
    df2 = pd.DataFrame(data=hrvs, columns=hrv_param_names)
    df = pd.concat([df1, df2], axis=1)
    #print(df)
    df.to_csv(fp_out, index=False, float_format='%.6f')
    #np.savetxt(fp_out, hrvs, delimiter=',', fmt='%.3f', header=','.join(['subj_id']+hrv_param_names), comments='')

