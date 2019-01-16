from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from PlotFunctions.Plot3DGraph import parsePointsTraceForObject
import numpy as np
from CommonFunctions.CommonFunctions import CostFunctionForPlot

def ContourPlot(Xmin ,Xmax ,Ymin ,Ymax ,Zmin ,Zmax ,SetOfObjects , TableOfPoints):
    fig=plt.figure()
    X=np.arange(Xmin,Xmax,1)
    Y = np.arange(Ymin, Ymax, 1)
    X, Y = np.meshgrid(X, Y)
    Z_domain=np.arange(Zmin,Zmax,50)
    Z=CostFunctionForPlot(X,Y)
    CS = plt.contour(X, Y, Z, Z_domain)
    plt.clabel(CS, inline=True, fontsize=10)

    ax = fig.add_subplot(111)

    for ObjectIndex in range(len(SetOfObjects)):
        ObjectTrace_X, ObjectTrace_Y= parsePointsTraceForObject(ObjectIndex, TableOfPoints)
        r = np.array(ObjectTrace_X)
        s = np.array(ObjectTrace_Y)
        line = Line2D(r, s)
        ax.add_line(line)
        plt.plot(r, s, label="Cost function for the best object.")

    plt.show()
