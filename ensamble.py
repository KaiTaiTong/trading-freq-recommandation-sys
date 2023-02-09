import numpy as np
import os
from utils.io import load_as_pkl, load_yaml_config
from tqdm import tqdm
from sklearn.mixture import GaussianMixture

CONFIG = load_yaml_config('./configs.yaml')


def ensamble_GMM(x):
    """
    Ensamble GMM using a weighted average of all GMMs trained for same trade_window. Note 
    that x needs to be large enough to cover the range

    Args:
        x (np.array): marginal profits array 

    Returns:
        (dict): ensambled GMM
    """
    logprob_ensamble = {}
    counter = 0
    for i in os.listdir('./models/'):
        if i.endswith('.pkl'):
            parameters = load_as_pkl('./models/'+i)
            counter += 1
            for trade_window in tqdm(range(1, CONFIG['MAX_TIME'], CONFIG['INTERVAL'])):
                gmm_means = parameters[trade_window]['means']
                gmm_conv = parameters[trade_window]['covariances']
                gmm_weights = parameters[trade_window]['weights']
                gmm_n = gmm_weights.shape[0]
                
                gmm = GaussianMixture(n_components=gmm_n)
                gmm.fit(np.asarray([1,2,3,4,5]).reshape(-1, 1)) # trick to load gmm param
                gmm.weights_ = gmm_weights
                gmm.means_ = gmm_means
                gmm.covariances_ = gmm_conv 
                logprob = gmm.score_samples(x)
                
                if trade_window not in logprob_ensamble.keys():
                    logprob_ensamble[trade_window] = logprob
                else:
                    logprob_ensamble[trade_window] += logprob

    for i in logprob_ensamble.keys():
        logprob_ensamble[i] /= counter

    return logprob_ensamble

if __name__ == '__main__':
    
    x = np.linspace(-50, 50, 1000).reshape(-1, 1)
    logprob_ensamble = ensamble_GMM(x)