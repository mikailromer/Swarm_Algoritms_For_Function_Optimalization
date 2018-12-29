import numpy as np

def CostFunctionForPlot(X, Y):
    return np.exp(np.sin(-np.sqrt(X**2+Y**2)))
    # return X ** 2 + Y ** 2

def CostFunction(X, Y):
    if (X==None or Y==None):
        return None
    else:
        return np.exp(np.sin(-np.sqrt(X ** 2 + Y ** 2)))
        #return X ** 2 + Y ** 2