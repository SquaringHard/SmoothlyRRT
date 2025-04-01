import numpy as np
from configs import *


# For existing data points, they need to be mapped to the parameter domain [0, 1], where the parameter domain is divided according to the exponential result of the chord length of the data point
def centripetal(NumOfPoints, points):
    params = np.zeros(NumOfPoints)

    for i in range(1, NumOfPoints):
        dis = 0
        for point in points:
            dis += (point[i] - point[i - 1]) ** 2
        params[i] = params[i - 1] + dis ** 0.25
        
    params /= params[-1]
    return params


# Generate knot vector for use by basis functions
def GenerateKnot(params, k, N):
    m = N + k
    knot = np.zeros(m+1)

    for i in range(k + 1, m - k):
        knot[i] = np.sum(params[i - k : i]) / k

    knot[m - k : m + 1] = 1
    return knot


# Recursive Cox-deBoor formula to derive the base function of the B-spline curve
# i: the sequence number of the deBoor function, k: degree, u: parameter, knot: knot vector
def deBoor(i, k, u, knot):
    if k == 1:
        return u >= knot[i] and u < knot[i + 1]

    FirstTerm = 0 if knot[i + k - 1] == knot[i]\
                else (u - knot[i]) / (knot[i + k - 1] - knot[i]) * deBoor(i, k - 1, u, knot)

    SecondTerm = 0 if knot[i+k] == knot[i+1]\
                 else (knot[i + k] - u) / (knot[i + k] - knot[i + 1]) * deBoor(i+1, k-1, u, knot)

    return FirstTerm + SecondTerm


# Generate B-spline curves based on parameters such as control points
# N: the number of control points; k: the number of times
def curve(ControlPoints, N, k, param, knot):
    Nik = np.zeros((len(param), N))
    for i in range(len(param)):
        for j in range(N):
            Nik[i][j] = deBoor(j, k + 1, param[i], knot)
    Nik[-1][-1] = 1
    return np.transpose([np.dot(Nik, point) for point in ControlPoints])


# Generate B-spline curve based on sampling points
def GenerateBSpline(SamplePoints):
    NumOfSamples = len(SamplePoints)
    SamplePoints = np.transpose(SamplePoints)
    knot = GenerateKnot(centripetal(NumOfSamples, SamplePoints), K_ORDER, NumOfSamples)
    params = np.linspace(0, 1, NUM_OF_POINTS)
    return curve(SamplePoints, NumOfSamples, K_ORDER, params, knot)