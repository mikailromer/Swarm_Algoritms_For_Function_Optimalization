from Objects.BasicObject import BasicObject
from CommonFunctions.CommonFunctions import *

class Particle(BasicObject):
    def __init__(self, X,Y,beta):
        BasicObject.__init__(self,X,Y)
        self.__AdaptationFunctionValue=AdaptationFunction(self.get_Z(),beta)
        self.__m=None
        self.__M=None
        self.__Fg={"Fgx":None,"Fgy":None}
        self.__a={"ax":None,"ay":None}
        self.__V={"vx":0,"vy":0}

    def get_m(self):
        return self.__m

    def get_M(self):
        return self.__M

    def get_Fgx(self):
        return self.__Fg["Fgx"]

    def get_Fgy(self):
        return self.__Fg["Fgy"]

    def get_ax(self):
        return self.__a["ax"]

    def get_ay(self):
        return self.__a["ay"]

    def get_Vx(self):
        return self.__V["vx"]

    def get_Vy(self):
        return self.__V["vy"]

    def get_AdaptationFunctionValue(self):
        return self.__AdaptationFunctionValue

    def AdaptationFunctionAndCostFunctionValueSet(self,X,Y,beta):
        self.set_Point(X,Y)
        self.__AdaptationFunctionValue = AdaptationFunction(self.get_Z(), beta)

    def set_a(self, ax,ay):
        self.__a={"ax": ax, "ay": ay}

    def set_M(self,M):
        self.__M=M

    def set_m(self,m):
        self.__m=m

    def set_Fg(self,Fgx,Fgy):
        self.__Fg={"Fgx":Fgx,"Fgy":Fgy}

    def set_V(self,Vx,Vy):
        self.__V={"vx":Vx,"vy":Vy}