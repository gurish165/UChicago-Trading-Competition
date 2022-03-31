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
    window_size = 100
    risk_aversion = 2
    diluted_shares = [425000000,246970000,576250000,4230000000,1930000000,3370000000,16320000000,7510000000,508840000]
    m = 0.02

    # Loading Global Data
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

    ## MARKOWITZ PORTFOLIO MINIMUM ##
    recent_price_change_data = np.array(price_percent_change[-200:], dtype=np.float64) # price_data[-200:].to_numpy()
    expected_return = np.mean(recent_price_change_data, axis=0)
    covariance_matrix = np.cov(recent_price_change_data.T) # 9 x 9 (C)
    inverted_covariance_matrix = np.linalg.inv(covariance_matrix)
    
    w_numerator = np.array(diluted_shares, dtype='float')*np.array(asset_prices, dtype='float')
    market_cap = np.dot(diluted_shares,asset_prices)
    w_mkt = w_numerator / market_cap

    implied_expected_return = risk_aversion*np.matmul(covariance_matrix,w_mkt)
    implied_expected_return = np.array(implied_expected_return, dtype='float')

    # MINIMUM VARIANCE GIVEN m
    lamb_1 = (implied_expected_return @ inverted_covariance_matrix @ implied_expected_return.T \
              - m*np.ones(9)@inverted_covariance_matrix@implied_expected_return.T) \
              / (np.ones(9)@inverted_covariance_matrix@np.ones(9).T)*(implied_expected_return@inverted_covariance_matrix@implied_expected_return.T) \
              - np.square(np.ones(9)@inverted_covariance_matrix@implied_expected_return.T)
    lamb_2 = (m*implied_expected_return@inverted_covariance_matrix@implied_expected_return.T \
              - np.ones(9)@inverted_covariance_matrix@implied_expected_return.T) \
              / (np.ones(9)@inverted_covariance_matrix@np.ones(9).T)*(implied_expected_return@inverted_covariance_matrix@implied_expected_return.T) \
              - np.square(np.ones(9)@inverted_covariance_matrix@implied_expected_return.T)
    weight = lamb_1 * np.ones(9) @ inverted_covariance_matrix + lamb_2 * implied_expected_return @ inverted_covariance_matrix
    # print(weight)

    return weight
    
    ## MINIMUM VARIANCE PORTFOLIO
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
