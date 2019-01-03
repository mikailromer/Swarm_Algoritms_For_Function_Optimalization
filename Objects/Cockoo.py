import numpy as np
import math
from Configs.ConfigDataForCsAlgorithm import CS_DataConfig as cf
from CommonFunctions.CommonFunctions import CostFunction





class Cockoo:
    def __init__(self,Point):
        self.__Point=Point
        self.__Z =CostFunction(self.__Point["X"],self.__Point["Y"])

    def get_X(self):
        return self.__Point["X"]

    def get_Y(self):
        return self.__Point["Y"]

    def set_Point(self, X, Y):
        self.__Point = {"X": X, "Y": Y}

    def get_Z(self):
        return self.__Z

    def set_Z(self, X, Y):
        self.__Z = CostFunction(self.__Point["X"],self.__Point["Y"])

    def print_info(self,i):
        print("id:","{0:3d}".format(i),
              "|| fitness:",str(self.__fitness).rjust(14," "),
              "|| position:",np.round(self.__position,decimals=4))




