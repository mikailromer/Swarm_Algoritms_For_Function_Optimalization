from CommonFunctions.CommonFunctions import CostFunction
from PlotFunctions.DataForPlot import *

class BasicObject(object):
    def __init__(self, X, Y):
        self.__Point = {"X": X, "Y": Y, "Z": CostFunction(X, Y)}

    def get_X(self):
        return self.__Point["X"]

    def get_Y(self):
        return self.__Point["Y"]

    def get_Z(self):
        return self.__Point["Z"]

    def get_Point(self):
        return self.__Point

    def set_Point(self, X, Y):
        self.__Point = {"X": X, "Y": Y, "Z": CostFunction(X, Y)}

        if self.get_X() > Xmax:
            self.__Point = {"X": Xmax, "Y": Y, "Z": CostFunction(Xmax, Y)}

        if self.get_X() < Xmin:
            self.__Point = {"X": Xmin, "Y": Y, "Z": CostFunction(Xmin, Y)}

        if self.get_Y() > Ymax:
            self.__Point = {"X": X, "Y": Ymax, "Z": CostFunction(X, Ymax)}

        if self.get_Y() < Ymin:
            self.__Point = {"X": X, "Y": Ymin, "Z": CostFunction(X, Ymin)}



