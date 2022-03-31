import pandas as pd
import numpy as np
import allocate
import warnings
warnings.filterwarnings("ignore")

price_data_df = pd.read_csv('Acutal Testing Data.csv')
analyst_1_prediction_df = pd.read_csv('Predicted Testing Data Analyst 1.csv')
analyst_2_prediction_df = pd.read_csv('Predicted Testing Data Analyst 2.csv')
analyst_3_prediction_df = pd.read_csv('Predicted Testing Data Analyst 3.csv')

weight = []
daily_returns= []

for i in range(len(price_data_df)):
    if i>20:
        prev_row = np.array(price_data_df.iloc[i-1].tolist()[1:], dtype='float')
        current_row = np.array(price_data_df.iloc[i].tolist()[1:], dtype='float')
        return_pct = weight*((current_row - prev_row) / prev_row)
        # print(return_pct)
        daily_returns.append(np.sum(return_pct))
    
    price_row = price_data_df.iloc[i].tolist()[1:]
    analyst1_row = analyst_1_prediction_df.iloc[i].values.tolist()[1:]
    analyst2_row = analyst_2_prediction_df.iloc[i].values.tolist()[1:]
    analyst3_row = analyst_3_prediction_df.iloc[i].values.tolist()[1:]
    weight = allocate.allocate_portfolio(price_row, analyst1_row, analyst2_row, analyst3_row)

# SHARPE RATIO
daily_returns = np.array(daily_returns, dtype='float')
# print(daily_returns)
print("Mean :",np.mean(daily_returns))
print("Std :", np.std(daily_returns))
sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns)
print("SHARPE RATIO: ", sharpe_ratio)