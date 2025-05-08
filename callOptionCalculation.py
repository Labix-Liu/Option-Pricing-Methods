import numpy as np
from scipy.stats import norm

def mcPricer(finalStockPrice, strikePrice, riskFreeInterestRate, maturityTime):
    # calculate sum of pay off / no. of simulations
    s = 0
    for i in finalStockPrice:
        s = s + payoff(i, strikePrice)

    return (s / len(finalStockPrice))*np.exp(-riskFreeInterestRate * maturityTime)

def payoff(finalStockPrice, strikePrice):
    return np.max([finalStockPrice-strikePrice,0])

def blackScholes(initialStockPrice, strikePrice, riskFreeInterestRate, sigma, maturityTime):
    d1 = (np.log(initialStockPrice / strikePrice) + (riskFreeInterestRate + sigma * sigma / 2) * maturityTime) / (sigma * np.sqrt(maturityTime))
    d2 = d1 - (sigma * np.sqrt(maturityTime))

    return norm.cdf(d1) * initialStockPrice - norm.cdf(d2) * strikePrice * np.exp(-riskFreeInterestRate * maturityTime)