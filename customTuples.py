class option:
    def __int__(self, strikePrice, maturityTime):
        self.strikePrice = strikePrice
        self.maturityTime = maturityTime


class market:
    def __int__(self, currentStockPrice, volatility, interest):
        self.currentStockPrice = currentStockPrice
        self.volatility = volatility
        self.interest = interest