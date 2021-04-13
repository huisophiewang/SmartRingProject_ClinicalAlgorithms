
all_subjs = ['LWP2_0019', 'LWP2_0017', 'LWP2_0015', 'LWP2_0013', 'LWP2_0011', 'LWP2_0009','LWP2_0007', 'LWP2_0005', 'LWP2_0003']
all_hrv_subjs = ['LWP2_0019', 'LWP2_0017', 'LWP2_0013', 'LWP2_0011', 'LWP2_0009','LWP2_0007', 'LWP2_0005', 'LWP2_0003']

# subj 0013 doesn't have FB data of stress tasks, also didn't feel stressed.
all_stress_subjs = ['LWP2_0019', 'LWP2_0017', 'LWP2_0015', 'LWP2_0011', 'LWP2_0009','LWP2_0007', 'LWP2_0005', 'LWP2_0003']
mb_lags_in_sample = [16, 16, 11, 18, 18, 9, 7, 18, 16]
mb_lags_in_sec = [lag * 0.25 for lag in mb_lags_in_sample]
subj_mb_lags = dict(zip(all_subjs, mb_lags_in_sec))
#print(subj_mb_lags)
relax_task_ids = [1, 1, 1, 1, 1, 1, 7, 7, 7]
stress_task_ids = ['14to15'] * 9
cycling_task_ids = [10] * 9
IAPS_task_ids = [4] * 9
subj_relax_task_ids = dict(zip(all_subjs, relax_task_ids))
subj_stress_task_ids = dict(zip(all_subjs, stress_task_ids))
subj_cycling_task_ids = dict(zip(all_subjs, cycling_task_ids))

