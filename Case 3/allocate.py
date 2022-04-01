from glob import glob
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt

#########################################################################
## Change this code to take in all asset price data and predictions    ##
## for one day and allocate your portfolio accordingly.                ##
#########################################################################

price_data = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
price_percent_change = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

analyst_1_prediction = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
analyst_1_percent_change = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

analyst_2_prediction = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
analyst_2_percent_change = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

analyst_3_prediction = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
analyst_3_percent_change = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

clustered_percent_change = pd.DataFrame(columns=['AC', 'B', 'DEF', 'GH', 'I'])

window_size = 10

def allocate_portfolio(asset_prices, asset_price_predictions_1, \
                       asset_price_predictions_2,\
                       asset_price_predictions_3):
    ## HYPERPARAMETER
    global window_size
    risk_aversion = 1

    # Loading Global Data
    diluted_shares = [425000000,246970000,576250000,4230000000,1930000000,3370000000,16320000000,7510000000,508840000]
    global price_data
    global price_percent_change
    global analyst_1_prediction
    global analyst_1_percent_change
    global analyst_2_prediction
    global analyst_2_percent_change
    global analyst_3_prediction
    global analyst_3_percent_change
    global clustered_percent_change

    # Append all the percent change data to the dataframes
    if len(price_data)>0:
        # ASSET PRICE PERCENT CHANGE
        old_data = price_data.iloc[-1].values.tolist()
        percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_data, dtype=np.float64)) / np.array(old_data, dtype=np.float64)
        price_percent_change = price_percent_change.append(pd.Series(percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        # NUMBER OF DAYS LEFT BEFORE THE NEXT MONTH
        num_days_left_in_month = 21 - ((len(price_data)-1) % 21)

        # PREDICTION OF ANALYST 1 PCT CHANGE
        old_p1_data = analyst_1_prediction.iloc[-1].values.tolist()
        p1_percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_p1_data, dtype=np.float64)) / np.array(asset_prices, dtype=np.float64)
        p1_percent_change /= num_days_left_in_month
        analyst_1_percent_change = analyst_1_percent_change.append(pd.Series(p1_percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        # PREDICTION OF ANALYST 1 PCT CHANGE
        old_p2_data = analyst_2_prediction.iloc[-1].values.tolist()
        p2_percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_p2_data, dtype=np.float64)) / np.array(asset_prices, dtype=np.float64)
        p2_percent_change /= num_days_left_in_month
        analyst_2_percent_change = analyst_2_percent_change.append(pd.Series(p2_percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        # PREDICTION OF ANALYST 1 PCT CHANGE
        old_p3_data = analyst_3_prediction.iloc[-1].values.tolist()
        p3_percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_p3_data, dtype=np.float64)) / np.array(asset_prices, dtype=np.float64)
        p3_percent_change /= num_days_left_in_month
        analyst_3_percent_change = analyst_3_percent_change.append(pd.Series(p3_percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        ## CLUSTERING TIME!!!
        cluster_1_AC = (np.array(asset_prices[0]+asset_prices[2], dtype=np.float64) - np.array(old_data[0] + old_data[2], dtype=np.float64)) / np.array(old_data[0] + old_data[2], dtype=np.float64)
        cluster_2_DEF = (np.array(asset_prices[3]+asset_prices[4]+asset_prices[5], dtype=np.float64) - np.array(old_data[3] + old_data[4] + old_data[5], dtype=np.float64)) / np.array(old_data[3] + old_data[4] + old_data[5], dtype=np.float64)
        cluster_3_GH = (np.array(asset_prices[6]+asset_prices[7], dtype=np.float64) - np.array(old_data[6] + old_data[7], dtype=np.float64)) / np.array(old_data[6] + old_data[7], dtype=np.float64)

    # Append all the input data to the dataframes
    price_data = price_data.append(pd.Series(asset_prices, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    analyst_1_prediction = analyst_1_prediction.append(pd.Series(asset_price_predictions_1, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    analyst_2_prediction = analyst_2_prediction.append(pd.Series(asset_price_predictions_2, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)
    analyst_3_prediction = analyst_3_prediction.append(pd.Series(asset_price_predictions_3, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)


    ## CALCULATE CORREALATION
    # if len(price_data)==2509:
    #     price_percent_change = price_percent_change.astype(float)
    #     corr_df = price_percent_change.corr(method='pearson')
    #     corr_df.to_csv('correlation.csv')
    #     plt.imshow(corr_df.to_numpy(), cmap='RdPu')
    #     plt.colorbar()
    #     plt.savefig('correlation.png')

    # IF IT DIDN'T PASS THE WINDOW SIZE YET
    if len(price_data)+1 < window_size:
        return np.zeros(9)

    ## PRICE_CHANGE && PRICE COVARIANCE MATRIX
    recent_price_change_data = np.array(price_percent_change[-window_size:], dtype=np.float64) # price_data[-200:].to_numpy()
    average_return = np.mean(recent_price_change_data, axis=0)
    covariance_matrix = np.cov(recent_price_change_data.T) # / np.sqrt(window_size-1)# 9 x 9 (SIMGA)
    inverted_covariance_matrix = np.linalg.inv(covariance_matrix)
    
    ## CALCULATING MARKET CAPITALIZATION WEIGHTS
    w_numerator = np.array(diluted_shares, dtype='float')*np.array(asset_prices, dtype='float')
    market_cap = np.dot(diluted_shares,asset_prices)
    w_mkt = w_numerator / market_cap

    ## BLACK-LITTERMAN: IMPLIED EXPECTED RETURN
    implied_expected_return = risk_aversion*np.matmul(covariance_matrix,w_mkt)
    implied_expected_return = np.array(implied_expected_return, dtype='float') # (PI)
    # print("IMPLIED EXPECTED RETURN:\n", implied_expected_return)


    ## BLACK-LITTERMAN: EXPECTED RETURN

    # THREE ANALYSTS COVARIANCE MATRIX && EXPECTED RETURN
    p1_price_change_data = np.array(analyst_1_percent_change[-window_size:], dtype=np.float64)
    p2_price_change_data = np.array(analyst_2_percent_change[-window_size:], dtype=np.float64)
    p3_price_change_data = np.array(analyst_3_percent_change[-window_size:], dtype=np.float64)
    analyst_price_chage_data = p1_price_change_data * 0.5 + p2_price_change_data * 0.25 + p3_price_change_data * 0.25
    analyst_covariance_matrix = np.cov(analyst_price_chage_data.T) # / np.sqrt(window_size-1) # 9 x 9 (OMEGA)
    inverted_analyst_covariance_matrix = np.linalg.inv(analyst_covariance_matrix) # INVERTED OMEGA
    analyst_expected_return = np.mean(analyst_price_chage_data, axis=0) # 9 X 1 (Q)
    
    black_litterman_cov_matrix = np.linalg.inv(inverted_covariance_matrix + inverted_analyst_covariance_matrix)
    expected_return = black_litterman_cov_matrix @ ((inverted_covariance_matrix @ implied_expected_return) + inverted_analyst_covariance_matrix @ analyst_expected_return)

    expected_return = analyst_expected_return
    ## HYPERPARAMETER: SET M VALUE
    m = 10 #  + np.std(expected_return) 

    ## MINIMUM VARIANCE GIVEN m
    lamb_1 = ((expected_return @ black_litterman_cov_matrix @ expected_return.T) \
              - (m * np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)) \
              / (((np.ones(9) @ black_litterman_cov_matrix @ np.ones(9).T) * (expected_return @black_litterman_cov_matrix @ expected_return.T)) \
              - (np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)**2)

    lamb_2 = ((m * np.ones(9) @ black_litterman_cov_matrix @ np.ones(9).T) \
              - (np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)) \
              / (((np.ones(9) @ black_litterman_cov_matrix @ np.ones(9).T)*(expected_return @ black_litterman_cov_matrix @ expected_return.T)) \
              - (np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)**2)

    weight = (lamb_1 * np.ones(9) @ black_litterman_cov_matrix) + (lamb_2 * expected_return @ black_litterman_cov_matrix)
    # print(weight)

    return -weight
    
    ## MINIMUM VARIANCE PORTFOLIO
    row_sum_1C = black_litterman_cov_matrix.sum(axis=1, dtype='float')
    total_sum_1C1 = black_litterman_cov_matrix.sum(dtype='float')
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
