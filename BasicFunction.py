import math
from configs import *

def CalcDist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Calculate angle p0-p1-p2
def CalcTheta(p0, p1, p2):
    theta1 = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    theta2 = math.atan2(p2[1] - p1[1], p2[0] - p1[0])

    if theta1 * theta2 >= 0:
        theta = abs(theta1-theta2)
    else:
        theta = abs(theta1) + abs(theta2)
        if theta > math.pi:
            theta = 2 * math.pi - theta
            
    theta = math.pi - theta
    return theta

# Check whether the straight line from p1 to p2 collides with an obstacle by dividing the segment p1-p2 into num segments and check whether each point on the straight line from p1 to p2 is within the obstacle
def CheckCollision(p1, p2, obstacles):
    num = max(int(abs(p1[0] - p2[0])), int(abs(p1[1] - p2[1])), 2)
    dx = (p2[0] - p1[0])/num
    dy = (p2[1] - p1[1])/num
    
    IsColliding = False
    for i in range(num+1):
        point = [int(p1[0] + i*dx), int(p1[1] + i*dy)]
        for obstacle in obstacles:
            # The generated points should be far away from obstacles
            if CalcDist(point, obstacle) <= 2.0 * OBSTACLES_RADIUS:
                IsColliding = True
                break
        if IsColliding:
            break
    return IsColliding