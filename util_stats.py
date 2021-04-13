import sys
import os
import numpy as np
np.set_printoptions(threshold=sys.maxsize, suppress=True, precision=12)
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

def pearson_corr(x, y):
    r, p = stats.pearsonr(x, y)
    print(r, p)
    return r

def np_xcorr(x, y, maxlags=20):
    # x, y have the same length
    N = len(x)
    # result is the same as scipy.signal.correlate
    corrs = np.correlate((x - np.mean(x)), (y - np.mean(y)), mode='full') / (np.std(x) * np.std(y) * N)
    center = (len(corrs) - 1)/2
    left = int(center-maxlags)
    right = int(center+maxlags)
    corrs = corrs[left:right+1]
    corr_lags = np.arange(maxlags, -maxlags-1, -1)
    idx = np.argmax(corrs)
    max_corr = corrs[idx]
    max_corr_lag = corr_lags[idx]
    print(corrs)
    print(corr_lags)
    print(max_corr)
    print(max_corr_lag)
    return corrs, corr_lags

# this implementation has the same result as np_xcorr,
# only allows the same length of x and y
def my_xcorr(x, y, maxlags):
    # x, y have the same length
    N = len(x)

    # should mean be subtracted here?
    # if subtracting mean, the results are the same as np.correlate() in np_xcorr
    # the definition of covariance includes subtracting mean
    # subtracting mean before padding
    x = x - np.mean(x)
    y = y - np.mean(y)

    # corr_lags from -(N-1), to N-1
    maxlags = min((N-1), maxlags)
    corrs = np.zeros(2 * maxlags + 1)
    corr_lags = np.arange(-maxlags, maxlags + 1, 1)

    # when lag = 0
    center_idx = maxlags
    r, p = stats.pearsonr(x, y)
    corrs[center_idx] = r

    # when lag is from 1 to N-1,
    # x shifted to right (zero padded on the left)
    # y doesn't move, but increase length (zero padded on the right)
    for lag in np.arange(1, maxlags+1, 1):
        x_padded = np.hstack((np.zeros(lag), x))
        y_padded = np.hstack((y, np.zeros(lag)))
        # computing pearson correlation involves subtracting mean and divided by std
        #r, p = stats.pearsonr(x_padded, y_padded)
        r = my_corr(x_padded, y_padded)
        corrs[center_idx+lag] = r

    # when lag is from -(N-1) to -1
    # x shifted to left, y doesn't move
    # which is equal to y shifted to right (zero padded on the left)
    # and x doesn't move, but increases length (zero padded on the right)
    for lag in np.arange(1, maxlags+1, 1):
        y_padded = np.hstack((np.zeros(lag), y))
        x_padded = np.hstack((x, np.zeros(lag)))
        #r, p = stats.pearsonr(x_padded, y_padded)
        r = my_corr(x_padded, y_padded)
        corrs[center_idx-lag] = r

    left = int(center_idx - maxlags)
    right = int(center_idx + maxlags)
    #print(corrs)
    #print(corr_lags)

    max_corr = np.max(np.abs(corrs))
    max_idx = np.argmax(np.abs(corrs))
    lag = corr_lags[max_idx]
    # print('max corr:', max_corr)
    # print('lag: ', lag)

    return max_corr, lag
    #return corrs, corr_lags

def my_corr(x, y):
    N = len(x)
    # if divided by (N-1), result is same as np.cov
    cov = np.sum(np.multiply(x, y)) / N
    std_x = np.std(x)
    std_y = np.std(y)
    corr = cov / (std_x * std_y)
    #print(corr)
    return corr

def Welch_t_test(x, y):
    # null hypothesis: the difference between the two means is zero
    # alternative hypothesis: the difference between the two means is not zero
    # if p-value is smaller than alpha, reject null hypothesis, which means alternative hypothesis is likely to be true
    t_stat, p = stats.ttest_ind(x, y, equal_var=False) # If False, perform Welch’s t-test, which does not assume equal population variance
    print(t_stat, p)

# between two signals that don't have the same length
def corr_and_mae(x1, x2):
    common_len = min(len(x1), len(x2))
    x1_cut = x1[0:common_len - 1]
    x2_cut = x2[0:common_len - 1]
    corr = pearson_corr(x1_cut, x2_cut)
    delta = x1_cut - x2_cut
    mae = np.sum(np.abs(delta)) / common_len
    print(corr, mae)
    return corr, mae


if __name__ == '__main__':
    sample1 = stats.norm.rvs(loc=5, scale=20, size=100)
    sample2 = stats.norm.rvs(loc=6, scale=10, size=150)
    #print(len(sample1))
    Welch_t_test(sample1, sample2)