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

clustered_percent_change = pd.DataFrame(columns=['AC', 'DEF', 'GH', 'B', 'I'])
a1_clustered_percent_change = pd.DataFrame(columns=['AC', 'DEF', 'GH', 'B', 'I'])
a2_clustered_percent_change = pd.DataFrame(columns=['AC', 'DEF', 'GH', 'B', 'I'])
a3_clustered_percent_change = pd.DataFrame(columns=['AC', 'DEF', 'GH', 'B', 'I'])

# window_size = 10

def allocate_portfolio(asset_prices, asset_price_predictions_1, \
                       asset_price_predictions_2,\
                       asset_price_predictions_3):
    ## HYPERPARAMETER
    # global window_size
    window_size = 10
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
    global a1_clustered_percent_change
    global a2_clustered_percent_change
    global a3_clustered_percent_change 

    # Append all the percent change data to the dataframes
    if len(price_data)>0:
        # ASSET PRICE PERCENT CHANGE
        old_data = price_data.iloc[-1].values.tolist()
        percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_data, dtype=np.float64)) / np.array(old_data, dtype=np.float64)*100
        price_percent_change = price_percent_change.append(pd.Series(percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        # NUMBER OF DAYS LEFT BEFORE THE NEXT MONTH
        num_days_left_in_month = 21 - ((len(price_data)-1) % 21)

        # PREDICTION OF ANALYST 1 PCT CHANGE
        old_p1_data = analyst_1_prediction.iloc[-1].values.tolist()
        p1_percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_p1_data, dtype=np.float64)) / np.array(asset_prices, dtype=np.float64)*100
        p1_percent_change /= num_days_left_in_month
        analyst_1_percent_change = analyst_1_percent_change.append(pd.Series(p1_percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        # PREDICTION OF ANALYST 2 PCT CHANGE
        old_p2_data = analyst_2_prediction.iloc[-1].values.tolist()
        p2_percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_p2_data, dtype=np.float64)) / np.array(asset_prices, dtype=np.float64)*100
        p2_percent_change /= num_days_left_in_month
        analyst_2_percent_change = analyst_2_percent_change.append(pd.Series(p2_percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        # PREDICTION OF ANALYST 3 PCT CHANGE
        old_p3_data = analyst_3_prediction.iloc[-1].values.tolist()
        p3_percent_change = (np.array(asset_prices, dtype=np.float64) - np.array(old_p3_data, dtype=np.float64)) / np.array(asset_prices, dtype=np.float64)*100
        p3_percent_change /= num_days_left_in_month
        analyst_3_percent_change = analyst_3_percent_change.append(pd.Series(p3_percent_change, index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']), ignore_index=True)

        ######################################################################################################################################################################################################

        ## CLUSTERING TIME!!!
        cluster_1_AC = (np.array(asset_prices[0]+asset_prices[2], dtype=np.float64) - np.array(old_data[0] + old_data[2], dtype=np.float64)) / np.array(old_data[0] + old_data[2], dtype=np.float64)
        cluster_2_DEF = (np.array(asset_prices[3]+asset_prices[4]+asset_prices[5], dtype=np.float64) - np.array(old_data[3] + old_data[4] + old_data[5], dtype=np.float64)) / np.array(old_data[3] + old_data[4] + old_data[5], dtype=np.float64)
        cluster_3_GH = (np.array(asset_prices[6]+asset_prices[7], dtype=np.float64) - np.array(old_data[6] + old_data[7], dtype=np.float64)) / np.array(old_data[6] + old_data[7], dtype=np.float64)
        cluster_pct_change = [cluster_1_AC, cluster_2_DEF, cluster_3_GH, percent_change[1], percent_change[8]]
        cluster_pct_change = np.array(cluster_pct_change)*100.0
        clustered_percent_change = clustered_percent_change.append(pd.Series(cluster_pct_change, index = ['AC', 'DEF', 'GH', 'B', 'I']), ignore_index=True)

        a1_percent_change = [np.mean(p1_percent_change[0]+p1_percent_change[2]), np.mean(p1_percent_change[3]+p1_percent_change[4]+p1_percent_change[5]), np.mean(p1_percent_change[6]+p1_percent_change[7]), p1_percent_change[1], p1_percent_change[8]]
        a2_percent_change = [np.mean(p2_percent_change[0]+p2_percent_change[2]), np.mean(p2_percent_change[3]+p2_percent_change[4]+p2_percent_change[5]), np.mean(p2_percent_change[6]+p2_percent_change[7]), p2_percent_change[1], p2_percent_change[8]]
        a3_percent_change = [np.mean(p3_percent_change[0]+p3_percent_change[2]), np.mean(p3_percent_change[3]+p3_percent_change[4]+p3_percent_change[5]), np.mean(p3_percent_change[6]+p3_percent_change[7]), p3_percent_change[1], p3_percent_change[8]]
        a1_clustered_percent_change = a1_clustered_percent_change.append(pd.Series(a1_percent_change, index = ['AC', 'DEF', 'GH', 'B', 'I']), ignore_index=True)
        a2_clustered_percent_change = a2_clustered_percent_change.append(pd.Series(a2_percent_change, index = ['AC', 'DEF', 'GH', 'B', 'I']), ignore_index=True)
        a3_clustered_percent_change = a3_clustered_percent_change.append(pd.Series(a3_percent_change, index = ['AC', 'DEF', 'GH', 'B', 'I']), ignore_index=True)


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

    # # IF IT DIDN'T PASS THE WINDOW SIZE YET
    # if len(price_data)+1 < window_size:
    #     return np.zeros(9)

    ## PRICE_CHANGE && PRICE COVARIANCE MATRIX
    recent_price_change_data = np.array(price_percent_change[-window_size:], dtype=np.float64) # price_data[-200:].to_numpy()
    average_return = np.mean(recent_price_change_data, axis=0)
    covariance_matrix = np.cov(recent_price_change_data.T) # / np.sqrt(window_size-1)# 9 x 9 (SIMGA)
    inverted_covariance_matrix = np.linalg.inv(covariance_matrix)
    
    # ## CALCULATING MARKET CAPITALIZATION WEIGHTS
    # w_numerator = np.array(diluted_shares, dtype='float')*np.array(asset_prices, dtype='float')
    # market_cap = np.dot(diluted_shares,asset_prices)
    # w_mkt = w_numerator / market_cap

    # ## BLACK-LITTERMAN: IMPLIED EXPECTED RETURN
    # implied_expected_return = risk_aversion*np.matmul(covariance_matrix,w_mkt)
    # implied_expected_return = np.array(implied_expected_return, dtype='float') # (PI)
    # # print("IMPLIED EXPECTED RETURN:\n", implied_expected_return)


    # ## BLACK-LITTERMAN: EXPECTED RETURN

    # # THREE ANALYSTS COVARIANCE MATRIX && EXPECTED RETURN
    p1_price_change_data = np.array(analyst_1_percent_change[-window_size:], dtype=np.float64)
    p2_price_change_data = np.array(analyst_2_percent_change[-window_size:], dtype=np.float64)
    p3_price_change_data = np.array(analyst_3_percent_change[-window_size:], dtype=np.float64)
    analyst_price_chage_data = p1_price_change_data * 0.5 + p2_price_change_data * 0.25 + p3_price_change_data * 0.25
    analyst_covariance_matrix = np.cov(analyst_price_chage_data.T) # / np.sqrt(window_size-1) # 9 x 9 (OMEGA)
    inverted_analyst_covariance_matrix = np.linalg.inv(analyst_covariance_matrix) # INVERTED OMEGA
    analyst_expected_return = np.mean(analyst_price_chage_data, axis=0) # 9 X 1 (Q)
    
    black_litterman_cov_matrix = np.linalg.inv(inverted_covariance_matrix + inverted_analyst_covariance_matrix)
    # expected_return = black_litterman_cov_matrix @ ((inverted_covariance_matrix @ implied_expected_return) + inverted_analyst_covariance_matrix @ analyst_expected_return)

    # expected_return = analyst_expected_return
    # ## HYPERPARAMETER: SET M VALUE
    # m = 10 #  + np.std(expected_return) 

    # ## MINIMUM VARIANCE GIVEN m
    # lamb_1 = ((expected_return @ black_litterman_cov_matrix @ expected_return.T) \
    #           - (m * np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)) \
    #           / (((np.ones(9) @ black_litterman_cov_matrix @ np.ones(9).T) * (expected_return @black_litterman_cov_matrix @ expected_return.T)) \
    #           - (np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)**2)

    # lamb_2 = ((m * np.ones(9) @ black_litterman_cov_matrix @ np.ones(9).T) \
    #           - (np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)) \
    #           / (((np.ones(9) @ black_litterman_cov_matrix @ np.ones(9).T)*(expected_return @ black_litterman_cov_matrix @ expected_return.T)) \
    #           - (np.ones(9) @ black_litterman_cov_matrix @ expected_return.T)**2)

    # weight = (lamb_1 * np.ones(9) @ black_litterman_cov_matrix) + (lamb_2 * expected_return @ black_litterman_cov_matrix)
    # # print(weight)

    # # return -weight
    
    # ## MINIMUM VARIANCE PORTFOLIO
    # row_sum_1C = black_litterman_cov_matrix.sum(axis=1, dtype='float')
    # total_sum_1C1 = black_litterman_cov_matrix.sum(dtype='float')
    # weight_1 = np.array(row_sum_1C / total_sum_1C1)
    # # return weight

    ######################################################################################################################################################################################################

    ## CLUSTERING

    ## PRICE_CHANGE && PRICE COVARIANCE MATRIX
    clustered_recent_price_change_data = np.array(clustered_percent_change[-window_size:], dtype=np.float64) # price_data[-200:].to_numpy()
    clustered_average_return = np.mean(clustered_recent_price_change_data, axis=0)
    clustered_covariance_matrix = np.cov(clustered_recent_price_change_data.T) # / np.sqrt(window_size-1)# 9 x 9 (SIMGA)
    inv_clustered_covariance_matrix = np.linalg.inv(clustered_covariance_matrix)
    
    ## CALCULATING MARKET CAPITALIZATION WEIGHTS
    c_w_numerator = np.array([(diluted_shares[0]*asset_prices[0]+diluted_shares[2]*asset_prices[2]), \
                            (diluted_shares[3]*asset_prices[3]+diluted_shares[4]*asset_prices[4]+diluted_shares[5]*asset_prices[5]), \
                            (diluted_shares[6]*asset_prices[6]+diluted_shares[7]*asset_prices[7]), \
                            (diluted_shares[1]*asset_prices[1]), \
                            (diluted_shares[8]*asset_prices[8])])
    c_market_cap = np.dot(diluted_shares,asset_prices)
    c_w_mkt = c_w_numerator / c_market_cap

    ## BLACK-LITTERMAN: IMPLIED EXPECTED RETURN
    c_implied_expected_return = risk_aversion*np.matmul(clustered_covariance_matrix,c_w_mkt)
    c_implied_expected_return = np.array(c_implied_expected_return, dtype='float') # (PI)
    # print("IMPLIED EXPECTED RETURN:\n", implied_expected_return)


    ## BLACK-LITTERMAN: EXPECTED RETURN

    # THREE ANALYSTS COVARIANCE MATRIX && EXPECTED RETURN
    a1_price_change_data = np.array(a1_clustered_percent_change[-window_size:], dtype=np.float64)
    a2_price_change_data = np.array(a2_clustered_percent_change[-window_size:], dtype=np.float64)
    a3_price_change_data = np.array(a3_clustered_percent_change[-window_size:], dtype=np.float64)
    c_analyst_price_chage_data = a1_price_change_data * 0.5 + a2_price_change_data * 0.25 + a3_price_change_data * 0.25
    c_analyst_price_chage_data_cov = np.cov(c_analyst_price_chage_data.T) # / np.sqrt(window_size-1) # 9 x 9 (OMEGA)
    c_inverted_analyst_covariance_matrix = np.linalg.inv(c_analyst_price_chage_data_cov) # INVERTED OMEGA
    c_analyst_expected_return = np.mean(c_analyst_price_chage_data, axis=0) # 9 X 1 (Q)
    
    c_black_litterman_cov_matrix = np.linalg.inv(inv_clustered_covariance_matrix + c_inverted_analyst_covariance_matrix)
    c_expected_return = c_black_litterman_cov_matrix @ ((inv_clustered_covariance_matrix @ c_implied_expected_return) + c_inverted_analyst_covariance_matrix @ c_analyst_expected_return)

    c_expected_return = c_analyst_expected_return

    ## MINIMUM VARIANCE PORTFOLIO
    c_row_sum_1C = c_black_litterman_cov_matrix.sum(axis=1, dtype='float')
    c_total_sum_1C1 = c_black_litterman_cov_matrix.sum(dtype='float')
    c_weight = c_row_sum_1C / c_total_sum_1C1
    weight_2 = np.array([c_weight[0]/2, c_weight[3], \
                        c_weight[0]/2, (c_weight[1])/3, \
                        (c_weight[1])/3, (c_weight[1])/3, \
                        (c_weight[2])/2, (c_weight[2])/2,
                        c_weight[4]])

    ## RPA
    weight_rpa = np.multiply(weight_2, (weight_2 @ covariance_matrix)) / np.sqrt(np.abs(weight_2 @ black_litterman_cov_matrix @ weight_2.T))
    weight_rpa = np.array(weight_rpa)

    ## RSI
    # rsi_timeframe = price_percent_change[-10:]
    # rsi_timeframe_T = np.transpose(rsi_timeframe)
    # def positive_avg(arr):
    #     return arr[arr > 0].mean()
    # def negative_avg(arr):
    #     return arr[arr < 0].mean()
    # avg_gain = np.apply_along_axis(positive_avg, 1, rsi_timeframe_T)
    # avg_loss = -np.apply_along_axis(negative_avg, 1, rsi_timeframe_T)
    # rsi = 100 - (100/(1+(avg_gain/14)/(avg_loss/14)))
    # weight_rsi = 50 - rsi
    # # weight_sq = (50 - rsi)**2
    # # sign_idx = np.sign(weight_rsi)
    # # weight_rsi = np.multiply(weight_sq, sign_idx) * 0.00001
    # weight_rsi[np.isnan(weight_rsi)] = 0

    final_weights = weight_2 *0.97 + weight_rpa * 0.03
    # final_weights = final_weights + weight_rsi * 0.00001
    # final_weights = np.array(final_weights / np.sum(final_weights))

    # print(np.sum(final_weights))
    # print(final_weights)
    return final_weights
