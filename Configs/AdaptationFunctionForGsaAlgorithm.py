
def AdaptationFunction(CostFunction,beta):
    if CostFunction==None:
        return None
    else:
        result = -beta *CostFunction
        return result