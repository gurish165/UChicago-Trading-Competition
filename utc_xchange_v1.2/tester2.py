import numpy as np
# import pandas as pd
# from matplotlib import pyplot as plt
from scipy.optimize import fsolve
from scipy.stats import norm
from py_vollib.black_scholes.greeks import analytical

def delta(S, K, sigma, t, r, flag):
    return analytical.delta(flag, S, K, t, r, sigma) * 100

def gamma(S, K, sigma, t, r, flag):
    return analytical.gamma(flag, S, K, t, r, sigma) * 100

def theta(S, K, sigma, t, r, flag):
    return analytical.theta(flag, S, K, t, r, sigma) * 100

def vega(S, K, sigma, t, r, flag):
    return analytical.vega(flag, S, K, t, r, sigma) * 100

if __name__ == '__main__':
    for i in range(-40):
        printi
