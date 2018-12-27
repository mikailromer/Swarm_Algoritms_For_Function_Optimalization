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
    if X==None or Y==None:
        return None
    else:
        return X ** 2 + Y ** 2

def AdaptationFunction(CostFunction,beta):
    if CostFunction==None:
        return None
    else:
        result = -beta *CostFunction
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

def ComputeDistanceBeetweenTwoParticles(Particle_I, Particle_J):
    if ((Particle_I.get_X()==None and Particle_I.get_Y()==None) or (Particle_J.get_X()==None and Particle_J.get_Y()==None)):
        return None
    else:
        X = Particle_J.get_X() - Particle_I.get_X()
        Y = Particle_J.get_Y() - Particle_I.get_Y()
        Rij = np.sqrt(X ** 2 + Y ** 2)
        return Rij

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
                        Rij = ComputeDistanceBeetweenTwoParticles(Particle_I, Particle_J)
                        FijX = FijX + G * ((Particle_I.get_M() * Particle_J.get_M()) / (Rij + epsilon)) \
                               * (Particle_J.get_X() - Particle_I.get_X())
                        FijY = FijY + G * ((Particle_I.get_M() * Particle_J.get_M()) / (Rij + epsilon)) \
                               * (Particle_J.get_Y() - Particle_I.get_Y())

            Particle_I.set_Fg(alfa*FijX,alfa*FijY)
            print('o')

def ComputeAccelerationsForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        if Particle_I.get_m()==0:
            Particle_I.set_a(None, None)
        else:
            aix = Particle_I.get_Fgx() / Particle_I.get_m()
            aiy = Particle_I.get_Fgy() / Particle_I.get_m()
            Particle_I.set_a(aix, aiy)
            print('o')


def ComputeVelocityForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        if (Particle_I.get_ax()==None) and (Particle_I.get_ay()==None):
            Particle_I.set_V(None, None)
        else:
            alfa=round(np.random.uniform(0,1), 3)
            vix=alfa*Particle_I.get_Vx()+Particle_I.get_ax()
            viy=alfa*Particle_I.get_Vy()+Particle_I.get_ay()
            Particle_I.set_V(vix,viy)
            print('o')

def ComputeCordinatesForParticles(SetOfParticles):
    for Particle_I in SetOfParticles:
        if (Particle_I.get_Vx()==None) and (Particle_I.get_Vy()==None):
            Particle_I.set_Point(None, None)
        else:
            x = Particle_I.get_X() + Particle_I.get_Vx()
            y = Particle_I.get_Y() + Particle_I.get_Vy()
            Particle_I.set_Point(x, y)
            print('o')


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

    NumberOfParticles = 3
    TotalTime=20
    Gt0=0.0001
    t0=1
    beta=0.98
    epsilon=1000
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
            ComputeGravityMassesForParticles(SetOfParticles,fBest,fWorst)
            ComputeInertialMassesOfParticles(SetOfParticles)
            ComputeNetForcesForParticles(SetOfParticles,G,epsilon)
            ComputeAccelerationsForParticles(SetOfParticles)
            ComputeVelocityForParticles(SetOfParticles)
            Xprev = SetOfParticles[i].get_X()
            Yprev = SetOfParticles[i].get_Y()

            ComputeCordinatesForParticles(SetOfParticles)

            Mprev = SetOfParticles[i].get_M()
            prev_adapt_value = SetOfParticles[i].get_AdaptationFunctionValue()
            SetOfParticles[i].AdaptationFunctionAndCostFunctionValueSet\
                (SetOfParticles[i].get_X(),SetOfParticles[i].get_Y(),beta)
            adapt_value=SetOfParticles[i].get_AdaptationFunctionValue()

        '''
        Make function which eliminates unnecessary Particle
        '''

        fBest,fWorst=SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles,mode="Values")
        IndexOfTheBestParticle, IndexOfTheWorstParticle = SearchForTheBestAndTheWorstAdaptationFunctionValues(SetOfParticles,mode="Indexes")
        t = t + 1
    #    plt.interactive(False)
     #   plot3DGraph(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, SetOfParticles)

    print("Xmin: ", fBest.get_X())
    print("Ymin: ", fBest.get_Y())
