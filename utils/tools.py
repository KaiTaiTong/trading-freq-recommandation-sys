import pandas as pd
import numpy as np

def compute_marginal_profit(open_stock_price, close_stock_price, trade_window):
    """
    Compute the marginal profit given open and close stock price historical record and 
    a trade_window. e.g.,

    if day trading, trade_window = 1, and the marginal profits for any given time investment 
    is close_stock_price - open_stock_price. That is buy on any given day and sell on the same 
    day closing

    Args:
        open_stock_price (np.array): 1D array 
        close_stock_price (np.array): 1D array 
        trade_window (int): trade window

    Returns:
        (np.array): profits array at each given day investment
    """
    assert(open_stock_price.shape == close_stock_price.shape), "Input stock price array must share same size"
    assert(trade_window < open_stock_price.shape[0]), "trade_window too large"
    assert(open_stock_price.ndim == 1 and close_stock_price.ndim == 1), "dim must be 1D"
    return close_stock_price[trade_window-1:-1] - open_stock_price[0:-trade_window]