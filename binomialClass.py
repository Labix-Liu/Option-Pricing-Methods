import numpy as np
import scipy

class binomModel:

    def __init__(self, currentOption, currentMarket):

        self.strikePrice = currentOption[0]
        self.maturityTime = currentOption[1]

        self.initialStockPrice = currentMarket[0]
        self.volatility = currentMarket[1]
        self.r = currentMarket[2]

        #self.u = np.exp(self.volatility * np.sqrt(self.timeStep))
        #self.d = np.exp(-self.volatility * np.sqrt(self.timeStep))

    def computeUDP(self, steps):
        timeStep = self.maturityTime / steps

        u = np.exp(self.volatility * np.sqrt(timeStep))
        d = np.exp(-self.volatility * np.sqrt(timeStep))
        p = (np.exp(self.r * timeStep) - d) / (u - d)

        return timeStep, u, d, p

    def computeLastStepPayoff(self, steps):

        timeStep, u, d, p = self.computeUDP(steps)

        payoffs = []
        for i in range(steps+1):
            payoffs.append(np.max([np.power(u,steps-i) * np.power(d,i) * self.initialStockPrice - self.strikePrice,0]))
        return payoffs

    def onePeriodBinomialModel(self):

        timeStep, u, d, p = self.computeUDP(1)
        payoffs = self.computeLastStepPayoff(1)

        return np.exp(-self.r * self.maturityTime) * (p * payoffs[0] + (1 - p) * payoffs[1])

    def europeanMultiPeriodBinomialModel(self, steps):

        timeStep, u, d, p = self.computeUDP(steps)
        optionValue = self.computeLastStepPayoff(steps)

        tmp = 0
        for i in range(steps):
            tmp = tmp + scipy.special.binom(steps, i) * np.power(p,steps-i) * np.power(1-p, i) * optionValue[i]

        optionPrice = np.exp(-steps * self.r * timeStep) * tmp

        return optionPrice

    def americanMultiPeriodBinomialModel(self, steps):

        timeStep, u, d, p = self.computeUDP(steps)

        prevOptionPrice = self.computeLastStepPayoff(steps)

        for i in range(steps-2, -1, -1):

            new = []

            for j in range(i+1):
                new.append(np.max([np.exp(-self.r * timeStep) * (p * prevOptionPrice[j] + (1 - p) * prevOptionPrice[j+1]),]))

            prevOptionPrice = new

        return prevOptionPrice[0]