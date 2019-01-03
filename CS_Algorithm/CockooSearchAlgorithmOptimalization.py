import numpy as np
import os
import sys
from random import SystemRandom
import csv
from Configs.ConfigDataForCsAlgorithm import CS_DataConfig as cf
from Objects.Cockoo import Cockoo
from PlotFunctions.DataForPlot import *
from PlotFunctions.Plot3DGraph import plot3DGraph



if os.path.exists("results"):
    pass
else:
    os.mkdir("results")

results = open("results" + os.sep + "results.csv", "w")
results_writer = csv.writer(results, lineterminator="\n")

def CreateSetOfCockoos(PopulationSize,Xmin,Xmax,Ymin,Ymax):
    SetOfCockoos = []
    for index in range(PopulationSize):
        X=round(np.random.uniform(Xmin,Xmax), 3)
        Y=round(np.random.uniform(Ymin, Ymax), 3)
        Point={"X":X,"Y":Y}
        SetOfCockoos.append(Cockoo(Point))
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
    Cockoo.set_Z(X,Y)

    # Simple Boundary Rule
    if Cockoo.get_X() > Xmax:
        Cockoo.set_Point(Xmax, Cockoo.get_Y())

    if Cockoo.get_X() < Xmin:
        Cockoo.set_Point(Xmin, Cockoo.get_Y())

    if Cockoo.get_Y() > Ymax:
        Cockoo.set_Point(Cockoo.get_X(), Ymax)

    if Cockoo.get_Y() < Ymin:
        Cockoo.set_Point(Cockoo.get_X(), Ymin)



def abandon(cockoo):
    # abandon some variables
    X = round(np.random.uniform(Xmin, Xmax), 3)
    Y = round(np.random.uniform(Ymin, Ymax), 3)
    cockoo.set_Point(X,Y)


def main():
    for trial in range(cf.get_trial()):
        randObject = SystemRandom()
        np.random.seed(randObject.randint(0,1000))

        SetOfResults = [] # fitness list
        SetOfCockoos = []
        results_list = []
        BestFitness=0
        """Generate Initial Population"""
        SetOfCockoos=CreateSetOfCockoos(cf.get_population_size(),Xmin,Xmax,Ymin,Ymax)

        """Sort List"""
        SetOfCockoos = sorted(SetOfCockoos, key=lambda ID: ID.get_Z())

        """Find Initial Best"""
        BestPositionInXaxis = SetOfCockoos[0].get_X()
        BestPositionInYaxis=SetOfCockoos[0].get_Y()
        BestFitness = SetOfCockoos[0].get_Z()

        """↓↓↓Main Loop↓↓↓"""
        for iteration in range(cf.get_iteration()):

            """Generate New Solutions"""
            for i in range(len(SetOfCockoos)):
                get_cuckoo(SetOfCockoos[i])
                SetOfCockoos[i].set_Z(SetOfCockoos[i].get_X(),SetOfCockoos[i].get_Y())

                """random choice (say j)"""
                j = np.random.randint(low=0, high=cf.get_population_size())
                while j == i: #random id[say j] ≠ i
                    j = np.random.randint(0, cf.get_population_size())

                # for minimize problem
                if(SetOfCockoos[i].get_Z() < SetOfCockoos[j].get_Z()):

                    SetOfCockoos[j].set_Point(SetOfCockoos[i].get_X(),SetOfCockoos[i].get_Y())
                    SetOfCockoos[j].set_Z(SetOfCockoos[i].get_X(),SetOfCockoos[i].get_Y())

            """Sort (to Keep Best)"""
            SetOfCockoos = sorted(SetOfCockoos, key=lambda ID: ID.get_Z())

            """Abandon Solutions (exclude the best)"""
            NumberOfTheWorstCockoos=round(cf.get_Pa()*cf.get_population_size())
            IndexesOfTheWorstSolutions=findTheWorstSolutions(SetOfCockoos,NumberOfTheWorstCockoos)
            for a in IndexesOfTheWorstSolutions:
                abandon(SetOfCockoos[a])
                SetOfCockoos[a].set_Z(SetOfCockoos[a].get_X(),SetOfCockoos[a].get_Y())

            """Sort to Find the Best"""
            SetOfCockoos = sorted(SetOfCockoos, key=lambda ID: ID.get_Z())

            if SetOfCockoos[0].get_Z() < BestFitness:
                BestFitness = SetOfCockoos[0].get_Z()
                BestPositionInXaxis = SetOfCockoos[0].get_X()
                BestPositionInYaxis = SetOfCockoos[0].get_Y()

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, BestFitness:%.4f" % (trial , iteration, BestFitness))

            results_list.append(str(BestFitness))

        results_writer.writerow(results_list)
        plot3DGraph(Xmin,Xmax,Ymin,Ymax,Zmin,Zmax,SetOfCockoos)

if __name__ == '__main__':
    main()
    results.close()