import numpy as np

def ComputeDistanceBeetweenTwoObjects(Object_I, Object_J):
    if ((Object_I.get_X()==None and Object_I.get_Y()==None) or (Object_J.get_X()==None and Object_J.get_Y()==None)):
        return None
    else:
        X = Object_J.get_X() - Object_I.get_X()
        Y = Object_J.get_Y() - Object_I.get_Y()
        Rij = np.sqrt(X ** 2 + Y ** 2)
        return Rij

def AdaptationFunction(CostFunction,beta):
    if CostFunction==None:
        return None
    else:
        result = -beta *CostFunction
        return result

def AtractivenessFunction(beta0,Rij,Lambda):
    result=beta0*np.exp(-1*Lambda*(Rij**2))
    return result

def CostFunctionForPlot(X, Y):
     #return np.exp(np.sin(-np.sqrt(X**2+Y**2)))
     return X ** 2 + Y ** 2
     #return 1000*np.sin(X + np.log10(np.fabs(X) + 0.00001)) + X ** 2 + Y ** 2

def CostFunction(X, Y):
    if (X==None or Y==None):
        return None
    else:
        #return np.exp(np.sin(-np.sqrt(X ** 2 + Y ** 2)))
        #return 1000*np.sin(X+np.log10(np.fabs(X)+0.00001))+X**2+Y**2
        return X ** 2 + Y ** 2