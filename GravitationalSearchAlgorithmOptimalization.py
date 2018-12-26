import numpy as np
from matplotlib import pyplot  as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from time import sleep as Sleep
from mpl_toolkits.mplot3d.axes3d import get_test_data


class Particle():
    def __init__(self, Point,beta):
        self.__Point = Point
        self.__Z = CostFunction(self.get_X(), self.get_Y())
        self.__AdaptationFunctionValue=AdaptationFunction(self.get_Z(),beta)
        self.__m=None
        self.__M=None
        self.__Fg={"Fgx":None,"Fgy":None}
        self.__a={"ax":None,"ay":None}
        self.__V={"vx":0,"vy":0}


    def get_X(self):
        return self.__Point["X"]

    def get_Y(self):
        return self.__Point["Y"]

    def get_Z(self):
        return self.__Z

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
        self.__Z=CostFunction(X,Y)
        self.__AdaptationFunctionValue = AdaptationFunction(self.get_Z(), beta)


    def set_Z(self, CostFunctionValue):
        self.__Z = CostFunctionValue

    def set_Point(self, X, Y):
        self.__Point = {"X": X, "Y": Y}

    def set_X(self, X):
        self.__Point["X"] = X

    def set_Y(self, Y):
        self.__Point["Y"] = Y

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



def CreateSetOfParticles(NumberOfParticles, Xmin, Xmax, Ymin, Ymax,beta):
    SetOfParticles = []
    for index in range(NumberOfParticles):
        X = round(np.random.uniform(Xmin, Xmax), 3)
        Y = round(np.random.uniform(Ymin, Ymax), 3)
        Point = {"X": X, "Y": Y}
        SetOfParticles.append(Particle(Point,beta))
    return SetOfParticles

def ComputeGravitationalConstant(G0,t0,beta,t):
    if t is 0:
        return G0
    else:
        return G0*((t0/t)**beta)


def CostFunction(X, Y):
    return X ** 2 + Y ** 2

def AdaptationFunction(CostFunction,beta):
    result = beta * np.exp(-CostFunction)
    return result

def SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles,mode="Values"):
    TheBestValue=SetOfParticles[0].get_AdaptationFunctionValue()
    TheWorstValue=SetOfParticles[0].get_AdaptationFunctionValue()
    IndexOfTheBestParticle=None
    IndexOfTheWorstParticle=None
    index=0
    for Particle in SetOfParticles:
        if Particle.get_AdaptationFunctionValue()>TheBestValue:
            TheBestValue=Particle.get_AdaptationFunctionValue()
            IndexOfTheBestParticle=index
        if Particle.get_AdaptationFunctionValue()<TheWorstValue:
            TheWorstValue=Particle.get_AdaptationFunctionValue()
            IndexOfTheWorstParticle=index
        index=index+1
    if mode=="Indexes":
        return IndexOfTheBestParticle, IndexOfTheWorstParticle
    elif mode=="Values":
        return TheBestValue, TheWorstValue,
    else:
        raise Exception("Unknown mode value!!!")

def GravityMass(fi,fBest,fWorst):
    return ((fi-fWorst)/(fBest-fWorst))

def InertialMass(Mi,SetOfParticles):
    SumOfGravityMasses=0
    for particle in SetOfParticles:
        SumOfGravityMasses=SumOfGravityMasses+particle.get_M()
    mi=Mi/SumOfGravityMasses
    return mi

def ComputeDistanceBeetweenTwoParticles(Particle_I, Particle_J):
    X = Particle_J.get_X() - Particle_I.get_X()
    Y = Particle_J.get_Y() - Particle_I.get_Y()
    Rij = np.sqrt(X ** 2 + Y ** 2)
    return Rij

def ComputeNetForcesForParticles(SetOfParticles,G,epsilon):
    for Particle_I in SetOfParticles:
        FijX=0
        FijY=0
        alfa = round(np.random.uniform(0, 1), 3)
        for Particle_J in SetOfParticles:
            Rij=ComputeDistanceBeetweenTwoParticles(Particle_I,Particle_J)
            FijX=FijX+G*((Particle_I.get_M()*Particle_J.get_M())/(Rij*epsilon))\
                 *(Particle_J.get_X()-Particle_I.get_X())
            FijY=FijY+G*((Particle_I.get_M()*Particle_J.get_M())/(Rij*epsilon))\
                 *(Particle_J.get_Y()-Particle_I.get_Y())
        Particle_I.set_Fg(alfa*FijX,alfa*FijY)

def ComputeAccelerationsForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        aix=Particle_I.get_Fgx()/Particle_I.get_m()
        aiy=Particle_I.get_Fgy()/Particle_I.get_m()
        Particle_I.set_a(aix,aiy)

def ComputeVelocityForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        alfa=round(np.random.uniform(0,1), 3)
        vix=alfa*Particle_I.get_Vx()+Particle_I.get_ax()
        viy=alfa*Particle_I.get_Vy()+Particle_I.get_ay()
        Particle_I.set_V(vix,viy)

def ComputeCordinatesForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        x=Particle_I.get_X()+Particle_I.get_Vx
        y=Particle_I.get_Y()+Particle_I.get_Vy
        Particle_I.set_Point(x,y)

def plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SetOfParticles):
    fig = plt.figure()
    PositionsOfParticlesIn_Xaxis = []
    PositionsOfParticlesIn_Yaxis = []
    PositionsOfParticlesIn_Zaxis = []
    for particle in SetOfParticles:
        PositionsOfParticlesIn_Xaxis.append(particle.get_X())
        PositionsOfParticlesIn_Yaxis.append(particle.get_Y())
        PositionsOfParticlesIn_Zaxis.append(particle.get_Z())

    ax = fig.add_subplot(1, 1, 1, projection='3d')
    X = np.arange(Xmin, Xmax, 1)
    Y = np.arange(Ymin, Ymax, 1)
    X, Y = np.meshgrid(X, Y)
    Z = CostFunction(X, Y)
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    ax.scatter(PositionsOfParticlesIn_Xaxis, PositionsOfParticlesIn_Yaxis, PositionsOfParticlesIn_Zaxis, c='r',
               marker='o')
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    '''
        Set optimalization parameters, such as:
            λ -  absortion parameter
            β0 - maximal atractiveness

    '''

    NumberOfParticles = 20
    TotalTime=20
    Gt0=10000
    t0=1
    beta=0.98
    epsilon=10
    '''
            Set dimentions of 3D plot, such as:
               Xmin,Xmax,Ymin,Ymax
               Zmin,Zmax - optionally

    '''
    Xmin = -20
    Xmax = 20
    Ymin = -20
    Ymax = 20
    Zmin = 0
    Zmax = 100
    BestParticle = None
    IndexOfTheBestParticle=None
    IndexOfTheWorstParticle=None
    # Fireflies initialization
    SetOfParticles = CreateSetOfParticles(NumberOfParticles, Xmin, Xmax, Ymin, Ymax,beta)
    t = 0
    while t < TotalTime and len(SetOfParticles)>1:
        G = ComputeGravitationalConstant(Gt0, t0, beta, t)
        for i in range(NumberOfParticles):
            fBest, fWorst = SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles,mode="Values")
            fi=SetOfParticles[i].get_AdaptationFunctionValue()
            Mi=GravityMass(fi,fBest,fWorst)
            SetOfParticles[i].set_M(Mi)
            mi=InertialMass(Mi,SetOfParticles)
            SetOfParticles[i].set_m(mi)
            ComputeNetForcesForParticles(SetOfParticles,G,epsilon)
            ComputeAccelerationsForParticles(SetOfParticles)
            ComputeCordinatesForParticles(SetOfParticles)
            SetOfParticles[i].AdaptationFunctionAndCostFunctionValueSet\
                (SetOfParticles[i].get_X(),SetOfParticles[i].get_Y(),beta)

        IndexOfTheBestParticle, IndexOfTheWorstParticle = SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles,mode="Indexes")
        t = t + 1
        plt.interactive(False)
        plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SetOfParticles)

    print("Xmin: ", fBest.get_X())
    print("Ymin: ", fBest.get_Y())
