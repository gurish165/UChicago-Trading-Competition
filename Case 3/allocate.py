import numpy as np
import pandas as pd
import scipy

#########################################################################
## Change this code to take in all asset price data and predictions    ##
## for one day and allocate your portfolio accordingly.                ##
#########################################################################

price_data = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
price_percent_change = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
analyst_1_prediction = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
analyst_2_prediction = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
analyst_3_prediction = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

def allocate_portfolio(asset_prices, asset_price_predictions_1, \
                       asset_price_predictions_2,\
                       asset_price_predictions_3):
    window_size = 20
    global price_data
    global analyst_1_prediction
    global analyst_2_prediction
    global analyst_3_prediction
    global price_percent_change

    # Append all the input data to the dataframes
    if len(price_data)>0:
        old_data = price_data.iloc[-1].values.tolist()
        percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_data, dtype=np.float64)) / np.array(old_data, dtype=np.float64)
        price_percent_change = price_percent_change.append(pd.Series(percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

    price_data = price_data.append(pd.Series(asset_prices, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    analyst_1_prediction = analyst_1_prediction.append(pd.Series(asset_price_predictions_1, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    analyst_2_prediction = analyst_2_prediction.append(pd.Series(asset_price_predictions_2, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    analyst_3_prediction = analyst_3_prediction.append(pd.Series(asset_price_predictions_3, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    
    if len(price_data)+1 < window_size:
        return 0

    ## MARKOWITZ PORTFOLIO MINIMUM VARIANCE ##
    recent_price_change_data = np.array(price_percent_change[-200:], dtype=np.float64) # price_data[-200:].to_numpy()
    # print(recent_price_change_data.shape)
    expected_value_price = np.mean(recent_price_change_data, axis=0) # 1 x 9 (mu)
    covariance_matrix = np.cov(recent_price_change_data.T) # 1 x 9 (sigma)
    # print(covariance_matrix)

    inverted_covariance_matrix = np.linalg.inv(covariance_matrix)
    row_sum_1C = inverted_covariance_matrix.sum(axis=1, dtype='float')
    total_sum_1C1 = inverted_covariance_matrix.sum(dtype='float')
    weight = row_sum_1C / total_sum_1C1
    return weight


    # This simple strategy equally weights all assets every period
    # (called a 1/n strategy).
    n_assets = len(asset_prices)
    weights = np.repeat(1 / n_assets, n_assets)
    return weights

'''
1. Calculate the expected return and std. using past x (window size) data and calcuate weigths for MVP
2. Incooperate the analyst predictions to make adjustments to my weights (depends on what they think will happen next month)
3. Set weights based on Large Cap vs Small Cap && Look at the past data on how they performed
4. Calculate Daily Return ( weights*today_data / weights*tmr_data )

5. Come up with something creative

'''
