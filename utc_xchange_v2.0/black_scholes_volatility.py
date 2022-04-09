from math import *

# Cumulative standard normal distribution
def cdf(x):
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

# Call Price based on Black Scholes Model
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   volatility: Volatility percentage (ie. 30% volatility is 0.30)
#             per_share_val = bs.black_scholes('c', underlying_px, strike_px, time_to_expiry, 0.00, volatility)
def black_scholes(flag, underlying_price, exercise_price, time_in_years, risk_free_rate, volatility):
    if flag == 'c' or flag == 'C':
        d1 = (log(underlying_price / exercise_price) + risk_free_rate * time_in_years) / (volatility * sqrt(time_in_years)) + 0.5 * volatility * sqrt(time_in_years)
        d2 = d1 - (volatility * sqrt(time_in_years))
        
        return underlying_price * cdf(d1) - exercise_price * exp(-time_in_years * risk_free_rate) * cdf(d2)
    else:
        return black_scholes_put(underlying_price, exercise_price, time_in_years, risk_free_rate, volatility)
# Put Price based on Black Scholes Model
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   volatility: Volatility percentage (ie. 30% volatility is 0.30)
def black_scholes_put(underlying_price, exercise_price, time_in_years, risk_free_rate, volatility):
    return black_scholes('c',underlying_price, exercise_price, time_in_years, risk_free_rate, volatility) + exercise_price * exp(-risk_free_rate * time_in_years) - underlying_price
