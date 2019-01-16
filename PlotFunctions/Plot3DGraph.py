import numpy as np
from matplotlib import pyplot  as plt
from mpl_toolkits.mplot3d import axes3d
from CommonFunctions.CommonFunctions import CostFunctionForPlot
from matplotlib import cm


def plot3DGraph(Xmin,Xmax,Ymin,Ymax,Zmin,Zmax,SetOfObjects,TableOfPoints):
    fig=plt.figure()

    X=np.arange(Xmin,Xmax,1)
    Y = np.arange(Ymin, Ymax, 1)
    X, Y = np.meshgrid(X, Y)
    Z=CostFunctionForPlot(X,Y)

    norm = plt.Normalize(Z.min(), Z.max())
    colors = cm.viridis(norm(Z))
    rcount, ccount, _ = colors.shape

    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount,
                           facecolors=colors, shade=False)
    surf.set_facecolor((0, 0, 0, 0))
    ax2 = plt.gca(projection="3d")
    for ObjectIndex in range(len(SetOfObjects)):
        ObjectTrace_X,ObjectTrace_Y,ObjectTrace_Z=parsePointsTraceForObject(ObjectIndex,TableOfPoints)
        r=np.array(ObjectTrace_X)
        s=np.array(ObjectTrace_Y)
        t=np.array(ObjectTrace_Z)
        ax2.scatter(r, s, zs=t, c='r', s=4)
        ax2.plot3D(r, s, ObjectTrace_Z, label='Trace {}'.format(ObjectIndex+1))
        
    plt.title('Cost function optimalization.')
    plt.legend()
    plt.show()
    plt.close('all')

def parsePointsTraceForObject(index,TableOfPoints, mode='XY'):
    PositionsOfObjectIn_Xaxis=[]
    PositionsOfObjectIn_Yaxis = []
    PositionsOfObjectIn_Zaxis = []

    for row in TableOfPoints:
        if mode == 'XY':
            PositionsOfObjectIn_Xaxis.append(row[index]["X"])
            PositionsOfObjectIn_Yaxis.append(row[index]["Y"])
        elif mode=='Z':
            PositionsOfObjectIn_Zaxis.append(row[index]["Z"])
    if mode=='Z':
        return PositionsOfObjectIn_Zaxis

    return PositionsOfObjectIn_Xaxis,PositionsOfObjectIn_Yaxis
