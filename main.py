import math
import matplotlib.pyplot as plt
import numpy as np
import stockSimulation
import callOptionCalculation
import binomialClass
import customTuples

def pathVisulization(arrOfPath, steps, maturityTime, initialStockPrice):
    plt.style.use('_mpl-gallery')
    x = np.linspace(0, maturityTime, steps)

    for p in arrOfPath:
        plt.plot(x, p)

    plt.axis((0, maturityTime, np.max([initialStockPrice - (maturityTime+1)*initialStockPrice, 0]), initialStockPrice + (maturityTime+1)*initialStockPrice))
    plt.tight_layout()
    plt.xlabel('Years')
    plt.ylabel('Stock Price')

    plt.show()
    plt.close()

# Variables of any option
strikePrice = 50
maturityTime = 0.4167
currentOption = (strikePrice, maturityTime)

# Variables coming from the market
currentStockPrice = 50
sigma = 0.4  # percentage volatility
r = 0.1 # risk-free interest rate
currentMarket = (currentStockPrice, sigma, r)

# Technical variables
steps = 5 # the number of time steps
mu = 0.04  # percentage drift
IterationNum = 1000

b = binomialClass.binomModel(currentOption, currentMarket)

print(b.onePeriodBinomialModel())
print(b.europeanMultiPeriodBinomialModel(steps))
print(b.americanMultiPeriodBinomialModel(steps))


paths = []
for i in range(IterationNum):
    paths.append(stockSimulation.naiveStockPathSimulate(currentStockPrice, steps, mu, sigma, maturityTime))
pathVisulization(paths, steps, maturityTime, currentStockPrice)
finalStockPrice = [p[-1] for p in paths]

result = callOptionCalculation.mcPricer(finalStockPrice, strikePrice, r, maturityTime)
print("The option price is predicted as", result)

blackScholesResults = callOptionCalculation.blackScholes(currentStockPrice, strikePrice, r, sigma, maturityTime)
print("The Solution to Black-Scholes's equation gives: ", blackScholesResults)

print("The MC simulation has a ", round(np.abs((result-blackScholesResults) / blackScholesResults * 100), 10), "% error margin!")

a = [70, 80, 90, 100, 110, 120, 130]
b = []
for i in a:
    b.append(callOptionCalculation.blackScholes(i, strikePrice, r, sigma, maturityTime))

plt.style.use('_mpl-gallery')
plt.plot(a, b)

plt.tight_layout()
plt.xlabel('Initial Stock Price')
plt.ylabel('Option Price')

plt.show()
plt.close()