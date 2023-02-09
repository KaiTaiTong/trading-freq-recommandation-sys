import pandas as pd
import numpy as np

class StockProfile:
    
    def __init__(self, stock_df):
        self.stock_df = stock_df
        self._preprocess()
    
    def _preprocess(self):
        """
        Basic Preprocessing steps for raw stock dataframe. Procedures involve, 
        1. Remove duplicated samples based on date
        2. Conversion of obj type to datetime and float
        3. Upsample to full time span with time-series linear interpolation 
        """
        columns_names = self.stock_df.columns.values
        assert('Date' in columns_names), "Input stock dataframe must contain column Date"
        interpo_logs = {}

        # Remove duplicated Date
        self.stock_df.drop_duplicates(subset='Date', keep='first', inplace=True)
        self.stock_df['Date'] = pd.to_datetime(self.stock_df['Date'])
        
        first_date, last_date = self.stock_df.iloc[0]['Date'], self.stock_df.iloc[-1]['Date']

        # Upsample
        reinterpolated_df = pd.DataFrame(columns=columns_names)
        reinterpolated_df['Date'] = pd.bdate_range(start=first_date, end=last_date)
        reinterpolated_df.loc[reinterpolated_df['Date'].isin(self.stock_df['Date']), columns_names[1:]] = self.stock_df.loc[self.stock_df['Date'].isin(reinterpolated_df['Date']), columns_names[1:]].values
        
        reinterpolated_df = reinterpolated_df.set_index('Date')
        for i in columns_names[1:]:
            reinterpolated_df[i] = pd.to_numeric(reinterpolated_df[i])
        interpo_logs['nan_count'] = reinterpolated_df.isna().sum()
        interpo_logs['prior_interpo'] = np.asarray(reinterpolated_df)

        # Linear interpolate based on time
        reinterpolated_df = reinterpolated_df.interpolate('time')
        interpo_logs['after_interpo'] = np.asarray(reinterpolated_df)

