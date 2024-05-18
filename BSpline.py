import numpy as np
from configs import *

# For existing data points, they need to be mapped to the parameter domain [0, 1], where the parameter domain is divided according to the exponential result of the chord length of the data point
def centripetal(NumOfPoints, points):
    params = np.zeros(NumOfPoints)

    for i in range(1, NumOfPoints):
        dis = 0
        for j in range(len(points)):
            dis += (points[j][i]-points[j][i-1])**2
        dis = np.sqrt(dis)
        params[i] = params[i-1] + np.sqrt(dis)
        
    for i in range(1, NumOfPoints):
        params[i] /= params[NumOfPoints-1]

    return params

# Generate knot vector for use by basis functions
def GenerateKnot(params, k, N):
    m = N + k
    knot = np.zeros(m+1)

    for i in range(k+1):
        knot[i] = 0

    for i in range(k+1, m-k):
        for j in range(i-k, i):
            knot[i] += params[j]
        knot[i] = knot[i] / k

    for i in range(m-k, m+1):
        knot[i] = 1

    return knot

# Recursive Cox-deBoor formula to derive the base function of the B-spline curve
# i: the sequence number of the deBoor function, k: degree, u: parameter, knot: knot vector
def deBoor(i, k, u, knot):
    if k == 1:
        if u >= knot[i] and u < knot[i + 1]:
            return 1
        else:
            return 0
    else:
        if knot[i+k-1] == knot[i]:
            FirstTerm = 0
        else:
            FirstTerm = (u - knot[i]) / (knot[i+k-1] - knot[i]) * deBoor(i, k-1, u, knot)

        if knot[i+k] == knot[i+1]:
            SecondTerm = 0
        else:
            SecondTerm = (knot[i+k] - u) / (knot[i+k] - knot[i+1]) * deBoor(i+1, k-1, u, knot)

        return FirstTerm + SecondTerm

# Calculate the control points of the B-spline curve
# N: number of data points, k: number of times
def CurveInterpolation(SamplePoints, N, k, param, knot):
    Nik = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            Nik[i][j] = deBoor(j, k+1, param[i], knot)
    Nik[N-1][N-1] = 1

    InversedNik = np.linalg.inv(Nik)
    ControlPoints = []
    for i in range(len(SamplePoints)):
        ControlPoints.append(np.dot(InversedNik, SamplePoints[i]).tolist())

    return ControlPoints

# Generate B-spline curves based on parameters such as control points
# N: the number of control points; k: the number of times
def curve(ControlPoints, N, k, param, knot):
    Nik = np.zeros((len(param), N))
    for i in range(len(param)):
        for j in range(N):
            Nik[i][j] = deBoor(j, k+1, param[i], knot)
    Nik[len(param)-1][N-1] = 1

    DataPoints = []
    for i in range(len(ControlPoints)):
        DataPoints.append(np.dot(Nik, ControlPoints[i]).tolist())

    return DataPoints

# Generate B-spline curve based on sampling points
def GenerateBSpline(SamplePoints):
    NumOfSamples = len(SamplePoints)
    SamplePoints = np.transpose(SamplePoints)
    ParamCentripetal = centripetal(NumOfSamples, SamplePoints)
    knot = GenerateKnot(ParamCentripetal, K_ORDER, NumOfSamples)
    params = np.linspace(0, 1, NUM_OF_POINTS)
    DataPoints = curve(SamplePoints, NumOfSamples, K_ORDER, params, knot)
    return np.transpose(DataPoints)