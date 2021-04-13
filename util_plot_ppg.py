import matplotlib.pyplot as plt

def plot_ppg(ppg_t, ppg, win_id=0, win_size=0):
    fig, ax = plt.subplots(1, 1, figsize=(14, 3), sharex=True)
    ax.set_title('win_size:{}, win_id:{}\n'.format(win_id, win_size))
    ax.plot(ppg_t, ppg, 'b', markersize=3, alpha=0.5, label='ppg raw')
    ax.legend(loc='upper right')
    plt.show()

def plot_ppg_with_peaks(ppg_t, ppg, peak_idxs):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].plot(ppg_t, ppg)
    ax[1].plot(ppg_t, ppg, 'b.-', markersize=3, alpha=0.5)
    ax[1].plot(ppg_t[peak_idxs], ppg[peak_idxs], 'r.', markersize=3)
    plt.show()

def plot_ppg_with_peaks_and_valleys(ppg_t, ppg, peak_idxs, valley_idxs):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].plot(ppg_t, ppg)
    ax[1].plot(ppg_t, ppg, 'b.-', markersize=3, alpha=0.5)
    ax[1].plot(ppg_t[peak_idxs], ppg[peak_idxs], 'ro', markersize=5, alpha=0.5)
    ax[1].plot(ppg_t[valley_idxs], ppg[valley_idxs], 'go', markersize=5, alpha=0.5)
    plt.show()

# PPG signal sampling frequency 64 Hz, dt = 1/64 = 0.015625
def plot_ppg_derivative(ppg_t, ppg, ppg_derivative_t, ppg_derivative):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].plot(ppg_t, ppg, 'b.-', markersize=3, alpha=0.5)
    ax[1].plot(ppg_derivative_t, ppg_derivative, 'b.-', markersize=3, alpha=0.5)
    ax[1].axhline(y=0.0, color='r', alpha=0.5)
    plt.show()

def plot_ppg_and_acc(ppg_t, ppg, acc_t, acc, win_id, win_size):
    fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    ax[0].set_title('win_size:{}, win_id:{}\n'.format(win_id, win_size))
    ax[0].plot(acc_t, acc, 'r', markersize=3, alpha=0.8, label='acc raw')
    ax[0].legend(loc='upper right')
    ax[1].plot(ppg_t, ppg, 'b', markersize=3, alpha=0.8, label='ppg raw')
    ax[1].legend(loc='upper right')
    plt.show()

def plot_ppg_and_rr(subj, task_id, win_id, ppg_t, ppg, peak_idxs, rr_t, rr, acc_t, acc, rr_t_e4, rr_e4, rr_t_fb, rr_fb):
    fig, ax = plt.subplots(3, 1, figsize=(14, 8), sharex=True)
    ax[0].set_title('subj:{}, task:{}, segment_id:{}\n'.format(subj, task_id, win_id))
    ax[0].plot(acc_t, acc, 'c', label='e4 acc')
    ax[0].legend(loc='upper right')
    ax[1].plot(ppg_t, ppg, 'b.-', markersize=3, alpha=0.5, label='e4 ppg')
    ax[1].plot(ppg_t[peak_idxs], ppg[peak_idxs], 'ro', markersize=5, alpha=0.5)
    ax[1].legend(loc='upper right')
    ax[2].plot(rr_t, rr, 'r.-', markersize=7, alpha=0.5, label='my rr')
    ax[2].plot(rr_t_e4, rr_e4, 'g.-', markersize=7, alpha=0.5, label='e4 rr')
    #ax[2].plot(rr_t_fb, rr_fb, 'g.-', markersize=7, alpha=0.5, label='fb rr')
    ax[2].legend(loc='upper right')
    plt.show()

def compare_ppg(ppg_t1, ppg1, ppg_t2, ppg2):
    fig, ax = plt.subplots(1, 1, figsize=(14, 3), sharex=True)
    ax.plot(ppg_t1, ppg1, 'b.-', markersize=3, alpha=0.5, label='ppg raw')
    ax.plot(ppg_t2, ppg2, 'r.-', markersize=3, alpha=0.5, label='ppg filtered')
    ax.legend(loc='upper right')
    plt.show()

