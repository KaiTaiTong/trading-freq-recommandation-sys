import matplotlib.pyplot as plt
import numpy as np

def plot_interpolation_stock_profile(preprocess_log, index=0):

    assert(index < preprocess_log['prior_interpo'].shape[1]), 'invalid index'
    nan_contained_array = preprocess_log['prior_interpo'][:, index]
    interpo_array = preprocess_log['after_interpo'][:, index]
    nan_indices = np.where(np.isnan(nan_contained_array))

    fig, ax = plt.subplots()
    ax.plot(nan_contained_array, 'r', label='nan_contained_array')
    ax.scatter(nan_indices, interpo_array[nan_indices], c='b', marker='o', label='interpolated NaN')

    ax.legend()
    plt.show()