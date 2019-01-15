from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from PlotFunctions.Plot3DGraph import parsePointsTraceForObject
import numpy as np


def CostFunctionGraph2D(Zmin, Zmax, BestObjectIndex,tableOfPoints, iterations):
    fig=plt.figure()
    ax = fig.add_subplot(111)
    iterations=iterations+1

    CostFunctionPoints = parsePointsTraceForObject(BestObjectIndex, tableOfPoints,mode='Z')
    MeanValuePoints=[]
    IterationList=[]
    for i in range(iterations):
        IterationList.append(i)

    line = Line2D(IterationList, CostFunctionPoints)
    ax.add_line(line)
    plt.plot(IterationList,CostFunctionPoints)
    ax.axis([0, iterations, Zmin, Zmax])

    for row in tableOfPoints:
        CostFunctionValues=[]
        for index in range(len(row)):
            CostFunctionValues.append(row[index]["Z"])
        MeanValuePoints.append(np.mean(np.array(CostFunctionValues)))

    ax2 = fig.add_subplot(111)
    line = Line2D(IterationList, MeanValuePoints)
    ax2.add_line(line)
    plt.plot(IterationList,MeanValuePoints)
    plt.xlabel('Iterations')
    plt.ylabel('Cost Function')
    plt.title('Cost Function Optimalization')
    plt.legend()
    plt.grid()
    plt.show()

