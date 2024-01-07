# Intraday Strategy Using GARCH Model

# Load Simulated Daily and Simulated 5-minute data.

import matplotlib.pyplot as plt
from arch import arch_model
import pandas_ta
import pandas as pd
import numpy as np
import os

# Set the data folder path
data_folder = '/Users/mayank/Python_garch/Algorithmic_Trading_Machine_Learning'

# Load simulated daily data
daily_df = pd.read_csv(os.path.join(data_folder, 'daily_data.csv')).drop('Unnamed: 7', axis=1)
daily_df['Date'] = pd.to_datetime(daily_df['Date'])
daily_df = daily_df.set_index('Date')

# Load simulated 5-minute intraday data
intraday_5min_df = pd.read_csv(os.path.join(data_folder, '5min_data.csv')).drop('Unnamed: 6', axis=1)
intraday_5min_df['datetime'] = pd.to_datetime(intraday_5min_df['datetime'])
intraday_5min_df = intraday_5min_df.set_index('datetime')
intraday_5min_df['date'] = pd.to_datetime(intraday_5min_df.index.date)

# Define function to fit GARCH model and predict 1-day ahead volatility in a rolling window.

daily_df['log_ret'] = np.log(daily_df['Adj Close']).diff()
daily_df['variance'] = daily_df['log_ret'].rolling(180).var()
daily_df = daily_df['2020':]

def predict_volatility(x):
    best_model = arch_model(y=x, p=1, q=3).fit(update_freq=5, disp='off')
    variance_forecast = best_model.forecast(horizon=1).variance.iloc[-1, 0]
    print(x.index[-1])
    return variance_forecast

daily_df['predictions'] = daily_df['log_ret'].rolling(180).apply(lambda x: predict_volatility(x))
daily_df = daily_df.dropna()

# Calculate prediction premium and form a daily signal from it.

daily_df['prediction_premium'] = (daily_df['predictions'] - daily_df['variance']) / daily_df['variance']
daily_df['premium_std'] = daily_df['prediction_premium'].rolling(180).std()
daily_df['signal_daily'] = daily_df.apply(lambda x: 1 if (x['prediction_premium'] > x['premium_std'])
                                           else (-1 if (x['prediction_premium'] < x['premium_std'] * -1) else np.nan),
                                          axis=1)
daily_df['signal_daily'] = daily_df['signal_daily'].shift()

# Plot the daily signal
plt.style.use('ggplot')
daily_df['signal_daily'].plot(kind='hist')
plt.show()

# Merge with intraday data and calculate intraday indicators to form the intraday signal.

final_df = intraday_5min_df.reset_index()\
                            .merge(daily_df[['signal_daily']].reset_index(),
                                   left_on='date',
                                   right_on='Date')\
                            .drop(['date', 'Date'], axis=1)\
                            .set_index('datetime')

final_df['rsi'] = pandas_ta.rsi(close=final_df['close'], length=20)
final_df['lband'] = pandas_ta.bbands(close=final_df['close'], length=20).iloc[:, 0]
final_df['uband'] = pandas_ta.bbands(close=final_df['close'], length=20).iloc[:, 2]
final_df['signal_intraday'] = final_df.apply(lambda x: 1 if (x['rsi'] > 70) &
                                                            (x['close'] > x['uband'])
                                             else (-1 if (x['rsi'] < 30) &
                                                         (x['close'] < x['lband']) else np.nan),
                                             axis=1)
final_df['return'] = np.log(final_df['close']).diff()

# Generate the position entry and hold until the end of the day.

final_df['return_sign'] = final_df.apply(lambda x: -1 if (x['signal_daily'] == 1) & (x['signal_intraday'] == 1)
                                          else (1 if (x['signal_daily'] == -1) & (x['signal_intraday'] == -1) else np.nan),
                                          axis=1)
final_df['return_sign'] = final_df.groupby(pd.Grouper(freq='D'))['return_sign']\
                                  .transform(lambda x: x.ffill())
final_df['forward_return'] = final_df['return'].shift(-1)
final_df['strategy_return'] = final_df['forward_return'] * final_df['return_sign']

# Calculate final strategy returns.

import matplotlib.ticker as mtick

strategy_cumulative_return = np.exp(np.log1p(final_df.groupby(pd.Grouper(freq='D'))['strategy_return'].sum()).cumsum()).sub(1)

# Plot the final strategy returns
strategy_cumulative_return.plot(figsize=(16, 6))
plt.title('Intraday Strategy Returns')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.ylabel('Return')
plt.show()
