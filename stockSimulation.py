import numpy as np


def naiveStockPathSimulate(initialStockPrice, steps, mu, sigma, maturityTime):
    dt = maturityTime / steps
    path = [initialStockPrice]
    for i in range(steps-1):

        # Z is under normal distribution
        Z = np.random.normal(0,1)

        # Use the formula as described
        path.append(path[i] * (1 + mu * dt + sigma * Z * np.sqrt(dt)))

    return path


