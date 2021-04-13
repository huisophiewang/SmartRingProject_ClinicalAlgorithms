import os
import pandas as pd
import numpy as np
from util_time import get_task_timing, get_lab_start_end_time
from util_file import DATA_DIR
e4_signal_name_map = {'ppg': 'BVP', 'rr': 'IBI', 'acc': 'ACC'}

def read_e4_signal(subj, signal_name, task_id='all'):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', 'e4', signal_name, 'raw']) + '.csv')
    df = pd.read_csv(fp)

    if task_id == 'all':
        df_task = df
    else:
        start_t, end_t = get_task_timing(subj, task_id)
        df_task = df.loc[df['unix_timestamp'].between(start_t, end_t + 1, inclusive=True)]

    t = df_task['unix_timestamp'].to_numpy()
    signal = df_task[signal_name].to_numpy()
    return t, signal

def read_e4_acc(subj, task_id='all'):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', 'e4', 'acc', 'raw']) + '.csv')
    df = pd.read_csv(fp)
    if task_id == 'all':
        df_task = df
    else:
        start_t, end_t = get_task_timing(subj, task_id)
        df_task = df.loc[df['unix_timestamp'].between(start_t, end_t + 1, inclusive=True)]
    t = df_task['unix_timestamp'].to_numpy()
    x = df_task['x'].to_numpy()
    y = df_task['y'].to_numpy()
    z = df_task['z'].to_numpy()
    # acc sampling freq 32 Hz,
    # range 2g, max value 128
    # 1 g value = 64
    rms = (np.sqrt(np.square(x) + np.square(y) + np.square(z)))/64.0
    # remove gravity
    rms = rms - 1.0
    rms = np.abs(rms)
    return t, rms, x, y, z

def write_e4_ppg_to_csv(subj):
    subj_dir = os.path.join(DATA_DIR, subj)
    signal_name = 'ppg'
    e4_signal_name = e4_signal_name_map[signal_name]
    fp_in = os.path.join(subj_dir, 'E4_raw', 'lab', 'left', e4_signal_name + '.csv')
    fp_out = os.path.join(subj_dir, '_'.join([subj, 'all', 'e4', signal_name, 'raw'])+ '.csv')
    df = pd.read_csv(fp_in, header=None)
    start_t = df.iloc[0][0]
    freq = df.iloc[1][0]
    signal = df.loc[2:].to_numpy()
    ts = np.arange(len(signal))
    ts = ts * 1.0/freq
    ts = ts + start_t
    m = np.concatenate((ts.reshape(-1,1), signal.reshape(-1,1)), axis=1)
    col_names = 'unix_timestamp,'+signal_name
    np.savetxt(fp_out, m, delimiter=',', fmt='%.6f,%.6f', header=col_names, comments='')

def write_e4_acc_to_csv(subj):
    subj_dir = os.path.join(DATA_DIR, subj)
    signal_name = 'acc'
    e4_signal_name = e4_signal_name_map[signal_name]
    fp_in = os.path.join(subj_dir, 'E4_raw', 'lab', 'left', e4_signal_name + '.csv')
    fp_out = os.path.join(subj_dir, '_'.join([subj, 'all', 'e4', signal_name, 'raw']) + '.csv')
    df = pd.read_csv(fp_in, header=None)
    start_t = df.iloc[0][0]
    freq = df.iloc[1][0]
    signal = df.loc[2:].to_numpy()
    ts = np.arange(len(signal))
    ts = ts * 1.0 / freq
    ts = ts + start_t
    m = np.concatenate((ts.reshape(-1, 1), signal), axis=1)
    col_names = 'unix_timestamp,' + 'x,y,z'
    np.savetxt(fp_out, m, delimiter=',', fmt='%.6f,%.0f,%.0f,%.0f', header=col_names, comments='')

def write_e4_ibi_to_csv(subj):
    subj_dir = os.path.join(DATA_DIR, subj)
    signal_name = 'rr'
    e4_signal_name = e4_signal_name_map[signal_name]
    fp_in = os.path.join(subj_dir, 'E4_raw', 'lab', 'left', e4_signal_name + '.csv')
    fp_out = os.path.join(subj_dir, '_'.join([subj, 'all', 'e4', signal_name, 'raw']) + '.csv')
    df = pd.read_csv(fp_in, header=None)
    # removed string 'IBI' in cell[0][1] in original csv file, because it makes column 1 interpreted as string
    start_t = df.iloc[0][0]
    rr_t = df.loc[1:][0].to_numpy()
    rr = df.loc[1:][1].to_numpy()
    rr = rr.astype(float)
    rr_t = rr_t + start_t
    m = np.concatenate((rr_t.reshape(-1, 1), rr.reshape(-1, 1)), axis=1)
    col_names = 'unix_timestamp,'+signal_name
    np.savetxt(fp_out, m, delimiter=',', fmt='%.6f,%.6f', header=col_names, comments='')


def cut_e4_raw_lab_session(subj, signal_name):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp_in = os.path.join(subj_dir, '_'.join([subj, 'all', 'e4', signal_name, 'raw']) + '.csv')
    fp_out = os.path.join(subj_dir, '_'.join([subj, 'lab', 'e4', signal_name, 'raw']) + '.csv')
    df = pd.read_csv(fp_in)
    lab_start_t, lab_end_t = get_lab_start_end_time(subj)
    df_lab = df.loc[df['unix_timestamp'].between(lab_start_t, lab_end_t + 1, inclusive=True)]
    df_lab.to_csv(fp_out, index=False, float_format='%.6f')


if __name__ == '__main__':
    subj = 'LWP2_0005'
    # lab_start_t, lab_end_t = get_lab_start_end_time(subj)
    # print(lab_start_t, lab_end_t)

    # task_id = 14
    # task_ppg_t, task_ppg = read_e4_signal(subj, 'ppg', task_id)
    # write_signal_by_task(subj, 'e4', 'ppg', task_id, task_ppg_t, task_ppg)
    # task_acc_t, task_acc_rms, _, _, _ = read_e4_acc(subj, task_id)
    # write_signal_by_task(subj, 'e4', 'acc_rms', task_id, task_acc_t, task_acc_rms)

    # write_e4_ppg_to_csv(subj)
    # cut_e4_raw_lab_session(subj, 'ppg')

    write_e4_ibi_to_csv(subj)
    cut_e4_raw_lab_session(subj, 'rr')

    # write_e4_acc_to_csv(subj)
    # cut_e4_raw_lab_session(subj, 'acc')
