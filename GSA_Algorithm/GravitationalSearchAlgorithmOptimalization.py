import numpy as np
from matplotlib import pyplot  as plt
from CommonFunctions.CommonFunctions import CostFunction,CostFunctionForPlot, AdaptationFunction
from CommonFunctions.CommonFunctions import ComputeDistanceBeetweenTwoObjects
from Objects.Particle import Particle
from mpl_toolkits.mplot3d import axes3d
from PlotFunctions.Plot3DGraph import plot3DGraph
from PlotFunctions.DataForPlot import *
from PlotFunctions.CostFunctionGraph2D import CostFunctionGraph2D
from PlotFunctions.ContourPlot import ContourPlot
from CommonFunctions.CommonFunctions import collectListOfPoints
from Configs.ConfigDataForGsaAlgorithm import GSA_DataConfig as cf
from os import path,mkdir
import sys


if path.exists("results"):
    pass
else:
    mkdir("results")

def CreateSetOfParticles(NumberOfParticles, Xmin, Xmax, Ymin, Ymax,beta):
    SetOfParticles = []
    for index in range(NumberOfParticles):
        X = round(np.random.uniform(Xmin, Xmax), 3)
        Y = round(np.random.uniform(Ymin, Ymax), 3)
        SetOfParticles.append(Particle(X,Y,beta))
    return SetOfParticles

def ComputeGravitationalConstant(G0,t0,beta,t):
    if t is 0:
        return G0
    else:
        return G0*((t0/t)**beta)

def SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles):
    TheBestValue=SetOfParticles[0].get_AdaptationFunctionValue()
    TheWorstValue=SetOfParticles[0].get_AdaptationFunctionValue()
    IndexOfTheBestParticle=0
    IndexOfTheWorstParticle=0
    index=0
    if len(SetOfParticles)<=1:
        return TheBestValue, TheWorstValue, IndexOfTheBestParticle, IndexOfTheWorstParticle
    else:
        for Particle in SetOfParticles:
            if Particle.get_AdaptationFunctionValue()>TheBestValue:
                TheBestValue=Particle.get_AdaptationFunctionValue()
                IndexOfTheBestParticle=index
            if Particle.get_AdaptationFunctionValue()<TheWorstValue:
                TheWorstValue=Particle.get_AdaptationFunctionValue()
                IndexOfTheWorstParticle=index
            index=index+1
        return TheBestValue,TheWorstValue,IndexOfTheBestParticle,IndexOfTheWorstParticle




def ComputeGravityMassesForParticles(SetOfParticles,fBest,fWorst):
    for particle in SetOfParticles:
        fi=particle.get_AdaptationFunctionValue()
        Mi = GravityMass(fi, fBest, fWorst)
        particle.set_M(Mi)

def GravityMass(fi,fBest,fWorst):
    return 1000*((fi-fWorst)/(fBest-fWorst))

def ComputeInertialMassesOfParticles(SetOfParticles):
    SumOfGravityMasses=0
    for particle in SetOfParticles:
        SumOfGravityMasses=SumOfGravityMasses+particle.get_M()
    for particle in SetOfParticles:
        mi = particle.get_M() / SumOfGravityMasses
        particle.set_m(mi)



def ComputeNetForcesForParticles(SetOfParticles,G,epsilon):
    for Particle_I in SetOfParticles:
        if Particle_I.get_M()==0:
            Particle_I.set_Fg(None, None)
        else:
            FijX=0
            FijY=0
            alfa = round(np.random.uniform(0, 1), 3)
            for Particle_J in SetOfParticles:
                if Particle_J.get_M() != 0:
                    if Particle_J is not Particle_I:
                        Rij = ComputeDistanceBeetweenTwoObjects(Particle_I, Particle_J)
                        FijX = FijX + G * ((Particle_I.get_M() * Particle_J.get_M()) / (Rij + epsilon)) \
                               * (Particle_J.get_X() - Particle_I.get_X())
                        FijY = FijY + G * ((Particle_I.get_M() * Particle_J.get_M()) / (Rij + epsilon)) \
                               * (Particle_J.get_Y() - Particle_I.get_Y())

            Particle_I.set_Fg(alfa*FijX,alfa*FijY)


def ComputeAccelerationsForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        if Particle_I.get_m()==0:
            Particle_I.set_a(None, None)
        else:
            aix = Particle_I.get_Fgx() / Particle_I.get_m()
            aiy = Particle_I.get_Fgy() / Particle_I.get_m()
            Particle_I.set_a(aix, aiy)



def ComputeVelocityForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        if (Particle_I.get_ax()==None) and (Particle_I.get_ay()==None):
            Particle_I.set_V(None, None)
        else:
            alfa=round(np.random.uniform(0,1), 3)
            vix=alfa*Particle_I.get_Vx()+Particle_I.get_ax()
            viy=alfa*Particle_I.get_Vy()+Particle_I.get_ay()
            Particle_I.set_V(vix,viy)


def ComputeCordinatesForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        if (Particle_I.get_Vx()==None) and (Particle_I.get_Vy()==None):
            Particle_I.set_Point(Particle_I.get_X(), Particle_I.get_Y())
        else:
            x = Particle_I.get_X() + Particle_I.get_Vx()
            y = Particle_I.get_Y() + Particle_I.get_Vy()
            Particle_I.set_Point(x, y)

            if Particle_I.get_X() > Xmax:
                Particle_I.set_Point(Xmax, Particle_I.get_Y())

            if Particle_I.get_X() < Xmin:
                Particle_I.set_Point(Xmin, Particle_I.get_Y())

            if Particle_I.get_Y() > Ymax:
                Particle_I.set_Point(Particle_I.get_X(), Ymax)

            if Particle_I.get_Y() < Ymin:
                Particle_I.set_Point(Particle_I.get_X(), Ymin)



def ComputeAdaptationFunctionAndCostFunctionValues(SetOfParticles,beta):
    #self.__Z=CostFunction(X,Y)
    #self.__AdaptationFunctionValue = AdaptationFunction(self.get_Z(), beta)
    for particle in SetOfParticles:
        particle.AdaptationFunctionAndCostFunctionValueSet(particle.get_X(),particle.get_Y(),beta)

def plot3DprobeGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    X = np.arange(Xmin, Xmax, 1)
    Y = np.arange(Ymin, Ymax, 1)
    X, Y = np.meshgrid(X, Y)
    Z = np.exp(np.sin(-np.sqrt(X**2+Y**2)))
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    plt.show()
    plt.close('all')




if __name__ == '__main__':
    '''
        Set optimalization parameters, such as:
            λ -  absortion parameter
            β0 - maximal atractiveness

    '''


    '''
            Set dimentions of 3D plot, such as:
               Xmin,Xmax,Ymin,Ymax
               Zmin,Zmax - optionally

    '''

    BestParticle = None
    IndexOfTheBestParticle=None
    IndexOfTheWorstParticle=None
    # Fireflies initialization

    SetOfParticles = CreateSetOfParticles(cf.get_NumberOfParticles(), Xmin, Xmax, Ymin, Ymax,cf.get_beta())
    with open(path.join("results", "results.txt"), "w") as results:
        for trial in range(cf.get_trials()):
            t = 0
            tableOfPoints = []
            tableOfPoints.append(collectListOfPoints(SetOfParticles))
            while t < cf.get_totalTime() and len(SetOfParticles)>1:
                G = ComputeGravitationalConstant(cf.get_Gt0(), cf.get_t0(), cf.get_beta(), t)
                fBest, fWorst,IndexOfTheBestParticle,IndexOfTheWorstParticle = SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles)
                ComputeGravityMassesForParticles(SetOfParticles,fBest,fWorst)
                ComputeInertialMassesOfParticles(SetOfParticles)
                ComputeNetForcesForParticles(SetOfParticles,G,cf.get_epsilon())
                ComputeAccelerationsForParticles(SetOfParticles)
                ComputeVelocityForParticles(SetOfParticles)
                ComputeCordinatesForParticles(SetOfParticles)
                ComputeAdaptationFunctionAndCostFunctionValues(SetOfParticles,cf.get_beta())
                removedParticle=SetOfParticles.pop(IndexOfTheWorstParticle)
                fBest,fWorst,IndexOfTheBestParticle,IndexOfTheWorstParticle=\
                    SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles)

                if trial==0 and t==0:
                    BestParticle=SetOfParticles[IndexOfTheBestParticle]
                else:
                    if SetOfParticles[IndexOfTheBestParticle].get_Z()<BestParticle.get_Z():
                        BestParticle=SetOfParticles[IndexOfTheBestParticle]

                tableOfPoints.append(collectListOfPoints(SetOfParticles))
                sys.stdout.write("\r Time:%4d, BestFitness:%8f\n" % (t, BestParticle.get_Z()))
                t = t + 1
                results.write('Xmin: {0}  Ymin: {1}  Zmin: {2}\n'.format(BestParticle.get_X(),BestParticle.get_Y(),BestParticle.get_Z()))


        print('\nThe best minimum: {}\n'.format(BestParticle.get_Z()))
        print('For X: {0} Y: {1}\n'.format(BestParticle.get_X(), BestParticle.get_Y()))
        CostFunctionGraph2D(Zmin,Zmax,IndexOfTheBestParticle,tableOfPoints,cf.get_totalTime())
        ContourPlot(Xmin,Xmax,Ymin,Ymax,Zmin,Zmax,SetOfParticles,tableOfPoints)
        #plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SetOfParticles,tableOfPoints)