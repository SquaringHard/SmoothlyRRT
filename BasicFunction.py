from math import hypot, atan2, pi
from configs import *


def CalcDist(p1, p2):
    return hypot(p1[0] - p2[0], p1[1] - p2[1])


# Calculate angle p0-p1-p2
def CalcTheta(p0, p1, p2):
    theta1 = atan2(p1[1] - p0[1], p1[0] - p0[0])
    theta2 = atan2(p2[1] - p1[1], p2[0] - p1[0])
    return pi - abs(theta1 - theta2)


# Check whether the straight line from p1 to p2 collides with an obstacle by dividing the segment p1-p2 into num segments and check whether each point on the straight line from p1 to p2 is within the obstacle
def CheckCollision(p1, p2, obstacles):
    num = int(CalcDist(p1, p2) / EPS)
    dx = (p2[0] - p1[0]) / num
    dy = (p2[1] - p1[1]) / num
    for i in range(num + 1):
        point = [p1[0] + i * dx, p1[1] + i * dy]
        for obstacle in obstacles:
            # The generated points should be far away from obstacles
            if CalcDist(point, obstacle) <= 2.0 * OBSTACLES_RADIUS:
                return True
    return False