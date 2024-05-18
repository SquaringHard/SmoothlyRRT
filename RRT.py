import math
from configs import *
from BasicFunction import *
from TreeClass import *

def RRT(start, goal, obstacles, PGoal = -1):
    tree = TreeClass()
    tree.AddPoint(start)
    CurrentPoint = start

    # Expand the tree until there is a point on the tree close enough to the end point and there are no obstacles on the way to the end point
    while CalcDist(CurrentPoint, goal) > 2.0 * OBSTACLES_RADIUS or CheckCollision(CurrentPoint, goal, obstacles):
        # Randomly generate a SamplePoint and extend a fixed step size from the CurrentPoint to this point to generate a new point
        # If this new point is not on the tree and the straight line to CurrentPoint does not intersect with the obstacle, add it to the tree
        SamplePoint = tree.SamplePoint(goal, PGoal)
        NearestPoint = tree.FindNearestPoint(SamplePoint)

        if SamplePoint != NearestPoint:
            theta = math.atan2(SamplePoint[1] - NearestPoint[1], SamplePoint[0] - NearestPoint[0])
            NewPoint = (int(NearestPoint[0] + STEP_LEN * math.cos(theta)),
                        int(NearestPoint[1] + STEP_LEN * math.sin(theta)))

            if not CheckCollision(NewPoint, NearestPoint, obstacles):
                tree.AddPoint(NewPoint)
                tree.parent[NewPoint] = NearestPoint
                CurrentPoint = NewPoint

        # If the number of generated points exceeds MAX_NUM_OF_POINTS, the task will be terminated
        if len(tree.points) > MAX_NUM_OF_POINTS:
            print('Failed to generate a tree from start to goal.')
            break

    # If the end point is not on the tree, add it manually
    if goal not in tree.parent:
        tree.AddPoint(goal)
        tree.parent[goal] = CurrentPoint

    return tree