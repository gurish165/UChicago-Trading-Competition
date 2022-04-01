import pandas as pd
import numpy as np
import alloc
import warnings
warnings.filterwarnings("ignore")

price_data_df = pd.read_csv('Acutal Testing Data.csv')
analyst_1_prediction_df = pd.read_csv('Predicted Testing Data Analyst 1.csv')
analyst_2_prediction_df = pd.read_csv('Predicted Testing Data Analyst 2.csv')
analyst_3_prediction_df = pd.read_csv('Predicted Testing Data Analyst 3.csv')

weight = []
daily_returns= []
daily_returns_by_stock = []
weights_history = []

srs = []

for i in range(len(price_data_df)):
    if i> alloc.window_size:
        weights_history.append(weight)
        prev_row = np.array(price_data_df.iloc[i-1].tolist()[1:], dtype='float')
        current_row = np.array(price_data_df.iloc[i].tolist()[1:], dtype='float')
        return_pct = weight*((current_row - prev_row) / prev_row)
        # print(return_pct)
        daily_returns_by_stock.append(return_pct)
        daily_returns.append(np.sum(return_pct))
        # print("ACTUAL DAILY RETURN:", ((current_row - prev_row) / prev_row))
    
    price_row = price_data_df.iloc[i].tolist()[1:]
    analyst1_row = analyst_1_prediction_df.iloc[i].values.tolist()[1:]
    analyst2_row = analyst_2_prediction_df.iloc[i].values.tolist()[1:]
    analyst3_row = analyst_3_prediction_df.iloc[i].values.tolist()[1:]
    weight = alloc.allocate_portfolio(price_row, analyst1_row, analyst2_row, analyst3_row)

daily_returns_by_stock = np.array(daily_returns_by_stock, dtype='float')
weights_history = np.array(weights_history, dtype='float')
np.savetxt("daily_returns_by_stock.csv", daily_returns_by_stock, delimiter=",")
np.savetxt("weights_history.csv", weights_history, delimiter=",")

# SHARPE RATIO
daily_returns = np.array(daily_returns, dtype='float')
print("DAILY RETURNS :", daily_returns)
print("NAN VALUES:", np.count_nonzero(np.isnan(daily_returns)))
print("Mean :",np.mean(daily_returns))
print("Std :", np.std(daily_returns))
sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns)
print(f"SHARPE RATIO FINAL: {sharpe_ratio}")
