from Objects.BasicObject import BasicObject

class Firefly(BasicObject):
    def __init__(self,X,Y,index,beta0):
        BasicObject.__init__(self ,X ,Y )
        self.__index=index
        self.__beta=beta0

    def get_index(self):
        return self.__index

    def get_beta(self):
        return self.__beta

    def set_beta(self,beta):
        self.__beta=beta

 #   def set_Z(self):
  #      self.__Point["Z"]=CostFunction(self.get_X(),self.get_Y())

