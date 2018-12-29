import numpy as np
from matplotlib import pyplot  as plt
from mpl_toolkits.mplot3d import axes3d
from CommonFunctions.CommonFunctions import CostFunctionForPlot

def plot3DGraph(Xmin,Xmax,Ymin,Ymax,Zmin,Zmax,SetOfObjects):
    fig=plt.figure()
    PositionsOfObjectsIn_Xaxis=[]
    PositionsOfObjectsIn_Yaxis = []
    PositionsOfObjectsIn_Zaxis=[]
    for firefly in SetOfObjects:
        PositionsOfObjectsIn_Xaxis.append(firefly.get_X())
        PositionsOfObjectsIn_Yaxis.append(firefly.get_Y())
        PositionsOfObjectsIn_Zaxis.append(firefly.get_Z())

    ax = fig.add_subplot(1, 1, 1, projection='3d')
    X=np.arange(Xmin,Xmax,1)
    Y = np.arange(Ymin, Ymax, 1)
    X, Y = np.meshgrid(X, Y)
    Z=CostFunctionForPlot(X,Y)
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    ax.scatter(PositionsOfObjectsIn_Xaxis, PositionsOfObjectsIn_Yaxis, PositionsOfObjectsIn_Zaxis, c='r', marker='o')
    plt.show()
    plt.close('all')