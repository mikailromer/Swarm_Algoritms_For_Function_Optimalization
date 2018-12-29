import numpy as np
from matplotlib import pyplot  as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from time import sleep as Sleep
from mpl_toolkits.mplot3d.axes3d import get_test_data



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

def CreateSwarmOfFireflies(NumberOfFireflies,Xmin,Xmax,Ymin,Ymax,beta0):
    SwarmOfFireflies = []
    for index in range(NumberOfFireflies):
        X=round(np.random.uniform(Xmin,Xmax), 3)
        Y=round(np.random.uniform(Ymin, Ymax), 3)
        Point={"X":X,"Y":Y}
        SwarmOfFireflies.append(Firefly(Point,index,beta0))
    return SwarmOfFireflies

def CostFunction(X,Y):
    return X**2+Y**2

def FirefliesLigthIntensity(CostFunction):
    return 1/(CostFunction+0.000001)

def ComputeDistanceBeetweenTwoFireflies(Firefly_I,Firefly_J):
    X=Firefly_J.get_X()-Firefly_I.get_X()
    Y=Firefly_J.get_Y()-Firefly_I.get_Y()
    Rij=np.sqrt(X**2 + Y**2)
    return Rij

def AtractivenessFunction(beta0,Rij):
    result=beta0*np.exp(-1*Lambda*(Rij**2))
    return result

def GenerateRandomVector():
    uX = round(np.random.uniform(-0.15, 0.15), 3)
    uY = round(np.random.uniform(-0.15, 0.15), 3)
    RandomVector = {"uX": uX, "uY": uY}
    return RandomVector

def FindTheMostAtractiveFirefly(SwarmOfFireflies):
    IndexOfTheMostAtractiveFirefly=0
    for firefly in SwarmOfFireflies:
        if firefly.get_Z()<SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_Z():
            IndexOfTheMostAtractiveFirefly=firefly.get_index()

    return IndexOfTheMostAtractiveFirefly

def plot3DGraph(Xmin,Xmax,Ymin,Ymax,Zmin,Zmax,SwarmOfFireflies):
    fig=plt.figure()
    PositionsOfFirefliesIn_Xaxis=[]
    PositionsOfFirefliesIn_Yaxis = []
    PositionsOfFirefliesIn_Zaxis=[]
    for firefly in SwarmOfFireflies:
        PositionsOfFirefliesIn_Xaxis.append(firefly.get_X())
        PositionsOfFirefliesIn_Yaxis.append(firefly.get_Y())
        PositionsOfFirefliesIn_Zaxis.append(firefly.get_Z())

    ax = fig.add_subplot(1, 1, 1, projection='3d')
    X=np.arange(Xmin,Xmax,1)
    Y = np.arange(Ymin, Ymax, 1)
    X, Y = np.meshgrid(X, Y)
    Z=CostFunction(X,Y)
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    ax.scatter(PositionsOfFirefliesIn_Xaxis, PositionsOfFirefliesIn_Yaxis, PositionsOfFirefliesIn_Zaxis, c='r', marker='o')
    plt.show()
    plt.close('all')


if __name__ =='__main__':
    '''
        Set optimalization parameters, such as:
            λ -  absortion parameter
            β0 - maximal atractiveness
            
    '''
    Lambda=0.02
    Beta0=1
    NumberOfFireflies=20
    MaxGeneration=25
    '''
            Set dimentions of 3D plot, such as:
               Xmin,Xmax,Ymin,Ymax
               Zmin,Zmax - optionally

    '''
    Xmin=-20
    Xmax=20
    Ymin=-20
    Ymax=20
    Zmin=0
    Zmax=100
    Best=None
    #Fireflies initialization
    SwarmOfFireflies=CreateSwarmOfFireflies(NumberOfFireflies,Xmin,Xmax,Ymin,Ymax,Beta0)
    Generation=0
    while Generation<MaxGeneration:
        for i in range(NumberOfFireflies):
            for j in range(NumberOfFireflies):
                CostFunctionFor_Xi=CostFunction(SwarmOfFireflies[i].get_X(),SwarmOfFireflies[i].get_Y())
                fXi=FirefliesLigthIntensity(CostFunctionFor_Xi)
                CostFunctionFor_Xj=CostFunction(SwarmOfFireflies[j].get_X(),SwarmOfFireflies[j].get_Y())
                fXj=FirefliesLigthIntensity(CostFunctionFor_Xj)

                if fXj>fXi:
                    Rij=ComputeDistanceBeetweenTwoFireflies(SwarmOfFireflies[i],SwarmOfFireflies[j])
                    beta=AtractivenessFunction(Beta0,Rij)
                    SwarmOfFireflies[i].set_beta(beta)
                    ui=GenerateRandomVector()
                    IIczlonXi=beta*(SwarmOfFireflies[j].get_X()-SwarmOfFireflies[i].get_X())
                    IIczlonYi=beta*(SwarmOfFireflies[j].get_Y()-SwarmOfFireflies[i].get_Y())
                    Xi=SwarmOfFireflies[i].get_X()+beta*(SwarmOfFireflies[j].get_X()-SwarmOfFireflies[i].get_X())+ui["uX"]
                    Yi=SwarmOfFireflies[i].get_Y()+beta*(SwarmOfFireflies[j].get_Y()-SwarmOfFireflies[i].get_Y())+ui["uY"]
                    SwarmOfFireflies[i].set_Point(Xi,Yi)
                    SwarmOfFireflies[i].set_beta(beta)

                SwarmOfFireflies[i].set_Z(CostFunctionFor_Xi)
                SwarmOfFireflies[i].set_Z(CostFunctionFor_Xj)

        uk=GenerateRandomVector()
        IndexOfTheMostAtractiveFirefly=FindTheMostAtractiveFirefly(SwarmOfFireflies)
        TheMostAtractiveFirefly_X=SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_X()+uk["uX"]
        TheMostAtractiveFirefly_Y = SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_Y() + uk["uY"]

        SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].set_Point(TheMostAtractiveFirefly_X,TheMostAtractiveFirefly_Y)

        SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].set_Z(CostFunction(SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_X()\
                                                                            ,SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_Y()))
        Best=SwarmOfFireflies[IndexOfTheMostAtractiveFirefly]
        Generation=Generation+1
        plt.interactive(False)
        plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SwarmOfFireflies)


    print("Xmin: ",Best.get_X())
    print("Ymin: ",Best.get_Y())








