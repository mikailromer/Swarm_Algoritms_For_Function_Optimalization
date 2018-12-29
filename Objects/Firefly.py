from Configs.CostFunction import CostFunction

class Firefly():
    def __init__(self,Point,index,beta0):
        self.__Point=Point
        self.__index=index
        self.__Z=CostFunction(self.get_X(),self.get_Y())
        self.__beta=beta0

    def get_X(self):
        return self.__Point["X"]

    def get_Y(self):
        return self.__Point["Y"]

    def get_Z(self):
        return self.__Z

    def get_index(self):
        return self.__index

    def get_beta(self):
        return self.__beta

    def set_Z(self,CostFunctionValue):
        self.__Z=CostFunctionValue

    def set_Point(self,X,Y):
        self.__Point={"X":X,"Y":Y}

    def set_X(self,X):
        self.__Point["X"]=X

    def set_Y(self,Y):
        self.__Point["Y"]=Y

    def set_beta(self,beta):
        self.__beta=beta