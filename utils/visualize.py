from scipy.interpolate import spline
import matplotlib.pyplot as plt
import numpy as np
import time

TRIAL=str(int(time.time()))

def smooth_xy(xs, ys, points_ratio=10):
  assert (len(xs) == len(ys)), "length mismatch between axises"
  points = int(len(xs) * points_ratio)
  xs_s = np.linspace(xs.min(),xs.max(),points) #300 represents number of points to make between xs.min and xs.max
  ys_s = spline(xs,ys,xs_s)
  return (xs_s, ys_s)

def remove_outliers(arr, m=2):
  u = np.mean(arr)
  s = np.std(arr)
  filtered = [e for e in arr if (u - 2 * s < e < u + 2 * s)]
  return filtered

def moving_avg(arr, window=10):
  cumsum_vec = np.cumsum(np.insert(arr, 0, 0))
  ma_vec = (cumsum_vec[window:] - cumsum_vec[:-window]) / window
  return ma_vec

def plot_linear(xs, ys, fname=None):
    assert (len(xs) == len(ys)), "length mismatch between axises"
    plt.plot(xs, ys, c='b')
    if (fname):
        plt.savefig(f'figs/{fname}-{TRIAL}.jpg')
        plt.close()
