from py_vollib import black_scholes as bs
from py_vollib import black as blk
import numpy as np
import pandas as pd


def main():
    prices = [120.31,113.83,118.28,111.98,108.41,102.95,105.53,111.05,106.46,104.29,102.25,109.33,115.37,111.69,113.46,115.92,114.78,113.92,120.33, 119.67, 120.24, 123.23, 123.23]
    stdev = np.std(prices[-4:])
    yte = 8/252
    strike = 120
    underlying = 119.40
    c = bs.black_scholes('c', underlying, strike, yte, 0.00, 0.4081390085121087) # 0.42
    print(f"Price per share with volatility: ${c}")
    print(f"Stdev is: {stdev}")
    prices.append(103)
    print(prices)
    stdev = np.std(prices)
    c = bs.black_scholes('c', underlying, strike, yte, 0.00, stdev)
    print(f"Price per share with volatility: ${c}")
    print(f"Stdev is: {stdev}")
    # c = blk.black('c', underlying, strike, yte, 0.001, stdev)
    # print(c)
    data = pd.read_csv("../amd-data.csv")
    close_prices = data["prccd"][-10:]
    print(close_prices)
    data['Log returns'] = np.log(close_prices/close_prices.shift())
    volatility = data['Log returns'].std()*252**0.5
    print(volatility)


if __name__ == "__main__":
    main()