import numpy as np
import matplotlib.pyplot as plt
from Objects.Firefly import Firefly
from CommonFunctions.CommonFunctions import CostFunction,AtractivenessFunction
from CommonFunctions.CommonFunctions import ComputeDistanceBeetweenTwoObjects
from PlotFunctions.Plot3DGraph import plot3DGraph
from PlotFunctions.DataForPlot import *
from Configs.ConfigDataForFaAlgorithm import *



def CreateSwarmOfFireflies(NumberOfFireflies,Xmin,Xmax,Ymin,Ymax,beta0):
    SwarmOfFireflies = []
    for index in range(NumberOfFireflies):
        X=round(np.random.uniform(Xmin,Xmax), 3)
        Y=round(np.random.uniform(Ymin, Ymax), 3)
        Point={"X":X,"Y":Y}
        SwarmOfFireflies.append(Firefly(Point,index,beta0))
    return SwarmOfFireflies



def FirefliesLigthIntensity(CostFunction):
    return 1/(CostFunction+0.000001)



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




if __name__ =='__main__':

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
                    Rij=ComputeDistanceBeetweenTwoObjects(SwarmOfFireflies[i],SwarmOfFireflies[j])
                    beta=AtractivenessFunction(Beta0,Rij,Lambda)
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








