import numpy as np
import matplotlib.pyplot as plt
from Objects.Firefly import Firefly
from CommonFunctions.CommonFunctions import CostFunction,AtractivenessFunction
from CommonFunctions.CommonFunctions import ComputeDistanceBeetweenTwoObjects
from PlotFunctions.Plot3DGraph import plot3DGraph
from PlotFunctions.DataForPlot import *
from Configs.ConfigDataForFaAlgorithm import FA_DataConfig as cf
from os import path,mkdir
import sys

if path.exists("results"):
    pass
else:
    mkdir("results")


def CreateSwarmOfFireflies(NumberOfFireflies,Xmin,Xmax,Ymin,Ymax,beta0):
    SwarmOfFireflies = []
    for index in range(NumberOfFireflies):
        X=round(np.random.uniform(Xmin,Xmax), 3)
        Y=round(np.random.uniform(Ymin, Ymax), 3)
        SwarmOfFireflies.append(Firefly(X,Y,index ,beta0 ))
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
    with open(path.join("results", "results.txt"), "w") as results:
        Best=None
        #Fireflies initialization
        SwarmOfFireflies=None
        Generation=0
        for Generation in range(cf.get_numberOfGenerations()):
            SwarmOfFireflies = CreateSwarmOfFireflies(cf.get_NumberOfFireflies(), Xmin, Xmax, Ymin, Ymax, cf.get_beta0())
            for iteration in range(cf.get_iteration()):
                for i in range(cf.get_NumberOfFireflies()):
                    for j in range(cf.get_NumberOfFireflies()):
                        CostFunctionFor_Xi=CostFunction(SwarmOfFireflies[i].get_X(),SwarmOfFireflies[i].get_Y())
                        fXi=FirefliesLigthIntensity(CostFunctionFor_Xi)
                        CostFunctionFor_Xj=CostFunction(SwarmOfFireflies[j].get_X(),SwarmOfFireflies[j].get_Y())
                        fXj=FirefliesLigthIntensity(CostFunctionFor_Xj)

                        if fXj>fXi:
                            Rij=ComputeDistanceBeetweenTwoObjects(SwarmOfFireflies[i],SwarmOfFireflies[j])
                            beta=AtractivenessFunction(cf.get_beta0(),Rij,cf.get_Lambda())
                            SwarmOfFireflies[i].set_beta(beta)
                            ui=GenerateRandomVector()
                            IIczlonXi=beta*(SwarmOfFireflies[j].get_X()-SwarmOfFireflies[i].get_X())
                            IIczlonYi=beta*(SwarmOfFireflies[j].get_Y()-SwarmOfFireflies[i].get_Y())
                            Xi=SwarmOfFireflies[i].get_X()+beta*(SwarmOfFireflies[j].get_X()-SwarmOfFireflies[i].get_X())+ui["uX"]
                            Yi=SwarmOfFireflies[i].get_Y()+beta*(SwarmOfFireflies[j].get_Y()-SwarmOfFireflies[i].get_Y())+ui["uY"]
                            SwarmOfFireflies[i].set_Point(Xi,Yi)
                            SwarmOfFireflies[i].set_beta(beta)

                uk=GenerateRandomVector()
                IndexOfTheMostAtractiveFirefly=FindTheMostAtractiveFirefly(SwarmOfFireflies)
                TheMostAtractiveFirefly_X=SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_X()+uk["uX"]
                TheMostAtractiveFirefly_Y = SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_Y() + uk["uY"]
                SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].set_Point(TheMostAtractiveFirefly_X,TheMostAtractiveFirefly_Y)
                if Generation==0:
                    Best = SwarmOfFireflies[IndexOfTheMostAtractiveFirefly]

                if SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_Z()<Best.get_Z():
                    Best=SwarmOfFireflies[IndexOfTheMostAtractiveFirefly]

                sys.stdout.write("\r Trial:%3d , Iteration:%4d, BestFitness:%.10f" % (Generation, iteration, SwarmOfFireflies[IndexOfTheMostAtractiveFirefly].get_Z()))
                print('\n')

            results.write('Generation: {0}  Xmin: {1}  Ymin: {2}  Zmin: {3}\n'.format(Generation,Best.get_X(),Best.get_Y(),Best.get_Z()))
            Generation=Generation+1


        plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SwarmOfFireflies)
        print('The best minimum: {}\n'.format(Best.get_Z()))
        print('For X: {0} Y: {1}\n'.format(Best.get_X(), Best.get_Y()))








