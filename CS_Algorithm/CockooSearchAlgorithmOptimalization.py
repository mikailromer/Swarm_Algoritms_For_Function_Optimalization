import numpy as np
import sys
from random import SystemRandom
from Configs.ConfigDataForCsAlgorithm import CS_DataConfig as cf
from Objects.Cockoo import Cockoo
from PlotFunctions.DataForPlot import *
from PlotFunctions.CostFunctionGraph2D import CostFunctionGraph2D
from PlotFunctions.ContourPlot import ContourPlot
from CommonFunctions.CommonFunctions import collectListOfPoints
from os import path, mkdir



if path.exists("results"):
    pass
else:
    mkdir("results")

def CreateSetOfCockoos(PopulationSize,Xmin,Xmax,Ymin,Ymax):
    SetOfCockoos = []
    for index in range(PopulationSize):
        X=round(np.random.uniform(Xmin,Xmax), 3)
        Y=round(np.random.uniform(Ymin, Ymax), 3)
        SetOfCockoos.append(Cockoo(X,Y))
    return SetOfCockoos


def levy_flight(Lambda):
    # generate step from levy distribution
    randObject=SystemRandom()
    np.random.seed(randObject.randint(0,1000))
    sigma1 = np.power((np.math.gamma(1 + Lambda) * np.sin((np.pi * Lambda) / 2)) \
                      / np.math.gamma((1 + Lambda) / 2) * np.power(2, (Lambda - 1) / 2), 1 / Lambda)
    sigma2 = 1
    u = np.random.normal(0, sigma1, size=cf.get_dimension())
    v = np.random.normal(0, sigma2, size=cf.get_dimension())
    step = u / np.power(np.fabs(v), 1 / Lambda)

    return step

def checkElementInTheListOfCockoos(index,ListOfTheWorstSolutions):
    if len(ListOfTheWorstSolutions)==0:
        return False
    else:
        Condition=False
        for i in range(len(ListOfTheWorstSolutions)):
            if(ListOfTheWorstSolutions[i]==index):
                return True

        return False

def findTheWorstSolutions(SetOfCockoos,NumberOfTheWorstCockoos):
    IndexesOfTheWorstSolutions=[]
    ListOfCockoos=SetOfCockoos
    if NumberOfTheWorstCockoos==0:
        return None
    else:
        for i in range(NumberOfTheWorstCockoos):
            IndexOfTheWorstCockoo = 0
            TheWorstSolution=ListOfCockoos[0].get_Z()
            for j in range(len(ListOfCockoos)):
                if checkElementInTheListOfCockoos(j,ListOfCockoos)==False:
                    if ListOfCockoos[j].get_Z()<TheWorstSolution:
                        TheWorstSolution=ListOfCockoos[j].get_Z()
                        IndexOfTheWorstCockoo=j

            IndexesOfTheWorstSolutions.append(IndexOfTheWorstCockoo)

    return IndexesOfTheWorstSolutions

def get_cuckoo(Cockoo):
    step_size = cf.get_stepsize() * levy_flight(cf.get_lambda())

    # Update position
    X=Cockoo.get_X()+step_size
    Y=Cockoo.get_Y()+step_size

    Cockoo.set_Point(X,Y)
    # Simple Boundary Rule
    if Cockoo.get_X() > Xmax:
        raise Exception("cos")
        Cockoo.set_Point(Xmax, Cockoo.get_Y())

    if Cockoo.get_X() < Xmin:
        raise Exception("coks")
        Cockoo.set_Point(Xmin, Cockoo.get_Y())

    if Cockoo.get_Y() > Ymax:
        raise Exception("caaaos")
        Cockoo.set_Point(Cockoo.get_X(), Ymax)

    if Cockoo.get_Y() < Ymin:
        raise Exception("aaassadcos")
        Cockoo.set_Point(Cockoo.get_X(), Ymin)



def abandon(cockoo):
    # abandon some variables
    X = round(np.random.uniform(Xmin, Xmax), 3)
    Y = round(np.random.uniform(Ymin, Ymax), 3)
    cockoo.set_Point(X,Y)


if __name__ == '__main__':
    with open(path.join("results", "results.txt"), "w") as results:
        SetOfResults = []  # fitness list
        SetOfCockoos = []
        TheBestCockoo=None
        for trial in range(cf.get_trial()):
            BestFitness = 0
            BestPositionInXaxis = None
            BestPositionInYaxis = None
            writtenList=[]
            tableOfPoints = []
            randObject = SystemRandom()
            np.random.seed(randObject.randint(0,1000))
            """Generate Initial Population"""
            SetOfCockoos=CreateSetOfCockoos(cf.get_population_size(),Xmin,Xmax,Ymin,Ymax)

            """Sort List"""
            SetOfCockoos = sorted(SetOfCockoos, key=lambda ID: ID.get_Z())
            if trial==0:
                TheBestCockoo=SetOfCockoos[0]

            """Find Initial Best"""
            BestPositionInXaxis = SetOfCockoos[0].get_X()
            BestPositionInYaxis=SetOfCockoos[0].get_Y()
            BestFitness = SetOfCockoos[0].get_Z()
            tableOfPoints.append(collectListOfPoints(SetOfCockoos))
            """↓↓↓Main Loop↓↓↓"""
            for iteration in range(cf.get_iteration()):

                """Generate New Solutions"""
                for i in range(len(SetOfCockoos)):
                    get_cuckoo(SetOfCockoos[i])
                    """random choice (say j)"""
                    j = np.random.randint(low=0, high=cf.get_population_size())
                    while j == i: #random id[say j] ≠ i
                        j = np.random.randint(0, cf.get_population_size())

                    # for minimize problem
                    if(SetOfCockoos[i].get_Z() < SetOfCockoos[j].get_Z()):

                        SetOfCockoos[j].set_Point(SetOfCockoos[i].get_X(),SetOfCockoos[i].get_Y())

                """Sort (to Keep Best)"""
                SetOfCockoos = sorted(SetOfCockoos, key=lambda ID: ID.get_Z())

                """Abandon Solutions (exclude the best)"""
                NumberOfTheWorstCockoos=round(cf.get_Pa()*cf.get_population_size())
                IndexesOfTheWorstSolutions=findTheWorstSolutions(SetOfCockoos,NumberOfTheWorstCockoos)
                for a in IndexesOfTheWorstSolutions:
                    abandon(SetOfCockoos[a])

                """Sort to Find the Best"""
                SetOfCockoos = sorted(SetOfCockoos, key=lambda ID: ID.get_Z())
                if SetOfCockoos[0].get_Z()<TheBestCockoo.get_Z():
                    TheBestCockoo=SetOfCockoos[0]

                if SetOfCockoos[0].get_Z() < BestFitness:
                    BestFitness = SetOfCockoos[0].get_Z()
                    BestPositionInXaxis = SetOfCockoos[0].get_X()
                    BestPositionInYaxis = SetOfCockoos[0].get_Y()

                tableOfPoints.append(collectListOfPoints(SetOfCockoos))
                sys.stdout.write("\r Iteration:%7d, BestFitness:%.4f" %( iteration, SetOfCockoos[0].get_Z()))
                results.write('Xmin: {0}  Ymin: {1}  Zmin: {2}\n'.format(SetOfCockoos[0].get_X(),SetOfCockoos[0].get_Y(),SetOfCockoos[0]))
                print('\n')

        print('The best minimum: {}\n'.format(TheBestCockoo.get_Z()))
        print('For X: {0} Y: {1}\n'.format(TheBestCockoo.get_X(),TheBestCockoo.get_Y()))
        CostFunctionGraph2D(Zmin,Zmax,0,tableOfPoints,cf.get_iteration())
        ContourPlot(Xmin,Xmax,Ymin,Ymax,Zmin,Zmax,SetOfCockoos,tableOfPoints)
        #plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SetOfCockoos,tableOfPoints)

