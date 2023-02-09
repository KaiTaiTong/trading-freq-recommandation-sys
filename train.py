import os
import multiprocessing
from utils.io import load_yaml_config, save_as_pkl
from utils.stock_profile_core import StockProfile, pd, np
from tqdm import tqdm
from sklearn.mixture import GaussianMixture

CONFIG = load_yaml_config('./configs.yaml')


def train(profile_path):
    """
    Training process for Gaussian Mixture Models. Hyperparameters are selected automatically using AIC score, 
    rather than cross validation. GMM weights are saved as pickle files for each trade_window

    Args:
        profile_path (str): profile_path
    """
    current_stock = StockProfile(pd.read_csv(profile_path))
    parameters = {'stock_profile_path': profile_path}
    for trade_window in range(1, CONFIG['MAX_TIME'], CONFIG['INTERVAL']):
        marginal_profit = current_stock.get_marginal_profit_on_n_day_trading(trade_window, mode='percentage')
        
        # training with auto tuning
        aic = []
        for n in range(1, CONFIG['MAX_N_GMM']):
            gmm = GaussianMixture(n_components=n)
            gmm.fit(marginal_profit.reshape(-1, 1))
            aic.append(gmm.aic(marginal_profit.reshape(-1, 1)))
        best_n = np.argmin(aic) + 1

        gmm = GaussianMixture(n_components=best_n)
        gmm.fit(marginal_profit.reshape(-1, 1))
        
        # save parameters
        parameters[trade_window] = {
            'means': gmm.means_, 
            'covariances': gmm.covariances_, 
            'weights': gmm.weights_
        }
    
    print(f'GMM training completed: {profile_path}')
    output_param_filename = os.path.join(CONFIG['PARAM_DIR'], profile_path.split('/')[-1][:-len('.csv')] + '.pkl')
    save_as_pkl(parameters, output_param_filename)


if __name__ == '__main__':

    profile_path_list = np.loadtxt('./data/train_set.txt', dtype=str)
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(train, profile_path_list)