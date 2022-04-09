import numpy as np
# import pandas as pd
# from matplotlib import pyplot as plt
from scipy.optimize import fsolve
from scipy.stats import norm
from py_vollib.black_scholes.greeks import analytical

# def d1(S,K,T,r,sigma):
#     return(np.log(S/K)+(r+sigma**2/2.)*T)/(sigma*np.sqrt(T))
# def d2(S,K,T,r,sigma):
#     return d1(S,K,T,r,sigma)-sigma*np.sqrt(T)

# def bs_call(S,K,T,r,sigma):
#     return S*norm.cdf(d1(S,K,T,r,sigma))-K*np.exp(-r*T)*norm.cdf(d2(S,K,T,r,sigma))
# def bs_put(S,K,T,r,sigma):
#     return K*np.exp(-r*T)-S+bs_call(S,K,T,r,sigma)

#     # Implied Volatility:

# def iv_call(S,K,T,r,C):
#     return max(0, fsolve((lambda sigma: np.abs(bs_call(S,K,T,r,sigma) - C)), [1])[0])
                      
# def iv_put(S,K,T,r,P):
#     return max(0, fsolve((lambda sigma: np.abs(bs_put(S,K,T,r,sigma) - P)), [1])[0])

# def delta_call(S,K,T,C):
#     sigma = iv_call(S,K,T,0,C)
#     return 100 * norm.cdf(d1(S,K,T,0,sigma))

# def gamma_call(S,K,T,C):
#     sigma = iv_call(S,K,T,0,C)
#     return 100 * norm.pdf(d1(S,K,T,0,sigma))/(S * sigma * np.sqrt(T))

# def vega_call(S,K,T,C):
#     sigma = iv_call(S,K,T,0,C)
#     return 100 * norm.pdf(d1(S,K,T,0,sigma)) * S * np.sqrt(T)

# def theta_call(S,K,T,C):
#     sigma = iv_call(S,K,T,0,C)
#     return 100 * S * norm.pdf(d1(S,K,T,0,sigma)) * sigma/(2 * np.sqrt(T))

# def delta_put(S,K,T,C):
#     sigma = iv_put(S,K,T,0,C)
#     return 100 * (norm.cdf(d1(S,K,T,0,sigma)) - 1)

# def gamma_put(S,K,T,C):
#     sigma = iv_put(S,K,T,0,C)
#     return 100 * norm.pdf(d1(S,K,T,0,sigma))/(S * sigma * np.sqrt(T))

# def vega_put(S,K,T,C):
#     sigma = iv_put(S,K,T,0,C)
#     return 100 * norm.pdf(d1(S,K,T,0,sigma)) * S * np.sqrt(T)

# def theta_put(S,K,T,C):
#     sigma = iv_put(S,K,T,0,C)
#     return 100 * S * norm.pdf(d1(S,K,T,0,sigma)) * sigma/(2 * np.sqrt(T))


# S = underlying asset price
# K = strike price
# sigma = vol
# t = time to expiration
# r = risk free interest rate
# flag = flag
def delta(S, K, sigma, t, r, flag):
    return analytical.delta(flag = flag, S = S, K = K, t = t, r = r, sigma = sigma) * 100

def gamma(S, K, sigma, t, r, flag):
    return analytical.gamma(flag = flag, S = S, K = K, t = t, r = r, sigma = sigma) * 100

def theta(S, K, sigma, t, r, flag):
    return analytical.theta(flag = flag, S = S, K = K, t = t, r = r, sigma = sigma) * 100

def vega(S, K, sigma, t, r, flag):
    return analytical.vega(flag = flag, S = S, K = K, t = t, r = r, sigma = sigma) * 100
